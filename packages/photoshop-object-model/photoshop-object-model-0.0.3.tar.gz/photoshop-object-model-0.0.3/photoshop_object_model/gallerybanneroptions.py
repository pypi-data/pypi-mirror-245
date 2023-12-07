
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .application import Application
    from .psgalleryfonttype import PsGalleryFontType

class GalleryBannerOptions():
    """
    Options that define the BannerOptions property of the GalleryOptions object. See ‘GalleryOptions ’ on page 82.Tip: You can preserve default values for many GalleryBannerOptions properties by setting the GalleryOptions property PreserveAllMetadata to true or by choosing File > Automate > Web Photo Gallery , and then choosing Preserve all metadata on the Options area of the Web Photo Gallery dialog. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the collection belongs to.
        """
        ...

    @property
    def ContactInfo(self) -> str:
        """
        Read-write. The Web photo gallery contact info.
        """
        ...

    @property
    def Date(self) -> str:
        """
        Read-write. The Web photo gallery date. Default: current date.
        """
        ...

    @property
    def Font(self) -> PsGalleryFontType:
        """
        Read-write. The font setting for the banner text. Default: 1.
        """
        ...

    @property
    def FontSize(self) -> int:
        """
        Read-write. The font size for the banner text (1 - 7; default: 3).
        """
        ...

    @property
    def Photographer(self) -> str:
        """
        Read-write. The Web photo gallery photographer.
        """
        ...

    @property
    def SiteName(self) -> str:
        """
        Read-write. The Web photo gallery site name. Default: Adobe Web Photo Gallery.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced GalleryBannerOptions object.
        """
        ...

