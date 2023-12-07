
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .rgbcolor import RGBColor
    from .application import Application
    from .psgallerysecuritytextrotatetype import PsGallerySecurityTextRotateType
    from .psgallerysecuritytextpositiontype import PsGallerySecurityTextPositionType
    from .psnewdocumentmode import PsNewDocumentMode
    from .psgalleryfonttype import PsGalleryFontType
    from .pspicturepackagetexttype import PsPicturePackageTextType

class PicturePackageOptions():
    """
    Options that can be specified for a Picture Package.
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Content(self) -> PsPicturePackageTextType:
        """
        Read-write. The content information. Default: 0 (psNoText).
        """
        ...

    @property
    def Flatten(self) -> bool:
        """
        Read-write. Indicates whether all layers in the final document are flattened. Default: true.
        """
        ...

    @property
    def Font(self) -> PsGalleryFontType:
        """
        Read-write. The font used for security text. Default: 1 (psArial).
        """
        ...

    @property
    def FontSize(self) -> int:
        """
        Read-write. The font size used for security text. Default: 12.
        """
        ...

    @property
    def Layout(self) -> str:
        """
        Read-write. The layout to use to generate the picture package. Default: “(2)5x7”.
        """
        ...

    @property
    def Mode(self) -> PsNewDocumentMode:
        """
        Read-write. Read-write. The color profile to use as the document mode. Default: 2 (psNewRGB).
        """
        ...

    @property
    def Opacity(self) -> int:
        """
        Read-write. The Web page security opacity as a percent. Default: 100.
        """
        ...

    @property
    def Resolution(self) -> float:
        """
        Read-write. The resolution of the document in pixels per inch. Default: 72.0.
        """
        ...

    @property
    def Text(self) -> str:
        """
        Read-write. The picture package custom text. Note:Valid only when Content = 2 (psUserText). See Content.
        """
        ...

    @property
    def TextColor(self) -> RGBColor:
        """
        Read-write. The color to use for security text.
        """
        ...

    @property
    def TextPosition(self) -> PsGallerySecurityTextPositionType:
        """
        Read-write. The security text position. Default: 1 (psCentered).
        """
        ...

    @property
    def TextRotate(self) -> PsGallerySecurityTextRotateType:
        """
        Read-write. The orientation to use for security text. Default: 1 (psZero).
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced PicturePackageOptions object.
        """
        ...

