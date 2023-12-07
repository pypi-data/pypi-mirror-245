
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from layercomp import LayerComp
    from application import Application
    from document import Document

class LayerComps():
    """
    The collection of LayerComp objects in the document. Note: See “LayerComp ” on page 96 for information on LayerComp objects.
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
        Read-only. The number of elements in the LayerComps collection.
        """
        ...

    @property
    def Parent(self) -> Document:
        """
        Read-only. The LayerComps object's container.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced LayerComps object.
        """
        ...

    def Add(self, Name:str, Comment:str, Appearance:bool, Position:bool, Visibility:bool) -> LayerComp:
        """
        Adds a layer comp.
        """
        ...

    def Index(self, ItemPtr:LayerComp) -> int:
        """
        Gets the index of the LayerComp into the collection.
        """
        ...

    def Item(self, ItemKey:int) -> LayerComp:
        """
        Gets an element from the LayerComps collection.
        """
        ...

    def RemoveAll(self) -> None:
        """
        Removes all LayerComp objects from the LayerComps collection.
        """
        ...

