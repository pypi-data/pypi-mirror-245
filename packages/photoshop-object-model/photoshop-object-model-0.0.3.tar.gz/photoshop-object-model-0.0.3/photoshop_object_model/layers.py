
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .layerset import LayerSet
    from .application import Application
    from .document import Document
    from .artlayer import ArtLayer

class Layers():
    """
    The collection of layer objects, including ArtLayer and LayerSet objects, in the document. Note: See “ArtLayer ” on page 24 for information on ArtLayer objects. See “LayerSet ” on page 99 for information on LayerSet objects.
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
        Read-only. The number of elements in the Layers collection.
        """
        ...

    @property
    def Parent(self) -> Document|LayerSet:
        """
        Read-only. The Layers object's container.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced Layers object.
        """
        ...

    def Index(self, ItemPtr:ArtLayer|LayerSet) -> int:
        """
        Gets the index of the ArtLayer or LayerSet into the collection.
        """
        ...

    def Item(self, ItemKey:int) -> ArtLayer|LayerSet:
        """
        Gets an element from the collection.
        """
        ...

    def RemoveAll(self) -> None:
        """
        Removes all layers from the collection.
        """
        ...

