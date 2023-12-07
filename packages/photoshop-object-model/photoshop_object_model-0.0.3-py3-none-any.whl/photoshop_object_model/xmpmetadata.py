
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .application import Application
    from .document import Document

class XMPMetadata():
    """
    Camera raw image file settings stored in an XMP file in the same folder as the raw file with the same base name and an XMP extension.
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Parent(self) -> Document:
        """
        Read-only. The object's container.
        """
        ...

    @property
    def RawData(self) -> str:
        """
        Read-write. The raw XML form of file information.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced XMPMetadata object.
        """
        ...

