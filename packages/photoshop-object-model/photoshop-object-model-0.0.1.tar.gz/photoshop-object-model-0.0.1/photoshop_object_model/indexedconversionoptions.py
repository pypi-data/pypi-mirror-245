
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from psforcedcolors import PsForcedColors
    from pspalettetype import PsPaletteType
    from psdithertype import PsDitherType
    from application import Application
    from psmattetype import PsMatteType

class IndexedConversionOptions():
    """
    Options that can be specified when converting an RGB image to an indexed color model. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Colors(self) -> int:
        """
        Read-write. The number of palette colors. Note:Valid only when Palette = 2 (psMacOSPalette) 3 (psWindowsPalette) 4 (psWebPalette) 5 (psUniform) 6 (psLocalPerceptual) 7 (psLocalSelective) 8 (psLocalAdaptive) See Palette.
        """
        ...

    @property
    def Dither(self) -> PsDitherType:
        """
        Read-write. The dither type.
        """
        ...

    @property
    def DitherAmount(self) -> int:
        """
        Read-write. The amount of dither. (1 - 100). Note:Valid only when Dither = 2 (psDiffusion).
        """
        ...

    @property
    def Forced(self) -> PsForcedColors:
        """
        Read-write. The type of colors to force into the color palette.
        """
        ...

    @property
    def Matte(self) -> PsMatteType:
        """
        Read-write. Read-write. The color to use to fill antialiased edges adjacent to transparent areas of the image. Default: 4 (psWhiteMatte). Note:When Transparency = false, the matte color is applied to transparent areas. See Transparency.
        """
        ...

    @property
    def Palette(self) -> PsPaletteType:
        """
        Read-write. The palette type. Default: 1 (psExact).
        """
        ...

    @property
    def PreserveExactColors(self) -> bool:
        """
        Read-write.Indicates whether to protect colors in the image that contain entries in the color table from being dithered. Note:Valid only when Dither = 2. (psDiffusion) See Dither.
        """
        ...

    @property
    def Transparency(self) -> bool:
        """
        Read-write. Indicates whether to preserve transparent areas of the image during conversion to GIF format.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced IndexedConversionOptions object.
        """
        ...

