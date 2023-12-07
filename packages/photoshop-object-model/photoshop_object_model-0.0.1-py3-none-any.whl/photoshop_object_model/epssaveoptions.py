
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from pspreviewtype import PsPreviewType
    from application import Application
    from pssaveencoding import PsSaveEncoding

class EPSSaveOptions():
    """
    Options that can be specified when saving a document in EPS format. 
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
        Read-write. Indicates whether to embed the color profile in this document.
        """
        ...

    @property
    def Encoding(self) -> PsSaveEncoding:
        """
        Read-write. The type of encoding to use. Default: 1.
        """
        ...

    @property
    def HalftoneScreen(self) -> bool:
        """
        Read-write. Indicates whether to include the halftone screen. Default: false.
        """
        ...

    @property
    def Interpolation(self) -> bool:
        """
        Read-write. Indicates whether to use image interpolation. Default: false.
        """
        ...

    @property
    def Preview(self) -> PsPreviewType:
        """
        Read-write. The preview type.
        """
        ...

    @property
    def PsColorManagement(self) -> bool:
        """
        Read-write. Indicates whether to use Postscript color management. Default: false.
        """
        ...

    @property
    def TransferFunction(self) -> bool:
        """
        Read-write. Indicates whether to include the Transfer functions to compensate for dot gain between the image and film. Default: false.
        """
        ...

    @property
    def TransparentWhites(self) -> bool:
        """
        Read-write. Indicates whether to display white areas as transparent. Note:Valid only when Document.Mode = 5. See ‘Mode’ on page 61 (in the Properties table of the Document object) or ‘ChangeMode’ on page 63 (in the Methods table of the Document object).
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced EPSSaveOptions object.
        """
        ...

    @property
    def VectorData(self) -> bool:
        """
        Read-write. Indicates whether to include vector data. Note:Valid only if the document includes vector data (text).
        """
        ...

