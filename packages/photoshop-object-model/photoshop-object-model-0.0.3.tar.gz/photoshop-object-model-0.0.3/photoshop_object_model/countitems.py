
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .document import Document
    from .psdcstype import PsDCSType
    from .pssaveencoding import PsSaveEncoding
    from .application import Application
    from .countitem import CountItem
    from .pspreviewtype import PsPreviewType

class CountItems():
    """
    The collection of CountItems objects in the document. See CountItem.Note:CountItems is available in the Extended Version only.
    """
    @property
    def Length(self) -> int:
        """
        Read-only. The number of elements in the CountItems collection.
        """
        ...

    @property
    def Parent(self) -> Document:
        """
        Read-only. The CountItems object’s container.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced CountItems object.
        """
        ...

    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def DCS(self) -> PsDCSType:
        """
        Read-write. Default: 3.
        """
        ...

    @property
    def EmbedColorProfile(self) -> bool:
        """
        Read-write. Indicates whether to embed the color profile in the document
        """
        ...

    @property
    def Encoding(self) -> PsSaveEncoding:
        """
        Read-write. The type of encoding to use for document. Default: 1.
        """
        ...

    @property
    def HalftoneScreen(self) -> bool:
        """
        Read-write. Indicates whether to include halftone screen. Default: false.
        """
        ...

    @property
    def Interpolation(self) -> bool:
        """
        Read-write. Indicates whether to use image interpolation. Default: false)
        """
        ...

    @property
    def Preview(self) -> PsPreviewType:
        """
        Read-write. The type of preview. Default: 3.
        """
        ...

    @property
    def TransferFunction(self) -> bool:
        """
        Read-write. Indicates whether to include the Transfer functions to compensate for dot gain between the image and film. Default: false.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced DCS1_SaveOptions object.
        """
        ...

    @property
    def VectorData(self) -> bool:
        """
        Read-write. Indicates whether to include vector data. Note:Valid only if the document includes vector data (un-rasterized text).
        """
        ...

    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def DCS(self) -> PsDCSType:
        """
        Read-write. The type of composite file to create. Default: 1.
        """
        ...

    @property
    def EmbedColorProfile(self) -> bool:
        """
        Read-write. Indicates whether to embed the color profile in the document.
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
    def MultiFileDCS(self) -> bool:
        """
        Read-write. Indicates whether to save color channels as multiple files or a single file. Default: false.
        """
        ...

    @property
    def Preview(self) -> PsPreviewType:
        """
        Read-write. The preview type. Default: 3.
        """
        ...

    @property
    def SpotColors(self) -> bool:
        """
        Read-write. Indicates whether to save spot colors.
        """
        ...

    @property
    def TransferFunction(self) -> bool:
        """
        Read-write. Indicates whether to include the Transfer functions to compensate for dot gain between the image and film. Default: false.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced DCS2_SaveOptions object.
        """
        ...

    @property
    def VectorData(self) -> bool:
        """
        Read-write. Indicates whether to include vector data. Note:Valid only if the document includes vector data (un-rasterized text).
        """
        ...

    def Add(self, position:List[float]) -> CountItem:
        """
        Creates a new CountItem object. Parameter position (x,y) represents the horizontal and vertical positions, respectively, of the new CountItem object.
        """
        ...

    def Index(self, ItemPtr:CountItem) -> int:
        """
        Gets the index of the CountItem into the collection.
        """
        ...

    def Item(self, ItemKey:int) -> Document:
        """
        Gets an element from the CountItem collection.
        """
        ...

    def RemoveAll(self) -> None:
        """
        Removes all CountItem objects from the CountItem collection.
        """
        ...

