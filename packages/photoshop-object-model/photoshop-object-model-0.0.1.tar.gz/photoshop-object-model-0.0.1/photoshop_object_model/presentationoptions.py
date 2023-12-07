
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from psmagnificationtype import PsMagnificationType
    from pstransitiontype import PsTransitionType
    from application import Application
    from pdfsaveoptions import PDFSaveOptions

class PresentationOptions():
    """
    Options that can be specified for PDF presentations. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def AutoAdvance(self) -> bool:
        """
        Read-write. Indicates whether to auto advance images when viewing the presentation. Default: true. Note:Valid only when Presentation = true. See Presentation.
        """
        ...

    @property
    def IncludeFilename(self) -> bool:
        """
        Read-write. Indicates whether to include the file name for the image (default: false).
        """
        ...

    @property
    def Interval(self) -> int:
        """
        Read-write. The time in seconds before the view is auto advanced (1 - 60; default: 5). Note:Valid only when AutoAdvance = true. See AutoAdvance.
        """
        ...

    @property
    def Loop(self) -> bool:
        """
        Read-write. Indicates whether to begin the presentation again after the last page. Default: false. Note:Valid only when AutoAdvance = true. See AutoAdvance.
        """
        ...

    @property
    def Magnification(self) -> PsMagnificationType:
        """
        Read-write. The magnification type to use when viewing the image.
        """
        ...

    @property
    def PDFFileOptions(self) -> PDFSaveOptions:
        """
        Read-write. Options to use when creating the PDF file.
        """
        ...

    @property
    def Presentation(self) -> bool:
        """
        Read-write. Indicates whether the output will be a presentation. Default: false); when false, the output is a Multi-Page document.
        """
        ...

    @property
    def Transition(self) -> PsTransitionType:
        """
        Read-write. The transition from one image to the next. Default: 9 (psNoTransition). Note:Valid only when AutoAdvance = true. See AutoAdvance.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced PDFPresentationOptions object.
        """
        ...

