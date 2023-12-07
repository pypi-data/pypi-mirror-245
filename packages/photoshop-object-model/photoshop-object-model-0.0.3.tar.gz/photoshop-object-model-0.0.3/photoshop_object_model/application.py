
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .document import Document
    from .preferences import Preferences
    from .batchoptions import BatchOptions
    from .application import Application
    from .documents import Documents
    from .psjavascriptexecutionmode import PsJavaScriptExecutionMode
    from .notifiers import Notifiers
    from .textfonts import TextFonts
    from .actiondescriptor import ActionDescriptor
    from .contactsheetoptions import ContactSheetOptions
    from .solidcolor import SolidColor
    from .picturepackageoptions import PicturePackageOptions
    from .pspurgetarget import PsPurgeTarget
    from .actionreference import ActionReference
    from .measurementlog import MeasurementLog
    from .psdialogmodes import PsDialogModes

class Application():
    """
    The Adobe Adobe Photoshop application object. The Application object contains all other Adobe Photoshop objects.
    """
    @property
    def ActiveDocument(self) -> Document:
        """
        Read-write. The frontmost document. (Setting this property is equivalent to clicking an open document in the Adobe Photoshop application to bring it to the front of the screen.)
        """
        ...

    @property
    def Application(self):
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def BackgroundColor(self) -> SolidColor:
        """
        Read-write. The color mode for the document’s background color.
        """
        ...

    @property
    def Build(self) -> str:
        """
        Read-only. The build number of the application.
        """
        ...

    @property
    def ColorSettings(self) -> str:
        """
        Read-write. The name of selected color setting’s set.
        """
        ...

    @property
    def CurrentTool(self) -> str:
        """
        Read-write. The name of the current tool selected.
        """
        ...

    @property
    def DisplayDialogs(self) -> PsDialogModes:
        """
        Read-write. The dialog mode for the document, which indicates whether or not Adobe Photoshop displays dialogs when the script runs.
        """
        ...

    @property
    def Documents(self) -> Documents:
        """
        Read-only. The collection of open documents.
        """
        ...

    @property
    def Fonts(self) -> TextFonts:
        """
        Read-only. The fonts installed on this system.
        """
        ...

    @property
    def ForegroundColor(self) -> SolidColor:
        """
        Read-write. The default foreground color (used to paint, fill, and stroke selections).
        """
        ...

    @property
    def FreeMemory(self) -> float:
        """
        Read-only. The amount of unused memory available to Adobe Photoshop.
        """
        ...

    @property
    def Locale(self) -> str:
        """
        Read-only. The language location of the application.
        """
        ...

    @property
    def MacintoshFileTypes(self) -> List[str]:
        """
        Read-only. A list of file image types Adobe Photoshop can open.
        """
        ...

    @property
    def MeasurementLog(self) -> MeasurementLog:
        """
        Read-only. The log of measurements taken.
        """
        ...

    @property
    def Name(self) -> str:
        """
        Read-only. The application's name.
        """
        ...

    @property
    def Notifiers(self) -> Notifiers:
        """
        Read-only. The collection of notifiers currently configured (in the Scripts Events Manager menu in the Adobe Photoshop application).
        """
        ...

    @property
    def NotifiersEnabled(self) -> bool:
        """
        Read-write. Indicates whether all notifiers are enabled or disabled.
        """
        ...

    @property
    def Path(self) -> str:
        """
        Read-only. The full path (as a String) to the location of the Adobe Photoshop application.
        """
        ...

    @property
    def Preferences(self) -> Preferences:
        """
        Read-only. The application preference settings (equivalent to selecting Edit > Preferences in the Adobe Photoshop application in Windows® or Photoshop > Preferences in Mac OS®).
        """
        ...

    @property
    def PreferencesFolder(self) -> str:
        """
        Read-only. The full path to the Preferences folder.
        """
        ...

    @property
    def RecentFiles(self) -> List[str]:
        """
        Read-only. Files (as an Array of String) in the Recent Files list.
        """
        ...

    @property
    def ScriptingBuildDate(self) -> str:
        """
        Read-only. The build date of the Scripting interface.
        """
        ...

    @property
    def ScriptingVersion(self) -> str:
        """
        Read-only. The version of the Scripting interface.
        """
        ...

    @property
    def SystemInformation(self) -> str:
        """
        Read-only. The system information for the applicaiton and the system.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced Application object.
        """
        ...

    @property
    def Version(self) -> str:
        """
        Read-only. The version of Adobe Photoshop application you are running.
        """
        ...

    @property
    def Visible(self) -> bool:
        """
        Read-write. Indicates whether the Adobe Photoshop application is the front-most/active application.
        """
        ...

    @property
    def WinColorSettings(self) -> str:
        """
        Read-only. Color settings.
        """
        ...

    @property
    def WindowsFileTypes(self) -> List[str]:
        """
        Read-only. A list of file image extensions Adobe Photoshop can open.
        """
        ...

    def Batch(self, InputFiles:List[str], Action:str, From:str, Options:BatchOptions) -> str:
        """
        Runs the batch automation routine (similar to the Batch command, or File > Automate > Batch in the Adobe Photoshop application). Note:The inputFiles parameter specifies the source for the files (as an array of String) to be manipulated by the Batch command.
        """
        ...

    def ChangeColorSettings(self, Name:str, File:str) -> None:
        """
        Sets Color Settings to a named set or to the contents of a settings file. The File parameter represents the path to the file as a String.
        """
        ...

    def CharIDToTypeID(self, CharID:str) -> int:
        """
        Converts from a four character code (character ID) to a runtime ID.
        """
        ...

    def DoAction(self, Action:str, From:str) -> None:
        """
        Plays an action from the Actions palette.
        """
        ...

    def DoJavaScript(self, JavaScriptCode:str, Arguments:list, ExecutionMode:PsJavaScriptExecutionMode) -> str:
        """
        Executes the specified JavaScript code.
        """
        ...

    def DoJavaScriptFile(self, JavaScriptFile:str, Arguments:list, ExecutionMode:PsJavaScriptExecutionMode) -> str:
        """
        Executes the specified JavaScript code, from the file specified by argument JavaScriptFile.
        """
        ...

    def ExecuteAction(self, EventID:int, Descriptor:ActionDescriptor, DisplayDialogs:PsDialogModes) -> ActionDescriptor:
        """
        Plays an ActionManager event.
        """
        ...

    def ExecuteActionGet(self, Reference:ActionReference) -> ActionDescriptor:
        """
        Obtains an ActionDescriptor.
        """
        ...

    def FeatureEnabled(self, Name:str) -> bool:
        """
        Determines whether the feature specified by Name is enabled. The following features are supported as values for Name: “photoshop/extend ed” “photoshop/standa rd” “photoshop/trial”
        """
        ...

    def Load(self, Document:str) -> None:
        """
        Loads a support document from the specified file path location.
        """
        ...

    def MakeContactSheet(self, InputFiles:List[str], Options:ContactSheetOptions) -> str:
        """
        Deprecated for Adobe Photoshop. Creates a contact sheet from the specified files.
        """
        ...

    def MakePDFPresentation(self, InputFilesOutputFiles, Options) -> str:
        """
        Deprecated for Adobe Photoshop. Creates a PDF presentation file from the specified input files. Note:The return string contains the path to the PDF file.
        """
        ...

    def MakePhotoGallery(self, InputFolderOutputFolder, Options) -> str:
        """
        Deprecated for Adobe Photoshop. Creates a Web photo gallery from the files in the specified input folder.
        """
        ...

    def MakePhotomerge(self, InputFiles:List[str]) -> str:
        """
        Deprecated for Adobe Photoshop. Merges multiple files into one; user interaction required.
        """
        ...

    def MakePicturePackage(self, InputFiles:List[str], Options:PicturePackageOptions) -> str:
        """
        Deprecated for Adobe Photoshop. Creates a picture package from the specified input files.
        """
        ...

    def Open(self, Document:str, As:Any, AsSmartObject:bool) -> Document:
        """
        Opens the specified document as the optionally specified file type. Optional paramater AsSmartObject (default:false) indicates whether to create a smart object around the opened document.
        """
        ...

    def OpenDialog(self) -> List[str]:
        """
        Uses the Photoshop open dialog box to select files. Returns an Array of String representing the files selected.
        """
        ...

    def Purge(self, Target:PsPurgeTarget) -> None:
        """
        Purges one or more caches.
        """
        ...

    def Quit(self) -> None:
        """
        Quits the Photoshop application.
        """
        ...

    def Refresh(self) -> None:
        """
        Pauses the script while the application refreshes.
        """
        ...

    def StringIDToTypeID(self, StringID:str) -> int:
        """
        Converts from a String ID to a runtime ID.
        """
        ...

    def TypeIDToCharID(self, TypeID:int) -> str:
        """
        Converts from a runtime ID to a character ID.
        """
        ...

    def TypeIDToStringID(self, TypeID:int) -> str:
        """
        Converts from a runtime ID to a String ID.
        """
        ...

