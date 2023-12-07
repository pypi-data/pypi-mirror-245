
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from pspdfresampletype import PsPDFResampleType
    from pspdfcompatibilitytype import PsPDFCompatibilityType
    from pspdfstandardtype import PsPDFStandardType
    from pspdfencoding import PsPDFEncoding
    from application import Application

class PDFSaveOptions():
    """
    Options that can be specified when saving a document in PDF format. 
    """
    @property
    def AlphaChannels(self) -> bool:
        """
        Read-write. Indicates whether to save the alpha channels with the file.
        """
        ...

    @property
    def Annotations(self) -> bool:
        """
        Read-write. Indicates whether to save comments with the file.
        """
        ...

    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def ColorConversion(self) -> bool:
        """
        Read-write. Indicates whether to convert the color profile to a destination profile.
        """
        ...

    @property
    def ConvertToEightBit(self) -> bool:
        """
        Read-write. Indicates whether to convert a 16-bit image to 8-bit for better compatibility with other applications.
        """
        ...

    @property
    def Descripton(self) -> str:
        """
        Read-write. Description of the save options to use.
        """
        ...

    @property
    def DestinationProfile(self) -> str:
        """
        Read-write. Description of the final RGB or CMYK output device, such as a monitor or a press standard.
        """
        ...

    @property
    def DowngradeColorProfile(self) -> bool:
        """
        Deprecated for Adobe Photoshop.
        """
        ...

    @property
    def DownSample(self) -> PsPDFResampleType:
        """
        Read-write. The down sample method to use.
        """
        ...

    @property
    def DownSampleSize(self) -> float:
        """
        Read-write. The size to downsample images if they exceed the limit in pixels per inch.
        """
        ...

    @property
    def DownSampleSizeLimit(self) -> float:
        """
        Read-write. Limits downsampling or subsampling to images that exceed this value in pixels per inch.
        """
        ...

    @property
    def EmbedColorProfile(self) -> bool:
        """
        Read-write. Indicates whether to embed the color profile in the document.
        """
        ...

    @property
    def EmbedFonts(self) -> bool:
        """
        Deprecated for Adobe Photoshop.
        """
        ...

    @property
    def EmbedThumbnail(self) -> bool:
        """
        Read-write. Indicates whether to include a small preview image in Adobe PDF files.
        """
        ...

    @property
    def Encoding(self) -> PsPDFEncoding:
        """
        Read-write. The encoding method to use. Default: 1 (psPDFZIP).
        """
        ...

    @property
    def Interpolation(self) -> bool:
        """
        Deprecated for Adobe Photoshop.
        """
        ...

    @property
    def JPEGQuality(self) -> int:
        """
        Read-write. The quality of the produced image (0 - 12), which is inversely proportionate to the compression amount. Note:Valid only when Encoding = 2 (psPDFJPEG).
        """
        ...

    @property
    def Layers(self) -> bool:
        """
        Read-write. Indicates whether to save the document’s layers.
        """
        ...

    @property
    def OptimizeForWeb(self) -> bool:
        """
        Read-write. Indicates whether to improve performance of PDF files on Web servers.
        """
        ...

    @property
    def OutputCondition(self) -> str:
        """
        Read-write. An optional comment field for inserting descriptions of the output condition. The text is stored in the PDF/X file.
        """
        ...

    @property
    def OutputConditionID(self) -> str:
        """
        Read-write. Indentifier for the output condition.
        """
        ...

    @property
    def PDFCompatibility(self) -> PsPDFCompatibilityType:
        """
        Read-write. The PDF version to make the document compatible with.
        """
        ...

    @property
    def PDFStandard(self) -> PsPDFStandardType:
        """
        Read-write. The PDF standard to make the document compatible with.
        """
        ...

    @property
    def PreserveEditing(self) -> bool:
        """
        Read-write. Indicates whether to reopen the PDF in Adobe Photoshop with native Photoshop data intact.
        """
        ...

    @property
    def PresetFile(self) -> str:
        """
        Read-write. The preset file to use for settings. Note:This option overrides other settings.
        """
        ...

    @property
    def ProfileInclusionPolicy(self) -> bool:
        """
        Read-write. Indicates whether to show which profiles to include.
        """
        ...

    @property
    def RegistryName(self) -> str:
        """
        Read-write. URL where the output condition is registered.
        """
        ...

    @property
    def SpotColors(self) -> bool:
        """
        Read-write. Indicates whether to save spot colors.
        """
        ...

    @property
    def TileSize(self) -> int:
        """
        Read-write. Compression option. Note:Valid only when encoding = PDFEncoding.JPEG2000.
        """
        ...

    @property
    def Transparency(self) -> bool:
        """
        Deprecated for Adobe Photoshop.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced PDFSaveOptions object.
        """
        ...

    @property
    def UseOutlines(self) -> bool:
        """
        Deprecated for Adobe Photoshop.
        """
        ...

    @property
    def VectorData(self) -> bool:
        """
        Deprecated for Adobe Photoshop.
        """
        ...

    @property
    def View(self) -> bool:
        """
        Read-write. Indicates whether to open the saved PDF in Adobe Acrobat.
        """
        ...

