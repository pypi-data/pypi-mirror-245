
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from psnewdocumentmode import PsNewDocumentMode
    from application import Application
    from psgalleryfonttype import PsGalleryFontType

class ContactSheetOptions():
    """
    Options that can be specified for a contact sheet. 
    """
    @property
    def AcrossFirst(self) -> bool:
        """
        Read-write. Indicates whether to place the images horizontally (left to right, then top to bottom) first. Default: true.
        """
        ...

    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def BestFit(self) -> bool:
        """
        Read-write. Indicates whether to rotate images for the best fit. Default: false.
        """
        ...

    @property
    def Caption(self) -> bool:
        """
        Read-write. Indicates whether to use the filename as a caption for the image. Default: true.
        """
        ...

    @property
    def ColumnCount(self) -> int:
        """
        Read-write. The number of columns to include (1 - 100; default: 5).
        """
        ...

    @property
    def Flatten(self) -> bool:
        """
        Read-write. Indicates whether to flatten all layers in the final document. Default: true.
        """
        ...

    @property
    def Font(self) -> PsGalleryFontType:
        """
        Read-write. The font used for the caption. Default: 1.
        """
        ...

    @property
    def FontSize(self) -> int:
        """
        Read-write. The font size to use for the caption. Default: 12.
        """
        ...

    @property
    def Height(self) -> int:
        """
        Read-write. The height (in pixels) of the resulting document (100 - 2900; default: 720).
        """
        ...

    @property
    def Horizontal(self) -> int:
        """
        Read-write. The horizontal spacing (in pixels) between images (0 - 29000; default: 1).
        """
        ...

    @property
    def Mode(self) -> PsNewDocumentMode:
        """
        Read-write. The document color mode. Default: 2 (psNewRGB).
        """
        ...

    @property
    def Resolution(self) -> float:
        """
        Read-write. The resolution of the document in pixels per inch (35 - 1200; default: 72.0).
        """
        ...

    @property
    def RowCount(self) -> int:
        """
        Read-write. The number of rows to use (1 - 100; default: 6).
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced ContactSheetOptions object.
        """
        ...

    @property
    def UseAutoSpacing(self) -> bool:
        """
        Read-write. Indicates whether to auto space the images. Default: true.
        """
        ...

    @property
    def Vertical(self) -> int:
        """
        Read-write. The vertical spacing (in pixels) between images (0 - 29000; default: 1). Note:Valid only when UseAutoSpacing = false.
        """
        ...

    @property
    def Width(self) -> int:
        """
        Read-write. The width (in pixels) of the resulting document (100 - 2900; default: 576).
        """
        ...

