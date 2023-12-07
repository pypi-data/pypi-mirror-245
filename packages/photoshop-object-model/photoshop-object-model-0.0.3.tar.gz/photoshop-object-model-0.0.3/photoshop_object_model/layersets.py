
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .layerset import LayerSet
    from .application import Application
    from .document import Document

class LayerSets():
    """
    The collection of LayerSet objects in the document. Note: See “LayerSet ” on page 99 for information on LayerSet objects.
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
        Read-only. The number of elements in the LayerSets collection.
        """
        ...

    @property
    def Parent(self) -> Document|LayerSet:
        """
        Read-only. The LayerSets object's container.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced LayerSets object.
        """
        ...

    def Add(self) -> LayerSet:
        """
        Creates a new LayerSet object.
        """
        ...

    def Index(self, ItemPtr:LayerSet) -> int:
        """
        Gets the index of the LayerSet into the collection.
        """
        ...

    def Item(self, ItemKey:int) -> LayerSet:
        """
        Gets an element from the LayerSets collection.
        """
        ...

    def RemoveAll(self) -> None:
        """
        Removes the layer set, and any layers or layer sets it contains, from the document.
        """
        ...

