import copy
import math
from functools import partial
from typing import Any, Callable, List, Optional, Sequence
import torch
from torch import nn, Tensor
from ..ops.stochastic_depth import StochasticDepth
from ..ops.misc import ConvNormActivation, SqueezeExcitation
from .utils import _make_divisible, load_state_dict_from_url
from ...builder import NETS


__all__ = (
    "EfficientNet",
    "efficientnet_b0",
    "efficientnet_b1",
    "efficientnet_b2",
    "efficientnet_b3",
    "efficientnet_b4",
    "efficientnet_b5",
    "efficientnet_b6",
    "efficientnet_b7",
    "efficientnet_b8",
    "efficientnet_l2",
)


model_urls = {
    # Weights ported from https://github.com/rwightman/pytorch-image-models/
    "efficientnet_b0": "https://download.pytorch.org/models/efficientnet_b0_rwightman-3dd342df.pth",
    "efficientnet_b1": "https://download.pytorch.org/models/efficientnet_b1_rwightman-533bc792.pth",
    "efficientnet_b2": "https://download.pytorch.org/models/efficientnet_b2_rwightman-bcdf34b7.pth",
    "efficientnet_b3": "https://download.pytorch.org/models/efficientnet_b3_rwightman-cf984f9c.pth",
    "efficientnet_b4": "https://download.pytorch.org/models/efficientnet_b4_rwightman-7eb33cd5.pth",
    # Weights ported from https://github.com/lukemelas/EfficientNet-PyTorch/
    "efficientnet_b5": "https://download.pytorch.org/models/efficientnet_b5_lukemelas-b6417697.pth",
    "efficientnet_b6": "https://download.pytorch.org/models/efficientnet_b6_lukemelas-c76e70fd.pth",
    "efficientnet_b7": "https://download.pytorch.org/models/efficientnet_b7_lukemelas-dcc49843.pth",
}


def efficientnet_params(model_name):
    """Map EfficientNet model name to parameter coefficients.

    Args:
        model_name (str): Model name to be queried.

    Returns:
        params_dict[model_name]: A (width,depth,res,dropout) tuple.
    """
    params_dict = {
        # Coefficients:   width,depth,res,dropout
        'efficientnet-b0': (1.0, 1.0, 224, 0.2),
        'efficientnet-b1': (1.0, 1.1, 240, 0.2),
        'efficientnet-b2': (1.1, 1.2, 260, 0.3),
        'efficientnet-b3': (1.2, 1.4, 300, 0.3),
        'efficientnet-b4': (1.4, 1.8, 380, 0.4),
        'efficientnet-b5': (1.6, 2.2, 456, 0.4),
        'efficientnet-b6': (1.8, 2.6, 528, 0.5),
        'efficientnet-b7': (2.0, 3.1, 600, 0.5),
        'efficientnet-b8': (2.2, 3.6, 672, 0.5),
        'efficientnet-l2': (4.3, 5.3, 800, 0.5),
    }
    return params_dict[model_name]


class MBConvConfig:
    # Stores information listed at Table 1 of the EfficientNet paper
    def __init__(
        self,
        expand_ratio: float,
        kernel: int,
        stride: int,
        input_channels: int,
        out_channels: int,
        num_layers: int,
        width_mult: float,
        depth_mult: float,
    ) -> None:
        self.expand_ratio = expand_ratio
        self.kernel = kernel
        self.stride = stride
        self.input_channels = self.adjust_channels(input_channels, width_mult)
        self.out_channels = self.adjust_channels(out_channels, width_mult)
        self.num_layers = self.adjust_depth(num_layers, depth_mult)

    def __repr__(self) -> str:
        s = self.__class__.__name__ + "("
        s += "expand_ratio={expand_ratio}"
        s += ", kernel={kernel}"
        s += ", stride={stride}"
        s += ", input_channels={input_channels}"
        s += ", out_channels={out_channels}"
        s += ", num_layers={num_layers}"
        s += ")"
        return s.format(**self.__dict__)

    @staticmethod
    def adjust_channels(channels: int, width_mult: float, min_value: Optional[int] = None) -> int:
        return _make_divisible(channels * width_mult, 8, min_value)

    @staticmethod
    def adjust_depth(num_layers: int, depth_mult: float):
        return int(math.ceil(num_layers * depth_mult))


class MBConv(nn.Module):
    def __init__(
        self,
        cnf: MBConvConfig,
        stochastic_depth_prob: float,
        norm_layer: Callable[..., nn.Module],
        se_layer: Callable[..., nn.Module] = SqueezeExcitation,
    ) -> None:
        super().__init__()

        if not (1 <= cnf.stride <= 2):
            raise ValueError("illegal stride value")

        self.use_res_connect = cnf.stride == 1 and cnf.input_channels == cnf.out_channels

        layers: List[nn.Module] = []
        activation_layer = nn.SiLU

        # expand
        expanded_channels = cnf.adjust_channels(cnf.input_channels, cnf.expand_ratio)
        if expanded_channels != cnf.input_channels:
            layers.append(
                ConvNormActivation(
                    cnf.input_channels,
                    expanded_channels,
                    kernel_size=1,
                    norm_layer=norm_layer,
                    activation_layer=activation_layer,
                )
            )

        # depthwise
        layers.append(
            ConvNormActivation(
                expanded_channels,
                expanded_channels,
                kernel_size=cnf.kernel,
                stride=cnf.stride,
                groups=expanded_channels,
                norm_layer=norm_layer,
                activation_layer=activation_layer,
            )
        )

        # squeeze and excitation
        squeeze_channels = max(1, cnf.input_channels // 4)
        layers.append(se_layer(expanded_channels, squeeze_channels, activation=partial(nn.SiLU, inplace=True)))

        # project
        layers.append(
            ConvNormActivation(
                expanded_channels, cnf.out_channels, kernel_size=1, norm_layer=norm_layer, activation_layer=None
            )
        )

        self.block = nn.Sequential(*layers)
        self.stochastic_depth = StochasticDepth(stochastic_depth_prob, "row")
        self.out_channels = cnf.out_channels

    def forward(self, input: Tensor) -> Tensor:
        result = self.block(input)
        if self.use_res_connect:
            result = self.stochastic_depth(result)
            result += input
        return result


@NETS.register_module()
class EfficientNet(nn.Module):
    def __init__(
        self,
        inverted_residual_setting: List[MBConvConfig],
        dropout: float,
        stochastic_depth_prob: float = 0.2,
        num_classes: int = 1000,
        input_dim: int = 3,
        block: Optional[Callable[..., nn.Module]] = None,
        norm_layer: Optional[Callable[..., nn.Module]] = None,
        priors: List[float] = None,
        **kwargs: Any,
    ) -> None:
        """
        EfficientNet main class

        Args:
            inverted_residual_setting (List[MBConvConfig]): network structure.
            dropout (float): the droupout probability.
            stochastic_depth_prob (float): the stochastic depth probability.
            num_classes (int): number of classes.
            input_dim (int): dimension of input.
            block (Optional[Callable[..., nn.Module]]): module specifying inverted residual building block for mobilenet.
            norm_layer (Optional[Callable[..., nn.Module]]): module specifying the normalization layer to use.
        """
        super().__init__()

        if not inverted_residual_setting:
            raise ValueError("The inverted_residual_setting should not be empty")
        elif not (
            isinstance(inverted_residual_setting, Sequence)
            and all([isinstance(s, MBConvConfig) for s in inverted_residual_setting])
        ):
            raise TypeError("The inverted_residual_setting should be List[MBConvConfig]")

        if block is None:
            block = MBConv

        if norm_layer is None:
            norm_layer = nn.BatchNorm2d

        layers: List[nn.Module] = []

        # building first layer
        firstconv_output_channels = inverted_residual_setting[0].input_channels
        layers.append(
            ConvNormActivation(
                input_dim, firstconv_output_channels, kernel_size=3, stride=2, norm_layer=norm_layer, activation_layer=nn.SiLU
            )
        )

        # building inverted residual blocks
        total_stage_blocks = sum([cnf.num_layers for cnf in inverted_residual_setting])
        stage_block_id = 0
        for cnf in inverted_residual_setting:
            stage: List[nn.Module] = []
            for _ in range(cnf.num_layers):
                # copy to avoid modifications. shallow copy is enough
                block_cnf = copy.copy(cnf)

                # overwrite info if not the first conv in the stage
                if stage:
                    block_cnf.input_channels = block_cnf.out_channels
                    block_cnf.stride = 1

                # adjust stochastic depth probability based on the depth of the stage block
                sd_prob = stochastic_depth_prob * float(stage_block_id) / total_stage_blocks

                stage.append(block(block_cnf, sd_prob, norm_layer))
                stage_block_id += 1

            layers.append(nn.Sequential(*stage))

        # building last several layers
        lastconv_input_channels = inverted_residual_setting[-1].out_channels
        lastconv_output_channels = 4 * lastconv_input_channels
        self.num_features = lastconv_output_channels
        layers.append(
            ConvNormActivation(
                lastconv_input_channels,
                lastconv_output_channels,
                kernel_size=1,
                norm_layer=norm_layer,
                activation_layer=nn.SiLU,
            )
        )

        self.features = nn.Sequential(*layers)
        self.avgpool = nn.AdaptiveAvgPool2d(1)
        self.classifier = nn.Sequential(
            nn.Dropout(p=dropout, inplace=True),
            nn.Linear(lastconv_output_channels, num_classes),
        )

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode="fan_out")
                if m.bias is not None:
                    nn.init.zeros_(m.bias)
            elif isinstance(m, (nn.BatchNorm2d, nn.GroupNorm)):
                nn.init.ones_(m.weight)
                nn.init.zeros_(m.bias)
            elif isinstance(m, nn.Linear):
                init_range = 1.0 / math.sqrt(m.out_features)
                nn.init.uniform_(m.weight, -init_range, init_range)
                nn.init.zeros_(m.bias)

        self.priors = priors
        if self.priors is not None:
            if len(self.priors) == 1:
                self.classifier[-1].bias.data.fill_(self.priors[0])
            else:
                with torch.no_grad():
                    self.classifier[-1].bias.data = torch.as_tensor(self.priors, device=self.classifier[-1].bias.device)
            
    def _forward_impl(self, x: Tensor) -> Tensor:
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

    def forward(self, x: Tensor) -> Tensor:
        return self._forward_impl(x)


def _efficientnet_conf(width_mult: float, depth_mult: float, **kwargs: Any) -> List[MBConvConfig]:
    bneck_conf = partial(MBConvConfig, width_mult=width_mult, depth_mult=depth_mult)
    inverted_residual_setting = [
        bneck_conf(1, 3, 1, 32, 16, 1),
        bneck_conf(6, 3, 2, 16, 24, 2),
        bneck_conf(6, 5, 2, 24, 40, 2),
        bneck_conf(6, 3, 2, 40, 80, 3),
        bneck_conf(6, 5, 1, 80, 112, 3),
        bneck_conf(6, 5, 2, 112, 192, 4),
        bneck_conf(6, 3, 1, 192, 320, 1),
    ]
    return inverted_residual_setting


def _efficientnet_model(
    arch: str,
    input_dim: int,
    inverted_residual_setting: List[MBConvConfig],
    dropout: float,
    pretrained: str,
    progress: bool,
    model_dir: str,
    **kwargs: Any,
) -> EfficientNet:
    model = EfficientNet(inverted_residual_setting, dropout, input_dim=input_dim, **kwargs)
    if (pretrained == 'imagenet') & (input_dim == 3):
        if model_urls.get(arch, None) is None:
            raise ValueError("No checkpoint is available for model type {}".format(arch))
        state_dict = load_state_dict_from_url(model_urls[arch], model_dir=model_dir, progress=progress)
        model.load_state_dict(state_dict)
    elif len(pretrained) > 0:
        state_dict = torch.load(pretrained)
        model.load_state_dict(state_dict, strict=False)
    return model


@NETS.register_module()
def efficientnet_b0(input_dim: int = 3, pretrained: str = '', progress: bool = True,
                    model_dir: str = '.', **kwargs: Any) -> EfficientNet:
    """
    Constructs a EfficientNet B0 architecture from
    `"EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks" <https://arxiv.org/abs/1905.11946>`_.

    Args:
        input_dim (int): dimension of input.
        pretrained (str): specifies directory of pretrained model. `pretrained='imagenet'` uses ImageNet pretrained model.
        progress (bool): if True, displays a progress bar of the download to stderr.
        model_dir (str): directory of pretrained model.
    """
    inverted_residual_setting = _efficientnet_conf(width_mult=1.0, depth_mult=1.0, **kwargs)
    return _efficientnet_model("efficientnet_b0", input_dim, inverted_residual_setting, 0.2,
                                pretrained, progress, model_dir, **kwargs)


@NETS.register_module()
def efficientnet_b1(input_dim: int = 3, pretrained: str = '', progress: bool = True,
                    model_dir: str = '.', **kwargs: Any) -> EfficientNet:
    """
    Constructs a EfficientNet B1 architecture from
    `"EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks" <https://arxiv.org/abs/1905.11946>`_.

    Args:
        input_dim (int): dimension of input.
        pretrained (str): specifies directory of pretrained model. `pretrained='imagenet'` uses ImageNet pretrained model.
        progress (bool): if True, displays a progress bar of the download to stderr.
        model_dir (str): directory of pretrained model.
    """
    inverted_residual_setting = _efficientnet_conf(width_mult=1.0, depth_mult=1.1, **kwargs)
    return _efficientnet_model("efficientnet_b1", input_dim, inverted_residual_setting, 0.2,
                                pretrained, progress, model_dir, **kwargs)


@NETS.register_module()
def efficientnet_b2(input_dim: int = 3, pretrained: str = '', progress: bool = True,
                    model_dir: str = '.', **kwargs: Any) -> EfficientNet:
    """
    Constructs a EfficientNet B2 architecture from
    `"EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks" <https://arxiv.org/abs/1905.11946>`_.

    Args:
        input_dim (int): dimension of input.
        pretrained (str): specifies directory of pretrained model. `pretrained='imagenet'` uses ImageNet pretrained model.
        progress (bool): if True, displays a progress bar of the download to stderr.
        model_dir (str): directory of pretrained model.
    """
    inverted_residual_setting = _efficientnet_conf(width_mult=1.1, depth_mult=1.2, **kwargs)
    return _efficientnet_model("efficientnet_b2", input_dim, inverted_residual_setting, 0.3,
                                pretrained, progress, model_dir, **kwargs)


@NETS.register_module()
def efficientnet_b3(input_dim: int = 3, pretrained: str = '', progress: bool = True,
                    model_dir: str = '.', **kwargs: Any) -> EfficientNet:
    """
    Constructs a EfficientNet B3 architecture from
    `"EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks" <https://arxiv.org/abs/1905.11946>`_.

    Args:
        input_dim (int): dimension of input.
        pretrained (str): specifies directory of pretrained model. `pretrained='imagenet'` uses ImageNet pretrained model.
        progress (bool): if True, displays a progress bar of the download to stderr.
        model_dir (str): directory of pretrained model.
    """
    inverted_residual_setting = _efficientnet_conf(width_mult=1.2, depth_mult=1.4, **kwargs)
    return _efficientnet_model("efficientnet_b3", input_dim, inverted_residual_setting, 0.3,
                                pretrained, progress, model_dir, **kwargs)


@NETS.register_module()
def efficientnet_b4(input_dim: int = 3, pretrained: str = '', progress: bool = True,
                    model_dir: str = '.', **kwargs: Any) -> EfficientNet:
    """
    Constructs a EfficientNet B4 architecture from
    `"EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks" <https://arxiv.org/abs/1905.11946>`_.

    Args:
        input_dim (int): dimension of input.
        pretrained (str): specifies directory of pretrained model. `pretrained='imagenet'` uses ImageNet pretrained model.
        progress (bool): if True, displays a progress bar of the download to stderr.
        model_dir (str): directory of pretrained model.
    """
    inverted_residual_setting = _efficientnet_conf(width_mult=1.4, depth_mult=1.8, **kwargs)
    return _efficientnet_model("efficientnet_b4", input_dim, inverted_residual_setting, 0.4,
                                pretrained, progress, model_dir, **kwargs)


@NETS.register_module()
def efficientnet_b5(input_dim: int = 3, pretrained: str = '', progress: bool = True,
                    model_dir: str = '.', **kwargs: Any) -> EfficientNet:
    """
    Constructs a EfficientNet B5 architecture from
    `"EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks" <https://arxiv.org/abs/1905.11946>`_.

    Args:
        input_dim (int): dimension of input.
        pretrained (str): specifies directory of pretrained model. `pretrained='imagenet'` uses ImageNet pretrained model.
        progress (bool): if True, displays a progress bar of the download to stderr.
        model_dir (str): directory of pretrained model.
    """
    inverted_residual_setting = _efficientnet_conf(width_mult=1.6, depth_mult=2.2, **kwargs)
    return _efficientnet_model(
        "efficientnet_b5", input_dim,
        inverted_residual_setting,
        0.4,
        pretrained,
        progress,
        model_dir,
        norm_layer=partial(nn.BatchNorm2d, eps=0.001, momentum=0.01),
        **kwargs,
    )


@NETS.register_module()
def efficientnet_b6(input_dim: int = 3, pretrained: str = '', progress: bool = True,
                    model_dir: str = '.', **kwargs: Any) -> EfficientNet:
    """
    Constructs a EfficientNet B6 architecture from
    `"EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks" <https://arxiv.org/abs/1905.11946>`_.

    Args:
        input_dim (int): dimension of input.
        pretrained (str): specifies directory of pretrained model. `pretrained='imagenet'` uses ImageNet pretrained model.
        progress (bool): if True, displays a progress bar of the download to stderr.
        model_dir (str): directory of pretrained model.
    """
    inverted_residual_setting = _efficientnet_conf(width_mult=1.8, depth_mult=2.6, **kwargs)
    return _efficientnet_model(
        "efficientnet_b6", input_dim,
        inverted_residual_setting,
        0.5,
        pretrained,
        progress,
        model_dir,
        norm_layer=partial(nn.BatchNorm2d, eps=0.001, momentum=0.01),
        **kwargs,
    )


@NETS.register_module()
def efficientnet_b7(input_dim: int = 3, pretrained: str = '', progress: bool = True,
                    model_dir: str = '.', **kwargs: Any) -> EfficientNet:
    """
    Constructs a EfficientNet B7 architecture from
    `"EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks" <https://arxiv.org/abs/1905.11946>`_.

    Args:
        input_dim (int): dimension of input.
        pretrained (str): specifies directory of pretrained model. `pretrained='imagenet'` uses ImageNet pretrained model.
        progress (bool): if True, displays a progress bar of the download to stderr.
        model_dir (str): directory of pretrained model.
    """
    inverted_residual_setting = _efficientnet_conf(width_mult=2.0, depth_mult=3.1, **kwargs)
    return _efficientnet_model(
        "efficientnet_b7", input_dim,
        inverted_residual_setting,
        0.5,
        pretrained,
        progress,
        model_dir,
        norm_layer=partial(nn.BatchNorm2d, eps=0.001, momentum=0.01),
        **kwargs,
    )


@NETS.register_module()
def efficientnet_b8(input_dim: int = 3, pretrained: str = '', progress: bool = True,
                    model_dir: str = '.', **kwargs: Any) -> EfficientNet:
    """
    Constructs a EfficientNet B8 architecture from
    `"EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks" <https://arxiv.org/abs/1905.11946>`_.

    Args:
        input_dim (int): dimension of input.
        pretrained (str): specifies directory of pretrained model. `pretrained='imagenet'` uses ImageNet pretrained model.
        progress (bool): if True, displays a progress bar of the download to stderr.
        model_dir (str): directory of pretrained model.
    """
    inverted_residual_setting = _efficientnet_conf(width_mult=2.2, depth_mult=3.6, **kwargs)
    return _efficientnet_model(
        "efficientnet_b8", input_dim,
        inverted_residual_setting,
        0.5,
        pretrained,
        progress,
        model_dir,
        norm_layer=partial(nn.BatchNorm2d, eps=0.001, momentum=0.01),
        **kwargs,
    )


@NETS.register_module()
def efficientnet_l2(input_dim: int = 3, pretrained: str = '', progress: bool = True,
                    model_dir: str = '.', **kwargs: Any) -> EfficientNet:
    """
    Constructs a EfficientNet B8 architecture from
    `"EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks" <https://arxiv.org/abs/1905.11946>`_.

    Args:
        input_dim (int): dimension of input.
        pretrained (str): specifies directory of pretrained model. `pretrained='imagenet'` uses ImageNet pretrained model.
        progress (bool): if True, displays a progress bar of the download to stderr.
        model_dir (str): directory of pretrained model.
    """
    inverted_residual_setting = _efficientnet_conf(width_mult=4.3, depth_mult=5.3, **kwargs)
    return _efficientnet_model(
        "efficientnet_l2", input_dim,
        inverted_residual_setting,
        0.5,
        pretrained,
        progress,
        model_dir,
        norm_layer=partial(nn.BatchNorm2d, eps=0.001, momentum=0.01),
        **kwargs,
    )