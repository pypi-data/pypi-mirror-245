
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .psgalleryconstraintype import PsGalleryConstrainType
    from .application import Application
    from .psgalleryfonttype import PsGalleryFontType

class GalleryImagesOptions():
    """
    Options that define the ImagesOptions property of the GalleryOptions object. See ‘GalleryOptions ’ on page 82.Tip: You can preserve default values for many GalleryImagesOptions properties by setting the GalleryOptions property PreserveAllMetadata to true or by choosing File > Automate > Web Photo Gallery , and then choosing Preserve all metadata on the Options area of the Web Photo Gallery dialog. 
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
        Read-write. The size (in pixels) of the border that separates images (0 - 99; default: 0).
        """
        ...

    @property
    def Caption(self) -> bool:
        """
        Read-write. Indication of whether to generate image captions. Default: false.
        """
        ...

    @property
    def Dimension(self) -> int:
        """
        Read-write. The resized image dimensions in pixels. Default: 350. Note:Valid only when ResizeImages = true. See ResizeImages.
        """
        ...

    @property
    def Font(self) -> PsGalleryFontType:
        """
        Read-write. The font to use for image captions. Default: 1.
        """
        ...

    @property
    def FontSize(self) -> int:
        """
        Read-write. The font size for image captions (1 - 7; default: 3). Note:Valid only when Caption = true. See Caption.
        """
        ...

    @property
    def ImageQuality(self) -> int:
        """
        Read-write. The quality setting for a JPEG image (0 - 12; default: 5).
        """
        ...

    @property
    def IncludeCopyright(self) -> bool:
        """
        Read-write. Indication of whether to include copyright information in captions. Default: false. Note:Valid only when Caption = true. See Caption.
        """
        ...

    @property
    def IncludeCredits(self) -> bool:
        """
        Read-write. Indication of whether to include the credits in image captions. Default: false. Note:Valid only when Caption = true. See Caption.
        """
        ...

    @property
    def IncludeFilename(self) -> bool:
        """
        Read-write. Indication of whether to include the file name in image captions. Default: true. Note:Valid only when Caption = true. See Caption.
        """
        ...

    @property
    def IncludeTitle(self) -> bool:
        """
        Read-write. Indication of whether to include the title in image captions. Default: false. Note:Valid only when Caption = true. See Caption.
        """
        ...

    @property
    def NumericLinks(self) -> bool:
        """
        Read-write. Indication of whether to add numeric links. Default: true.
        """
        ...

    @property
    def ResizeConstraint(self) -> PsGalleryConstrainType:
        """
        Read-write. The image dimensions to constrain in the gallery image. Default: 3. Note:Valid only when ResizeImages = true. See ResizeImages.
        """
        ...

    @property
    def ResizeImages(self) -> bool:
        """
        Read-write. Indication of whether to automatically resize images for placement on the gallery pages. Default: true.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced GalleryImagesOptions object.
        """
        ...

