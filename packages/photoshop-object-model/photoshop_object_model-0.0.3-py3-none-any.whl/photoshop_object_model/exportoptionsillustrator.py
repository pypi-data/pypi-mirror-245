
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .application import Application
    from .psillustratorpathtype import PsIllustratorPathType

class ExportOptionsIllustrator():
    """
    Options that can be specified when exporting a PathItem object to an Adobe Illustrator® file. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Path(self) -> PsIllustratorPathType:
        """
        Read-write. The type of path to export. Default: 1.
        """
        ...

    @property
    def PathName(self) -> str:
        """
        Read-write. The name of the path to export. Note:Valid only when Path = 3. See Path.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced ExportOptionsIllustrator object.
        """
        ...

