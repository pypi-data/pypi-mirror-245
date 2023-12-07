
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from application import Application
    from nothing import Nothing
    from artlayer import ArtLayer
    from document import Document

class ArtLayers():
    """
    The collection of ArtLayer objects in the document. 
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
        Read-only. The number of elements in the ArtLayers collection.
        """
        ...

    @property
    def Parent(self) -> Document:
        """
        Read-only. The object's container.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced ArtLayers object.
        """
        ...

    def Add(self) -> ArtLayer:
        """
        Creates a new ArtLayer in the document.
        """
        ...

    def Index(self, ItemPtr:ArtLayer) -> int:
        """
        Gets the index of the ArtLayer into the collection.
        """
        ...

    def Item(self, ItemKey:int) -> ArtLayer:
        """
        Gets an element from the ArtLayers collection.
        """
        ...

    def RemoveAll(self) -> Nothing:
        """
        Removes all elements from the ArtLayers collection.
        """
        ...

