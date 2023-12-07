
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from psgallerythumbsizetype import PsGalleryThumbSizeType
    from application import Application
    from psgalleryfonttype import PsGalleryFontType

class GalleryThumbnailOptions():
    """
    Options that define the thumbnailOptions property of the GalleryOptions object. See ‘GalleryOptions ’ on page 82.Tip: You can preserve default values for many GalleryThumbnailOptions properties by setting the GalleryOptions property PreserveAllMetadata to true or by choosing File > Automate > Web Photo Gallery , and then choosing Preserve all metadata on the Options area of the Web Photo Gallery dialog. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the collection belongs to.
        """
        ...

    @property
    def Border(self) -> int:
        """
        Read-write. The amount of border pixels you want around your thumbnail images (0 - 99; default: 0).
        """
        ...

    @property
    def Caption(self) -> bool:
        """
        Read-write. Indicates whether there is a caption. Default: false.
        """
        ...

    @property
    def ColumnCount(self) -> int:
        """
        Read-write. The number of columns on the page. Default: 5.
        """
        ...

    @property
    def Dimension(self) -> int:
        """
        Read-write. The Web photo gallery thumbnail dimension in pixels. Default: 75.
        """
        ...

    @property
    def Font(self) -> PsGalleryFontType:
        """
        Read-write. The Web photo gallery font. Default: 1.
        """
        ...

    @property
    def FontSize(self) -> int:
        """
        Read-write. The font size for thumbnail images text (1 - 7; default: 3).
        """
        ...

    @property
    def IncludeCopyright(self) -> bool:
        """
        Read-write. Indication of whether to include copyright information for thumbnails. Default: false.
        """
        ...

    @property
    def IncludeCredits(self) -> bool:
        """
        Read-write. Indication of whether to include credits for thumbnails. Default: false.
        """
        ...

    @property
    def IncludeFilename(self) -> bool:
        """
        Read-write. Indication of whether to include file names for thumbnails. Default: false.
        """
        ...

    @property
    def IncludeTitle(self) -> bool:
        """
        Read-write. Indication of whether to include titles for thumbnails. Default: false.
        """
        ...

    @property
    def RowCount(self) -> int:
        """
        Read-write. The number of rows on the page. Default: 3.
        """
        ...

    @property
    def Size(self) -> PsGalleryThumbSizeType:
        """
        Read-write. The thumbnail image size. Default: 2.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced GalleryThumbnailOptions object.
        """
        ...

