
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .application import Application
    from .document import Document

class Documents():
    """
    The collection of open Document objects. Note: See ‘Document ’ on page 60 for information on the Document object. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the collection belongs to.
        """
        ...

    @property
    def Count(self) -> int:
        """
        Read-only. The number of elements in the Documents collection.
        """
        ...

    @property
    def Parent(self) -> Application:
        """
        Read-only. The Documents objects’ container.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced Documents object.
        """
        ...

    def Add(self, Width, Height, Resolution, Name, Mode, InitialFill, PixelAspectRatio, BitsPerChannel, ColorProfileName) -> Document:
        """
        Adds a Document Object. PixelAspectRatio: range from 0.100 - 10.00. Default 1.0 for a square aspect ratio. BitsPerChannelType has a default value of 8 (psDocument8Bits).
        """
        ...

    def Index(self, ItemPtr:Document) -> int:
        """
        Gets the index of the Document into the collection.
        """
        ...

    def Item(self, ItemKey:int) -> Document:
        """
        Gets an element from the Documents collection.
        """
        ...

