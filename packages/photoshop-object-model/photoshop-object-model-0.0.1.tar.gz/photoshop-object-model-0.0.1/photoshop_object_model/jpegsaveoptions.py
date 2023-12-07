
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from psformatoptionstype import PsFormatOptionsType
    from application import Application
    from psmattetype import PsMatteType

class JPEGSaveOptions():
    """
    Options that can be specified when saving a document in JPEG format. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def EmbedColorProfile(self) -> bool:
        """
        Read-write. Indicates whether to embed the color profile in the document.
        """
        ...

    @property
    def FormatOptions(self) -> PsFormatOptionsType:
        """
        Read-write.The download format to use. Default: 1 (psStandardBaseline).
        """
        ...

    @property
    def Matte(self) -> PsMatteType:
        """
        Read-write. The color to use to fill antialiased edges adjacent to transparent areas of the image. Default: 4 (psWhiteMatte). Note:When Transparency = false, the matte color is applied to transparent areas. See Transparency.
        """
        ...

    @property
    def Quality(self) -> int:
        """
        Read-write. The image quality setting to use (affects file size and compression) (0 - 12; default: 3).
        """
        ...

    @property
    def Scans(self) -> int:
        """
        Read-write. The number of scans to make to incrementally display the image on the page (3 - 5; default: 3). Note:Valid only for when FormatOptions = 3 (psProgressive).
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced JPEGSaveOptions object.
        """
        ...

