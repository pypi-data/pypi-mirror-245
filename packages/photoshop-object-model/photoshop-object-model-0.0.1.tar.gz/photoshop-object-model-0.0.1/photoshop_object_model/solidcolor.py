
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from rgbcolor import RGBColor
    from labcolor import LabColor
    from pscolormodel import PsColorModel
    from graycolor import GrayColor
    from application import Application
    from cmykcolor import CMYKColor
    from hsbcolor import HSBColor

class SolidColor():
    """
    A color definition used in the document. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def CMYK(self) -> CMYKColor:
        """
        Read-write. The CMYK color mode.
        """
        ...

    @property
    def Gray(self) -> GrayColor:
        """
        Read-write. The Grayscale color mode.
        """
        ...

    @property
    def HSB(self) -> HSBColor:
        """
        Read-write. The HSB color mode.
        """
        ...

    @property
    def Lab(self) -> LabColor:
        """
        Read-write. The LAB color mode.
        """
        ...

    @property
    def Model(self) -> PsColorModel:
        """
        Read-write. The color model.
        """
        ...

    @property
    def NearestWebColor(self) -> RGBColor:
        """
        Read-only. The nearest Web color to the current color.
        """
        ...

    @property
    def RGB(self) -> RGBColor:
        """
        Read-write. The RGB color mode.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced SolidColor object.
        """
        ...

    def IsEqual(self, Color) -> bool:
        """
        Indicates whether the SolidColor object is visually equal to the specified color.
        """
        ...

