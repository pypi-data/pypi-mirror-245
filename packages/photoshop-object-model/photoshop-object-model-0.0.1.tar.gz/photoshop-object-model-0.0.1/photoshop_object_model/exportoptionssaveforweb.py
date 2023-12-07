
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from rgbcolor import RGBColor
    from pscolorreductiontype import PsColorReductionType
    from psdithertype import PsDitherType
    from pssavedocumenttype import PsSaveDocumentType
    from application import Application

class ExportOptionsSaveForWeb():
    """
    Options that can be specified when optimizing a document for the Web, or for devices. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Blur(self) -> float:
        """
        Read-write. Applies blur to the image to reduce artifacts. Default: 0.0.
        """
        ...

    @property
    def ColorReduction(self) -> PsColorReductionType:
        """
        Read-write. The color reduction algorithm. Default: 1 (psSelective).
        """
        ...

    @property
    def Colors(self) -> int:
        """
        Read-write. The number of colors in the palette. Default: 256.
        """
        ...

    @property
    def Dither(self) -> PsDitherType:
        """
        Read-write. The type of dither. Default: 2 (psDiffusion).
        """
        ...

    @property
    def DitherAmount(self) -> int:
        """
        Read-write. The amount of dither. Default: 100. Note:Valid only when Dither = 2. See Dither.
        """
        ...

    @property
    def Format(self) -> PsSaveDocumentType:
        """
        Read-write. The file format to use. Default: 3 (psCompuServeGIFSave).
        """
        ...

    @property
    def IncludeProfile(self) -> bool:
        """
        Read-write. Indicates whether to include the document’s embedded color profile. Default: false.
        """
        ...

    @property
    def Interlaced(self) -> bool:
        """
        Read-write. Indicates whether to download in multiple passes; progressive. Default: false.
        """
        ...

    @property
    def Lossy(self) -> int:
        """
        Read-write. The amount of lossiness allowed. Default: 0.
        """
        ...

    @property
    def MatteColor(self) -> RGBColor:
        """
        Read-write. The colors to blend transparent pixels against.
        """
        ...

    @property
    def Optimized(self) -> bool:
        """
        Read-write. Indicates whether to create smaller but less compatible files. Default: true. Note:Valid only when format = 6 (psJPEGSave). See Format.
        """
        ...

    @property
    def PNG8(self) -> bool:
        """
        Read-write. Indicates the number of bits; true = 8, false = 24. Default: true. Note:Valid only when format = 13 (psPNGSave). See Format.
        """
        ...

    @property
    def Quality(self) -> int:
        """
        Read-write. The quality of the produced image (0 - 100 as percentage; default: 60).
        """
        ...

    @property
    def Transparency(self) -> bool:
        """
        Read-write. Indicates transparent areas of the image should be included in the saved image. Default: true.
        """
        ...

    @property
    def TransparencyAmount(self) -> int:
        """
        Read-write. The amount of transparency dither. Default: 100. Note:Valid only if Transparency = true. See Transparency.
        """
        ...

    @property
    def TransparencyDither(self) -> PsDitherType:
        """
        Read-write. The transparency dither algorithm. Default: 1.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced ExportOptionsSaveForWeb object.
        """
        ...

    @property
    def WebSnap(self) -> int:
        """
        Read-write. The tolerance amount within which to snap close colors to Web palette colors. Default: 0.
        """
        ...

