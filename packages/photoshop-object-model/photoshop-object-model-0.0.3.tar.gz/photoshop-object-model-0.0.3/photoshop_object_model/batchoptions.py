
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .application import Application
    from .psfilenamingtype import PsFileNamingType
    from .psbatchdestinationtype import PsBatchDestinationType

class BatchOptions():
    """
    Options to specify when running a Batch command. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Destination(self) -> PsBatchDestinationType:
        """
        Read-write. The type of destination for the processed files. Default: 1(psNoDestination).
        """
        ...

    @property
    def DestinationFolder(self) -> str:
        """
        Read-write. The folder location for the processed files. Note:Valid only when Destination = 3 (psFolder). See Destination.
        """
        ...

    @property
    def ErrorFile(self) -> str:
        """
        Read-write. The file in which to log errors encountered. Note:To display errors on the screen (and stop batch processing when errors occur) leave blank.
        """
        ...

    @property
    def FileNaming(self) -> List[PsFileNamingType]:
        """
        Read-write. A list of file naming options (maximum: 6). Note:Valid only when Destination = 3 (psFolder). See Destination.
        """
        ...

    @property
    def MacintoshCompatible(self) -> bool:
        """
        Read-write. Indicates whether to make the final file names Macintosh compatible. Default: true. Note:Valid only when Destination = 3 (psFolder). See Destination.
        """
        ...

    @property
    def OverrideOpen(self) -> bool:
        """
        Read-write. Indicates whether to override action open commands. Default: false.
        """
        ...

    @property
    def OverrideSave(self) -> bool:
        """
        Read-write. Indicates whether to override save as action steps with the specified destination. Default: false. Note:Valid only when Destination = 3 (psFolder). or Destination = 2 (psSaveAndClose). See Destination.
        """
        ...

    @property
    def StartingSerial(self) -> int:
        """
        Read-write. The starting serial number to use in naming files. Default: 1. Note:Valid only when Destination = 3 (psFolder). See Destination.
        """
        ...

    @property
    def SuppressOpen(self) -> bool:
        """
        Read-write. Indicates whether to suppress the file open options dialogs. Default: false.
        """
        ...

    @property
    def SuppressProfile(self) -> bool:
        """
        Read-write. Indicates whether to suppress the color profile warnings. Default: false.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced BatchOptions object.
        """
        ...

    @property
    def UnixCompatible(self) -> bool:
        """
        Read-write. Indicates whether to make the final file name Unix® compatible. Default: true. Note:Valid only when Destination = 3 (psFolder). See Destination.
        """
        ...

    @property
    def WindowsCompatible(self) -> bool:
        """
        Read-write. Indicates whether to make the final file names Windows compatible. Default: true. Note:Valid only when Destination = 3 (psFolder). See Destination.
        """
        ...

