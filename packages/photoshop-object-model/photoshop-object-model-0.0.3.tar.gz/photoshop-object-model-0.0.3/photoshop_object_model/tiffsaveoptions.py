
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .pslayercompressiontype import PsLayerCompressionType
    from .psbyteorder import PsByteOrder
    from .application import Application
    from .pstiffencodingtype import PsTIFFEncodingType

class TiffSaveOptions():
    """
    Options that can be specified when saving a document in TIFF format. 
    """
    @property
    def AlphaChannels(self) -> bool:
        """
        Read-write. Indicates whether to save the alpha channels.
        """
        ...

    @property
    def Annotations(self) -> bool:
        """
        Read-write. Indicates whether to save the annotations.
        """
        ...

    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def ByteOrder(self) -> PsByteOrder:
        """
        Read-write. The order in which the document’s bytes will be read. The default is 2 (psMacOSByteOrder) when running on Mac OS and 1 (psIBMByteOrder) when running on a PC.
        """
        ...

    @property
    def EmbedColorProfile(self) -> bool:
        """
        Read-write. Indicates whether to embed the color profile in the document.
        """
        ...

    @property
    def ImageCompression(self) -> PsTIFFEncodingType:
        """
        Read-write. The compression type. Default: 1 (psNoTIFFCompression).
        """
        ...

    @property
    def InterleaveChannels(self) -> bool:
        """
        Read-write. Indicates whether the channels in the image will be interleaved.
        """
        ...

    @property
    def JPEGQuality(self) -> int:
        """
        Read-write. The quality of the produced image (0 - 12), which is inversely proportionate to the amount of JPEG compression. Note:Valid only when ImageCompression = 3 (psTiffJPEG).
        """
        ...

    @property
    def LayerCompression(self) -> PsLayerCompressionType:
        """
        Read-write. The method of compression to use when saving layers (as opposed to saving composite data). Note:Valid only when Layers = true. See Layers
        """
        ...

    @property
    def Layers(self) -> bool:
        """
        Read-write. Indicates whether to save the layers.
        """
        ...

    @property
    def SaveImagePyramid(self) -> bool:
        """
        Read-write. Indicates whether to preserve multiresolution information. Default: false.
        """
        ...

    @property
    def SpotColors(self) -> bool:
        """
        Read-write. Indicates whether to save the spot colors.
        """
        ...

    @property
    def Transparency(self) -> bool:
        """
        Read-write. Indicates whether to save the transparency as an additional alpha channel when the file is opened in another application.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced TIFFSaveOptions object.
        """
        ...

