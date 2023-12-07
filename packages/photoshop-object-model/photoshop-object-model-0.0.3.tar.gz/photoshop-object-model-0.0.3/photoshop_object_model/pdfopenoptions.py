
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .psbitsperchanneltype import PsBitsPerChannelType
    from .pscroptotype import PsCropToType
    from .double import Double
    from .application import Application
    from .psopendocumentmode import PsOpenDocumentMode

class PDFOpenOptions():
    """
    Options that can be specified when open ing a document in generic PDF format. 
    """
    @property
    def AntiAlias(self) -> bool:
        """
        Read-write. Indicates whether to use antialias.
        """
        ...

    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def BitsPerChannel(self) -> PsBitsPerChannelType:
        """
        Read-write. The number of bits per channel.
        """
        ...

    @property
    def ConstrainProportions(self) -> bool:
        """
        Deprecated for Adobe Photoshop.
        """
        ...

    @property
    def CropPage(self) -> PsCropToType:
        """
        Read-write. The method of cropping to use.
        """
        ...

    @property
    def Height(self) -> Double:
        """
        Deprecated for Adobe Photoshop.
        """
        ...

    @property
    def Mode(self) -> PsOpenDocumentMode:
        """
        Read-write. The color model to use.
        """
        ...

    @property
    def Name(self) -> str:
        """
        Read-write. The name of the document.
        """
        ...

    @property
    def Object(self) -> int:
        """
        Read-write. The number of 3d objects to open.
        """
        ...

    @property
    def Page(self) -> int:
        """
        Read-write. The page to which to open the document.
        """
        ...

    @property
    def Resolution(self) -> float:
        """
        Read-write. The resolution of the document (in pixels per inch).
        """
        ...

    @property
    def SuppressWarnings(self) -> bool:
        """
        Read-write. Indicates whether to suppress warnings when opening the document.
        """
        ...

    @property
    def Typename(self) -> str:
        """
        Read-only. The class name of the referenced PDFOpenOptions object.
        """
        ...

    @property
    def Use3DObjectNumber(self) -> bool:
        """
        Read-write. If true, the 3d property refers to using 3d object; if false, then UsePageNumber is used.
        """
        ...

    @property
    def UsePageNumber(self) -> bool:
        """
        Read-write. Indicates whether the value specified in the page property will refer to an image number when usePageNumber = false. See Page.
        """
        ...

    @property
    def Width(self) -> Double:
        """
        Deprecated for Adobe Photoshop.
        """
        ...

