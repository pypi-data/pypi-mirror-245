
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from gallerycustomcoloroptions import GalleryCustomColorOptions
    from galleryimagesoptions import GalleryImagesOptions
    from gallerythumbnailoptions import GalleryThumbnailOptions
    from application import Application
    from gallerybanneroptions import GalleryBannerOptions
    from gallerysecurityoptions import GallerySecurityOptions

class GalleryOptions():
    """
    Options that can be specifie d for a Web photo gallery. Tip: You can preserve default values for many GalleryOptions properties by choosing File > Automate > Web Photo Gallery , and then choosing Preserve all metadata on the Options area of the Web Photo Gallery dialog. 
    """
    @property
    def AddSizeAttributes(self) -> bool:
        """
        Read-write. Indicates whether width and height attributes for images will be added. Default: true.
        """
        ...

    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the collection belongs to.
        """
        ...

    @property
    def BannerOptions(self) -> GalleryBannerOptions:
        """
        Read-write. The options related to banner settings.
        """
        ...

    @property
    def CustomColorOptions(self) -> GalleryCustomColorOptions:
        """
        Read-write. The options related to custom color settings.
        """
        ...

    @property
    def EmailAddress(self) -> str:
        """
        Read-write. The email address to show on the Web page.
        """
        ...

    @property
    def ImagesOptions(self) -> GalleryImagesOptions:
        """
        Read-write. The options related to images settings.
        """
        ...

    @property
    def IncludeSubFolders(self) -> bool:
        """
        Read-write. Indication of whether to include all files found in sub folders of the input folder. Default: true.
        """
        ...

    @property
    def LayoutStyle(self) -> str:
        """
        Read-write. The style to use for laying out the Web page. Default: Centered Frame 1 - Basic.
        """
        ...

    @property
    def PreserveAllMetadata(self) -> bool:
        """
        Read-write. Indicates whether to save metadata. Default: false.
        """
        ...

    @property
    def SecurityOptions(self) -> GallerySecurityOptions:
        """
        Read-write. The options related to security settings.
        """
        ...

    @property
    def ThumbnailOptions(self) -> GalleryThumbnailOptions:
        """
        Read-write. The options related to thumbnail image settings.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced GalleryOptions object.
        """
        ...

    @property
    def UseShortExtension(self) -> bool:
        """
        Read-write. Indicates whether the short Web page extension .htm or Number (Long) Web page extension .html will be used. Default: true.
        """
        ...

    @property
    def UseUTF8Encoding(self) -> bool:
        """
        Read-write. Indicates whether the Web page should use UTF-8 encoding. Default: false.
        """
        ...

