from .actiondescriptor import ActionDescriptor
from .actionlist import ActionList
from .actionreference import ActionReference
from .application import Application
from .artlayer import ArtLayer
from .artlayers import ArtLayers
from .batchoptions import BatchOptions
from .bitmapconversionoptions import BitmapConversionOptions
from .bmpsaveoptions import BMPSaveOptions
from .camerarawopenoptions import CameraRAWOpenOptions
from .channel import Channel
from .channels import Channels
from .cmykcolor import CMYKColor
from .colorsampler import ColorSampler
from .colorsamplers import ColorSamplers
from .contactsheetoptions import ContactSheetOptions
from .countitem import CountItem
from .countitems import CountItems
from .dicomopenoptions import DICOMOpenOptions
from .document import Document
from .documentinfo import DocumentInfo
from .documents import Documents
from .epsopenoptions import EPSOpenOptions
from .epssaveoptions import EPSSaveOptions
from .exportoptionsillustrator import ExportOptionsIllustrator
from .exportoptionssaveforweb import ExportOptionsSaveForWeb
from .gallerybanneroptions import GalleryBannerOptions
from .gallerycustomcoloroptions import GalleryCustomColorOptions
from .galleryimagesoptions import GalleryImagesOptions
from .galleryoptions import GalleryOptions
from .gallerysecurityoptions import GallerySecurityOptions
from .gallerythumbnailoptions import GalleryThumbnailOptions
from .gifsaveoptions import GIFSaveOptions
from .graycolor import GrayColor
from .historystate import HistoryState
from .historystates import HistoryStates
from .hsbcolor import HSBColor
from .indexedconversionoptions import IndexedConversionOptions
from .jpegsaveoptions import JPEGSaveOptions
from .labcolor import LabColor
from .layercomp import LayerComp
from .layercomps import LayerComps
from .layers import Layers
from .layerset import LayerSet
from .layersets import LayerSets
from .measurementlog import MeasurementLog
from .measurementscale import MeasurementScale
from .nocolor import NoColor
from .notifier import Notifier
from .notifiers import Notifiers
from .pathitem import PathItem
from .pathitems import PathItems
from .pathpoint import PathPoint
from .pathpointinfo import PathPointInfo
from .pathpoints import PathPoints
from .pdfopenoptions import PDFOpenOptions
from .pdfsaveoptions import PDFSaveOptions
from .photocdopenoptions import PhotoCDOpenOptions
from .photoshopsaveoptions import PhotoshopSaveOptions
from .pictfilesaveoptions import PICTFileSaveOptions
from .picturepackageoptions import PicturePackageOptions
from .pixarsaveoptions import PixarSaveOptions
from .pngsaveoptions import PNGSaveOptions
from .preferences import Preferences
from .presentationoptions import PresentationOptions
from .rawformatopenoptions import RawFormatOpenOptions
from .rawsaveoptions import RawSaveOptions
from .rgbcolor import RGBColor
from .selection import Selection
from .sgirgbsaveoptions import SGIRGBSaveOptions
from .solidcolor import SolidColor
from .subpathinfo import SubPathInfo
from .subpathitem import SubPathItem
from .subpathitems import SubPathItems
from .targasaveoptions import TargaSaveOptions
from .textfont import TextFont
from .textfonts import TextFonts
from .textitem import TextItem
from .tiffsaveoptions import TiffSaveOptions
from .xmpmetadata import XMPMetadata

class PhotoshopObjectModel():
    def __init__(self):
        self.ActionDescriptor = ActionDescriptor()
        self.ActionList = ActionList()
        self.ActionReference = ActionReference()
        self.Application = Application()
        self.ArtLayer = ArtLayer()
        self.ArtLayers = ArtLayers()
        self.BatchOptions = BatchOptions()
        self.BitmapConversionOptions = BitmapConversionOptions()
        self.BMPSaveOptions = BMPSaveOptions()
        self.CameraRAWOpenOptions = CameraRAWOpenOptions()
        self.Channel = Channel()
        self.Channels = Channels()
        self.CMYKColor = CMYKColor()
        self.ColorSampler = ColorSampler()
        self.ColorSamplers = ColorSamplers()
        self.ContactSheetOptions = ContactSheetOptions()
        self.CountItem = CountItem()
        self.CountItems = CountItems()
        self.DICOMOpenOptions = DICOMOpenOptions()
        self.Document = Document()
        self.DocumentInfo = DocumentInfo()
        self.Documents = Documents()
        self.EPSOpenOptions = EPSOpenOptions()
        self.EPSSaveOptions = EPSSaveOptions()
        self.ExportOptionsIllustrator = ExportOptionsIllustrator()
        self.ExportOptionsSaveForWeb = ExportOptionsSaveForWeb()
        self.GalleryBannerOptions = GalleryBannerOptions()
        self.GalleryCustomColorOptions = GalleryCustomColorOptions()
        self.GalleryImagesOptions = GalleryImagesOptions()
        self.GalleryOptions = GalleryOptions()
        self.GallerySecurityOptions = GallerySecurityOptions()
        self.GalleryThumbnailOptions = GalleryThumbnailOptions()
        self.GIFSaveOptions = GIFSaveOptions()
        self.GrayColor = GrayColor()
        self.HistoryState = HistoryState()
        self.HistoryStates = HistoryStates()
        self.HSBColor = HSBColor()
        self.IndexedConversionOptions = IndexedConversionOptions()
        self.JPEGSaveOptions = JPEGSaveOptions()
        self.LabColor = LabColor()
        self.LayerComp = LayerComp()
        self.LayerComps = LayerComps()
        self.Layers = Layers()
        self.LayerSet = LayerSet()
        self.LayerSets = LayerSets()
        self.MeasurementLog = MeasurementLog()
        self.MeasurementScale = MeasurementScale()
        self.NoColor = NoColor()
        self.Notifier = Notifier()
        self.Notifiers = Notifiers()
        self.PathItem = PathItem()
        self.PathItems = PathItems()
        self.PathPoint = PathPoint()
        self.PathPointInfo = PathPointInfo()
        self.PathPoints = PathPoints()
        self.PDFOpenOptions = PDFOpenOptions()
        self.PDFSaveOptions = PDFSaveOptions()
        self.PhotoCDOpenOptions = PhotoCDOpenOptions()
        self.PhotoshopSaveOptions = PhotoshopSaveOptions()
        self.PICTFileSaveOptions = PICTFileSaveOptions()
        self.PicturePackageOptions = PicturePackageOptions()
        self.PixarSaveOptions = PixarSaveOptions()
        self.PNGSaveOptions = PNGSaveOptions()
        self.Preferences = Preferences()
        self.PresentationOptions = PresentationOptions()
        self.RawFormatOpenOptions = RawFormatOpenOptions()
        self.RawSaveOptions = RawSaveOptions()
        self.RGBColor = RGBColor()
        self.Selection = Selection()
        self.SGIRGBSaveOptions = SGIRGBSaveOptions()
        self.SolidColor = SolidColor()
        self.SubPathInfo = SubPathInfo()
        self.SubPathItem = SubPathItem()
        self.SubPathItems = SubPathItems()
        self.TargaSaveOptions = TargaSaveOptions()
        self.TextFont = TextFont()
        self.TextFonts = TextFonts()
        self.TextItem = TextItem()
        self.TiffSaveOptions = TiffSaveOptions()
        self.XMPMetadata = XMPMetadata()
