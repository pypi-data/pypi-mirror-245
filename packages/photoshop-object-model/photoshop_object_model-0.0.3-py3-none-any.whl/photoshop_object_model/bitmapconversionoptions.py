
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .application import Application
    from .psbitmaphalftonetype import PsBitmapHalfToneType
    from .psbitmapconversiontype import PsBitmapConversionType

class BitmapConversionOptions():
    """
    Options to specify when converting an image to Bitmap mode.Note: Convert color images to grayscale before converting the image to bitmap mode. See ‘Desaturate ’ on page 31 (in the Properties table of the ArtLayer object). 
    """
    @property
    def Angle(self) -> float:
        """
        Read-write. The angle (in degrees) at which to orient individual dots (-180 - 180). See Shape. Note:Valid only when Method = 4. See Method.
        """
        ...

    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Frequency(self) -> float:
        """
        Read-write. The number of printer dots (per inch) to use (1.0 - 999.99). Note:Valid only when Method = 4. See Method.
        """
        ...

    @property
    def Method(self) -> PsBitmapConversionType:
        """
        Read-write. The conversion method to use. Default: 3.
        """
        ...

    @property
    def PatternName(self) -> str:
        """
        Read-write. The name of the pattern to use. Note:Valid only when Method = 5. See Method.
        """
        ...

    @property
    def Resolution(self) -> float:
        """
        Read-write. The output resolution in pixels per inch. Default: 72.0.
        """
        ...

    @property
    def Shape(self) -> PsBitmapHalfToneType:
        """
        Read-write. The dot shape to use. Note:Valid only when Method = 1. See Method.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced BitmapConversionOptions object.
        """
        ...

