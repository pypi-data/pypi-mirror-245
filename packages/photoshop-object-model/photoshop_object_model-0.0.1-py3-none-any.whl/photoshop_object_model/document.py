
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from documentinfo import DocumentInfo
    from pathitems import PathItems
    from layers import Layers
    from psanchorposition import PsAnchorPosition
    from artlayer import ArtLayer
    from application import Application
    from layercomps import LayerComps
    from channel import Channel
    from layerset import LayerSet
    from measurementscale import MeasurementScale
    from psdirection import PsDirection
    from artlayers import ArtLayers
    from layersets import LayerSets
    from pssaveoptions import PsSaveOptions
    from selection import Selection
    from countitems import CountItems
    from psbitsperchanneltype import PsBitsPerChannelType
    from historystate import HistoryState
    from colorsamplers import ColorSamplers
    from document import Document
    from psdocumentmode import PsDocumentMode
    from psextensiontype import PsExtensionType
    from arraydouble import arrayDouble
    from channels import Channels
    from pscolorprofiletype import PsColorProfileType
    from xmpmetadata import XMPMetadata
    from historystates import HistoryStates

class Document():
    """
    The active containment object for layers and all most objects in the script; the basic canvas for the file. Note: In Adobe Photoshop, a document can also be referred to as an image or a canvas. ?The term image refers to the entire document and its contents. You can trim or crop an image. You resize an image using the ResizeImage() method. ?The term canvas refers to the space in which the document sits on the screen. You can rotate or flip the canvas. You resize the canvas using the ResizeCanvas() method. 
    """
    @property
    def ActiveChannels(self) -> List[Channel]:
        """
        Read-write. The selected channels.
        """
        ...

    @property
    def ActiveHistoryBrushSource(self) -> HistoryState:
        """
        Read-write. The history state to use with the history brush.
        """
        ...

    @property
    def ActiveHistoryState(self) -> HistoryState:
        """
        Read-write. The selected HistoryState object.
        """
        ...

    @property
    def ActiveLayer(self) -> ArtLayer|LayerSet:
        """
        Read-write. The selected layer.
        """
        ...

    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def ArtLayers(self) -> ArtLayers:
        """
        Read-only. The ArtLayers collection.
        """
        ...

    @property
    def BackgroundLayer(self) -> ArtLayer:
        """
        Read-only. The background layer of the document.
        """
        ...

    @property
    def BitsPerChannel(self) -> PsBitsPerChannelType:
        """
        Read-write. The number of bits per channel.
        """
        ...

    @property
    def Channels(self) -> Channels:
        """
        Read-only. The Channels collection.
        """
        ...

    @property
    def ColorProfileName(self) -> str:
        """
        Read-write. The name of the color profile. Note:Valid only when ColorProfileType = 3 or ColorProfileType = 2. See ColorProfileType.
        """
        ...

    @property
    def ColorProfileType(self) -> PsColorProfileType:
        """
        Read-write. The type of color model that defines the document’s working space.
        """
        ...

    @property
    def ColorSamplers(self) -> ColorSamplers:
        """
        Read-only. The current color samplers associated with this document.
        """
        ...

    @property
    def ComponentChannels(self) -> List[Channel]:
        """
        Read-only. A list of the component color channels.
        """
        ...

    @property
    def CountItems(self) -> CountItems:
        """
        Read-only. The current count items. Note:For additional information about count items, see Adobe Photoshop help on the Coun Tool.
        """
        ...

    @property
    def FullName(self) -> str:
        """
        Read-only. The full path name of the document.
        """
        ...

    @property
    def Height(self) -> float:
        """
        Read-only. The height of the document (unit value).
        """
        ...

    @property
    def Histogram(self) -> List[int]:
        """
        Read-only. A histogram showing the number of pixels at each color intensity level for the composite channel. Note:Valid only when Mode = 2; Mode = 3; or Mode = 6. See Mode.
        """
        ...

    @property
    def HistoryStates(self) -> HistoryStates:
        """
        Read-only. The HistoryStates collection.
        """
        ...

    @property
    def Info(self) -> DocumentInfo:
        """
        Read-only. Metadata about the document.
        """
        ...

    @property
    def LayerComps(self) -> LayerComps:
        """
        Read-only. The LayerComps collection.
        """
        ...

    @property
    def Layers(self) -> Layers:
        """
        Read-only. The Layers collection.
        """
        ...

    @property
    def LayerSets(self) -> LayerSets:
        """
        Read-only. The LayerSets collection.
        """
        ...

    @property
    def Managed(self) -> bool:
        """
        Read-only. Indicates whether the document a is workgroup document.
        """
        ...

    @property
    def MeasurementScale(self) -> MeasurementScale:
        """
        Read-only. The measurement scale for the document. Note:This feature is available in the Extended Version only.
        """
        ...

    @property
    def Mode(self) -> PsDocumentMode:
        """
        Read-only. The color profile.
        """
        ...

    @property
    def Name(self) -> str:
        """
        Read-only. The document's name.
        """
        ...

    @property
    def Parent(self) -> Application:
        """
        Read-only. The Document object's container.
        """
        ...

    @property
    def Path(self) -> str:
        """
        Read-only. The path to the document.
        """
        ...

    @property
    def PathItems(self) -> PathItems:
        """
        Read-only. The PathItems collection.
        """
        ...

    @property
    def PixelAspectRatio(self) -> float:
        """
        Read-write. The (custom) pixel aspect ratio to use (0.100 - 10.000).
        """
        ...

    @property
    def QuickMaskMode(self) -> bool:
        """
        Read-write. Indicates whether the document is in Quick Mask mode.
        """
        ...

    @property
    def Resolution(self) -> float:
        """
        Read-only. The document’s resolution (in pixels per inch).
        """
        ...

    @property
    def Saved(self) -> bool:
        """
        Read-only. Indicates whether the document has been saved since the last change.
        """
        ...

    @property
    def Selection(self) -> Selection:
        """
        Read-only. The selected area of the document.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the Document object.
        """
        ...

    @property
    def Width(self) -> float:
        """
        Read-only. The width of the document (unit value).
        """
        ...

    @property
    def XMPMetadata(self) -> XMPMetadata:
        """
        Read-only. XMP data for the image. Camera Raw settings are contained here.
        """
        ...

    def AutoCount(self, channel, threshold) -> None:
        """
        Counts the number of objects in a document. Creates a CountItem object for each object counted. Note:The AutoCount feature is available in the Extended Version only. For additional information about how to set up objects to count, please see the Count Tool in the Adobe Photoshop Help
        """
        ...

    def ChangeMode(self, DestinationMode, Options) -> None:
        """
        Changes the color profile.
        """
        ...

    def Close(self, Saving:PsSaveOptions) -> None:
        """
        Closes the document. If any changes have been made, the script presents an alert with three options: save, do not save, prompt to save. The optional parameter specifies a selection in the alert box. Default: 3 (psPromptToSaveChange s).
        """
        ...

    def ConvertProfile(self, DestinationProfile, Intent, BlackPointCompensation, Dither) -> None:
        """
        Changes the color profile. Note:The DestinationProfi le parameter must be either a string that names the color mode or Working RGB, Working CMYK, Working Gray, Lab Color (meaning one of the working color spaces or Lab color)
        """
        ...

    def Crop(self, Bounds:arrayDouble, Angle:float, Width:float, Height:float) -> None:
        """
        Crops the document. The first parameter is an array of four coordinates that mark the portion remaining after cropping, in the following order: left, top, right, bottom.
        """
        ...

    def Duplicate(self, Name:str, MergeLayersOnly:bool):
        """
        Creates a duplicate of the Document object. The optional parameter Name provides the name for the duplicated document. The optional parameter MergeLayersOnly indicates whether to only duplicate merged layers.
        """
        ...

    def ExportDocument(self, ExportIn, ExportAs, Options) -> None:
        """
        Exports the document. Note:The ExportIn parameter represents the path to a file as String.
        """
        ...

    def Flatten(self) -> None:
        """
        Flattens all layers.
        """
        ...

    def FlipCanvas(self, Direction:PsDirection) -> None:
        """
        Flips the image within the canvas in the specified direction.
        """
        ...

    def ImportAnnotations(self, File:str) -> None:
        """
        Imports annotations into the document.
        """
        ...

    def MergeVisibleLayers(self) -> None:
        """
        Flattens all visible layers in the document.
        """
        ...

    def Paste(self, IntoSelection:bool) -> ArtLayer:
        """
        Pastes the contents of the clipboard into the document. If the optional argument is set to true and a selection is active, the contents are pasted into the selection.
        """
        ...

    def PrintOut(self, SourceSpace, PrintSpace, IntentBlackPointCompensation) -> None:
        """
        Prints the document. Note: PrintSpace specifies the color space for the printer. Valid values are nothing (that is, the same as the source); or Working RGB, Working CMYK, Working Gray, Lab Color (meaning one of the working color spaces or Lab color); or a string specifying a specific colorspace. Default: nothing).
        """
        ...

    def RasterizeAllLayers(self) -> None:
        """
        Rasterizes all layers.
        """
        ...

    def RecordMeasurements(self, Source, DataPoints) -> None:
        """
        Record measurements of document.
        """
        ...

    def ResizeCanvas(self, Width:float, Height:float, Anchor:PsAnchorPosition) -> None:
        """
        Changes the size of the canvas to display more or less of the image but does not change the image size. See ResizeImage.
        """
        ...

    def ResizeImage(self, Width, Height, Resolution, ResampleMethod, Amount) -> None:
        """
        Changes the size of the image.
        """
        ...

    def RevealAll(self) -> None:
        """
        Expands the document to show clipped sections.
        """
        ...

    def RotateCanvas(self, Angle:float) -> None:
        """
        Rotates the canvas (including the image) in clockwise direction.
        """
        ...

    def Save(self) -> None:
        """
        Saves the document.
        """
        ...

    def SaveAs(self, SaveIn:str, Options:Any, AsCopy:bool, ExtensionType:PsExtensionType) -> None:
        """
        Saves the document with specified save options. Note:The Options parameter’s value can be a value from the PsSaveDocumentType constant list, or any of the “SaveOptions” objects in the current chapter such as BMPSaveOptions, EPSSaveOptions, JPEGSaveOptions, and so on. Note:The SaveIn parameter represents the path to the file to save in as String.
        """
        ...

    def SplitChannels(self) -> List[Document]:
        """
        Splits the document channels into separate images.
        """
        ...

    def Trap(self, Width:int) -> None:
        """
        Applies trapping to a CMYK document. Note:Valid only when Mode = 3. See Mode.
        """
        ...

    def Trim(self, Type, Top, Left, Bottom, Right) -> None:
        """
        Trims the transparent area around the image on the specified sides of the canvas. Note:Default is true for all Boolean values.
        """
        ...

