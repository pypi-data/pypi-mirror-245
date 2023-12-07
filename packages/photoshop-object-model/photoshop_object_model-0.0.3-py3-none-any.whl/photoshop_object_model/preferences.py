
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .psgridsize import PsGridSize
    from .pscolorpicker import PsColorPicker
    from .pspaintingcursors import PsPaintingCursors
    from .pspointtype import PsPointType
    from .psresamplemethod import PsResampleMethod
    from .psunits import PsUnits
    from .pssavelogitemstype import PsSaveLogItemsType
    from .psguidelinestyle import PsGuideLineStyle
    from .psfontpreviewtype import psFontPreviewType
    from .pstypeunits import PsTypeUnits
    from .application import Application
    from .psgridlinestyle import PsGridLineStyle
    from .psquerystatetype import PsQueryStateType
    from .pssavebehavior import PsSaveBehavior
    from .psotherpaintingcursors import PsOtherPaintingCursors
    from .pseditlogitemstype import PsEditLogItemsType

class Preferences():
    """
    Options to define for the Preferences property of the Application object. See ‘Preferences ’ on page 17 (in the Properties table for the Application object).Note: Defining the Preferences properties is basically equivalent to selecting Edit > Preferences (Windows) or Photoshop > Preferences in the Adob e Photoshop application. For explanations of individual settings, please refer to Adobe Photoshop Help. 
    """
    @property
    def AdditionalPluginFolder(self) -> str:
        """
        Read-write. The path to an additional plug-in folder. Note:Valid only when UseAdditionalPluginFolder = true. See UseAdditionalPluginFolder.
        """
        ...

    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def AskBeforeSavingLayeredTIFF(self) -> bool:
        """
        Read-write. Indicates whether to ask the user to verify layer preservation options when saving a file in TIFF format.
        """
        ...

    @property
    def AutoUpdateOpenDocuments(self) -> bool:
        """
        Read-write. Indicates whether to automatically update open documents.
        """
        ...

    @property
    def BeepWhenDone(self) -> bool:
        """
        Read-write. Indicates whether to beep when a process finishes.
        """
        ...

    @property
    def ColorChannelsInColor(self) -> bool:
        """
        Read-write. Indicates whether to display component channels in the Channels palette in color.
        """
        ...

    @property
    def ColorPicker(self) -> PsColorPicker:
        """
        Read-write.
        """
        ...

    @property
    def ColumnGutter(self) -> float:
        """
        Read-write. The width of the column gutters (in points). (0.1 - 600.0).
        """
        ...

    @property
    def ColumnWidth(self) -> float:
        """
        Read-write. Column width (in points) (0.1 - 600.0).
        """
        ...

    @property
    def CreateFirstSnapshot(self) -> bool:
        """
        Read-write. Indicates whether to automatically make the first snapshot when a new document is created.
        """
        ...

    @property
    def DynamicColorSliders(self) -> bool:
        """
        Read-write. Indicates whether dynamic color sliders appear in the Color palette.
        """
        ...

    @property
    def EditLogItems(self) -> PsEditLogItemsType:
        """
        Read-write. The options for editing history log items. Note:Valid only when UseHistoryLog = true. See UseHistoryLog.
        """
        ...

    @property
    def ExportClipboard(self) -> bool:
        """
        Read-write. Indicates whether to retain Adobe Photoshop contents on the clipboard after you exit the application.
        """
        ...

    @property
    def FontPreviewSize(self) -> psFontPreviewType:
        """
        Read-write. Indicates whether to show font previews in the type tool font menus.
        """
        ...

    @property
    def GamutWarningOpacity(self) -> float:
        """
        Read-write. (0 - 100 as percent).
        """
        ...

    @property
    def GridSize(self) -> PsGridSize:
        """
        Read-write. The size to use for squares in the grid.
        """
        ...

    @property
    def GridStyle(self) -> PsGridLineStyle:
        """
        Read-write. The formatting style for non-printing grid lines.
        """
        ...

    @property
    def GridSubDivisions(self) -> int:
        """
        Read-write. (1 - 100)
        """
        ...

    @property
    def GuideStyle(self) -> PsGuideLineStyle:
        """
        Read-write. The formatting style for non-printing guide lines.
        """
        ...

    @property
    def ImageCacheLevels(self) -> int:
        """
        Read-write. The number of images to hold in the cache (1 - 8).
        """
        ...

    @property
    def ImagePreviews(self) -> PsSaveBehavior:
        """
        Read-write. The behavior mode to use when saving files.
        """
        ...

    @property
    def Interpolation(self) -> PsResampleMethod:
        """
        Read-write. The method to use to assign color values to any new pixels created when an image is resampled or resized.
        """
        ...

    @property
    def KeyboardZoomResizesWindows(self) -> bool:
        """
        Read-write. Indicates whether to automatically resize the window when zooming in or out using keyboard shortcuts.
        """
        ...

    @property
    def MaximizeCompatibility(self) -> PsQueryStateType:
        """
        Read-write. The behavior to use to check whether to maximize compatibility when opening Adobe Photoshop (PSD) files.
        """
        ...

    @property
    def MaxRAMuse(self) -> int:
        """
        Read-write. The maximum percentage of available RAM used by Adobe Photoshop (5 - 100).
        """
        ...

    @property
    def NonLinearHistory(self) -> bool:
        """
        Read-write. Indicates whether to allow non-linear history.
        """
        ...

    @property
    def NumberOfHistoryStates(self) -> int:
        """
        Read-write. The number of history states to preserve (1 - 100).
        """
        ...

    @property
    def OtherCursors(self) -> PsOtherPaintingCursors:
        """
        Read-write. The type of pointer to use.
        """
        ...

    @property
    def PaintingCursors(self) -> PsPaintingCursors:
        """
        Read-write. The type of pointer to use.
        """
        ...

    @property
    def Parent(self) -> Application:
        """
        Read-write. The Preferences object's container.
        """
        ...

    @property
    def PixelDoubling(self) -> bool:
        """
        Read-write. Indicates whether to halve the resolution or (double the size of pixels) to make previews display more quickly.
        """
        ...

    @property
    def PointSize(self) -> PsPointType:
        """
        Read-write. The point/pica size.
        """
        ...

    @property
    def RecentFileListLength(self) -> int:
        """
        Read-write. The number of items in the recent file list (0 - 30).
        """
        ...

    @property
    def RulerUnits(self) -> PsUnits:
        """
        Read-write. The unit the scripting system will use when receiving and returning values.
        """
        ...

    @property
    def SaveLogItems(self) -> PsSaveLogItemsType:
        """
        Read-write. The options for saving the history items.
        """
        ...

    @property
    def SaveLogItemsFile(self) -> str:
        """
        Read-write. The path to the history log file.
        """
        ...

    @property
    def SavePaletteLocations(self) -> bool:
        """
        Read-write. Indicates whether to make new palette locations the default location.
        """
        ...

    @property
    def ShowAsianTextOptions(self) -> bool:
        """
        Read-write. Indicates whether to display Asian text options in the Paragraph palette.
        """
        ...

    @property
    def ShowEnglishFontNames(self) -> bool:
        """
        Read-write. Indicates whether to list Asian font names in English.
        """
        ...

    @property
    def ShowSliceNumber(self) -> bool:
        """
        Read-write. Indicates whether to display slice numbers in the document window when using the Slice tool.
        """
        ...

    @property
    def ShowToolTips(self) -> bool:
        """
        Read-write. Indicates whether to show pop up definitions on mouse over.
        """
        ...

    @property
    def SmartQuotes(self) -> bool:
        """
        Read-write. Indicates whether to use curly or straight quote marks.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced Preferences object.
        """
        ...

    @property
    def TypeUnits(self) -> PsTypeUnits:
        """
        Read-write. The unit type-size that the numeric inputs are assumed to represent.
        """
        ...

    @property
    def UseAdditionalPluginFolder(self) -> bool:
        """
        Read-write. Indicates whether to use an additional folder for compatible plug-ins stored with a different application.
        """
        ...

    @property
    def UseHistoryLog(self) -> bool:
        """
        Read-write. Indicates whether to create a log file for history states.
        """
        ...

    @property
    def UseLowerCaseExtension(self) -> bool:
        """
        Read-write. Indicates whether the file extension should be lowercase.
        """
        ...

    @property
    def UseShiftKeyForToolSwitch(self) -> bool:
        """
        Read-write. Indicates whether to enable cycling through a set of hidden tools.
        """
        ...

    @property
    def UseVideoAlpha(self) -> bool:
        """
        Read-write. Indicates whether to enable Adobe Photoshop to send transparency information to your computer’s video board. (Requires hardware support.)
        """
        ...

