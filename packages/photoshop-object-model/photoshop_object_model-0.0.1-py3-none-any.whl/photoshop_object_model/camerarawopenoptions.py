
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from pscamerarawsize import PsCameraRAWSize
    from pscamerarawsettingstype import PsCameraRAWSettingsType
    from psbitsperchanneltype import PsBitsPerChannelType
    from pscolorspacetype import PsColorSpaceType
    from pswhitebalancetype import PsWhiteBalanceType
    from application import Application

class CameraRAWOpenOptions():
    """
    Options that can be specified when opening a document in Camera Raw format.
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def BitsPerChannel(self) -> PsBitsPerChannelType:
        """
        Read-write. The number of bits per channel.
        """
        ...

    @property
    def BlueHue(self) -> int:
        """
        Read-write. The blue hue of the shot (-100 - 100).
        """
        ...

    @property
    def BlueSaturation(self) -> int:
        """
        Read-write. The blue saturation of the shot (-100 - 100).
        """
        ...

    @property
    def Brightness(self) -> int:
        """
        Read-write. The brightness of the shot (0 - 150).
        """
        ...

    @property
    def ChromaticAberrationBY(self) -> int:
        """
        Read-write. The chromatic aberration B/Y of the shot (-100 - 100).
        """
        ...

    @property
    def ChromaticAberrationRC(self) -> int:
        """
        Read-write. The chromatic aberration R/C of the shot (-100 - 100).
        """
        ...

    @property
    def ColorNoiseReduction(self) -> int:
        """
        Read-write. The color noise reduction of the shot (0 - 100).
        """
        ...

    @property
    def ColorSpace(self) -> PsColorSpaceType:
        """
        Read-write. The colorspace for the image.
        """
        ...

    @property
    def Contrast(self) -> int:
        """
        Read-write. The contrast of the shot (-50 - 100).
        """
        ...

    @property
    def Exposure(self) -> float:
        """
        Read-write. The exposure of the shot (4.0 - 4.0).
        """
        ...

    @property
    def GreenHue(self) -> int:
        """
        Read-write. The green hue of the shot (-100 - 100).
        """
        ...

    @property
    def GreenSaturation(self) -> int:
        """
        Read-write. The green saturation of the shot (-100 - 100).
        """
        ...

    @property
    def LuminanceSmoothing(self) -> int:
        """
        Read-write. The luminance smoothing of the shot (0 - 100).
        """
        ...

    @property
    def RedHue(self) -> int:
        """
        Read-write. The red hue of the shot (-100 - 100).
        """
        ...

    @property
    def RedSaturation(self) -> int:
        """
        Read-write. The red saturation of the shot (-100 - 100).
        """
        ...

    @property
    def Resolution(self) -> float:
        """
        Read-write. The resolution of the document in pixels per inch (1 - 999).
        """
        ...

    @property
    def Saturation(self) -> int:
        """
        Read-write. The saturation of the shot (-100 - 100).
        """
        ...

    @property
    def Settings(self) -> PsCameraRAWSettingsType:
        """
        Read-write. The global settings for all Camera RAW options. Default: 0 (psCameraDefault).
        """
        ...

    @property
    def Shadows(self) -> int:
        """
        Read-write. The shadows of the shot (0 - 100).
        """
        ...

    @property
    def ShadowTint(self) -> int:
        """
        Read-write. The shadow tint of the shot (-100 - 100).
        """
        ...

    @property
    def Sharpness(self) -> int:
        """
        Read-write. The sharpness of the shot (0 - 100).
        """
        ...

    @property
    def Size(self) -> PsCameraRAWSize:
        """
        Read-write. The size of the new document.
        """
        ...

    @property
    def Temperature(self) -> int:
        """
        Read-write. The temperature of the shot (2000 - 50000).
        """
        ...

    @property
    def Tint(self) -> int:
        """
        Read-write. The tint of the shot (-150 - 150).
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced CameraRAWOpenOptions object.
        """
        ...

    @property
    def VignettingAmount(self) -> int:
        """
        Read-write. The vignetting amount of the shot (-100 - 100).
        """
        ...

    @property
    def VignettingMidpoint(self) -> int:
        """
        Read-write. The vignetting mid point of the shot (-100 - 100).
        """
        ...

    @property
    def WhiteBalance(self) -> PsWhiteBalanceType:
        """
        Read-write. The white balance options for the image.
        """
        ...

