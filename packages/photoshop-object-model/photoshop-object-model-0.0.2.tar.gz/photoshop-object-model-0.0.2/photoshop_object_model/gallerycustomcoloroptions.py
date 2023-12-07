
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from rgbcolor import RGBColor
    from application import Application

class GalleryCustomColorOptions():
    """
    Options that define the customColorOptions property of the GalleryOptions object. See ‘GalleryOptions ’ on page 82.Tip: You can preserve default values for many GalleryCustomColorOptions properties by setting the GalleryOptions property PreserveAllMetadata to true or by choosing File > Automate > Web Photo Gallery , and then choosing Preserve all metadata on the Options area of the Web Photo Gallery dialog. 
    """
    @property
    def ActiveLinkColor(self) -> RGBColor:
        """
        Read-write. The color to use to indicate an active link.
        """
        ...

    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the collection belongs to.
        """
        ...

    @property
    def BackgroundColor(self) -> RGBColor:
        """
        Read-write. The background color.
        """
        ...

    @property
    def BannerColor(self) -> RGBColor:
        """
        Read-write. The banner color.
        """
        ...

    @property
    def LinkColor(self) -> RGBColor:
        """
        Read-write. The color to use to indicate a link.
        """
        ...

    @property
    def TextColor(self) -> RGBColor:
        """
        Read-write. The text color.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced GalleryCustomColorOptions object.
        """
        ...

    @property
    def VisitedLinkColor(self) -> RGBColor:
        """
        Read-write. The color to use to indicate a visited link.
        """
        ...

