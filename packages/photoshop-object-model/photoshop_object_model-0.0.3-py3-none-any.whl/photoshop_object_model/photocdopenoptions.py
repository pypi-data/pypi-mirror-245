
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .psorientation import PsOrientation
    from .application import Application
    from .psphotocdsize import PsPhotoCDSize
    from .psphotocdcolorspace import PsPhotoCDColorSpace

class PhotoCDOpenOptions():
    """
    DEPRECATED in Adobe Photoshop. Kodak PhotoCD is now found in the Goodies folder on the Adobe Photoshop Install DVD.Options to be specified when opening a Kodak Photo CD (PCD) files, including high-resolution files from Pro Photo CD discs.
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def ColorProfileName(self) -> str:
        """
        Read-write. The profile to use when reading the image.
        """
        ...

    @property
    def ColorSpace(self) -> PsPhotoCDColorSpace:
        """
        Read-write. The colorspace for the image.
        """
        ...

    @property
    def Orientation(self) -> PsOrientation:
        """
        Read-write. The image orientation.
        """
        ...

    @property
    def PixelSize(self) -> PsPhotoCDSize:
        """
        Read-write. The image dimensions.
        """
        ...

    @property
    def Resolution(self) -> float:
        """
        Read-write. The image resolution (in pixels per inch).
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced PhotoCDOpenOptions object.
        """
        ...

