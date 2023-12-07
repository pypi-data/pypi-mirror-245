
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from rgbcolor import RGBColor
    from psgallerysecuritytextrotatetype import PsGallerySecurityTextRotateType
    from application import Application
    from psgalleryfonttype import PsGalleryFontType
    from psgallerysecuritytype import PsGallerySecurityType
    from psgallerysecuritytextpositiontype import PsGallerySecurityTextPositionType

class GallerySecurityOptions():
    """
    Options that define the SecurityOptions property of the GalleryOptions object. See ‘GalleryOptions ’ on page 82.Tip: You can preserve default values for many GallerySecurityOptions properties by setting the GalleryOptions property PreserveAllMetadata to true or by choosing File > Automate > Web Photo Gallery , and then choosing Preserve all metadata on the Options area of the Web Photo Gallery dialog. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the collection belongs to.
        """
        ...

    @property
    def Content(self) -> PsGallerySecurityType:
        """
        Read-write. The Web photo gallery security content. Default: 1.
        """
        ...

    @property
    def Font(self) -> PsGalleryFontType:
        """
        Read-write. The Web photo gallery security font. Default: 1.
        """
        ...

    @property
    def FontSize(self) -> int:
        """
        Read-write. The Web photo gallery security font size (1 - 72; default: 3).
        """
        ...

    @property
    def Opacity(self) -> int:
        """
        Read-write. The Web page security opacity as a percent. Default: 100.
        """
        ...

    @property
    def Text(self) -> str:
        """
        Read-write. The Web photo gallery security custom text.
        """
        ...

    @property
    def TextColor(self) -> RGBColor:
        """
        Read-write. The Web page security text color.
        """
        ...

    @property
    def TextPosition(self) -> PsGallerySecurityTextPositionType:
        """
        Read-write. The Web photo gallery security text position. Default: 1.
        """
        ...

    @property
    def TextRotate(self) -> PsGallerySecurityTextRotateType:
        """
        Read-write. The Web photo gallery security text orientation to use. Default: 1.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced GallerySecurityOptions object.
        """
        ...

