
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .application import Application

class PNGSaveOptions():
    """
    Options that can be specified when saving a document in PNG format. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Compression(self) -> int:
        """
        Read-write. The compression of the image (0 - 9), Default: 0.
        """
        ...

    @property
    def Interlaced(self) -> bool:
        """
        Read-write. Indicates whether the should rows be interlaced. Default: false.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced PNGSaveOptions object.
        """
        ...

