
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from subpathinfo import SubPathInfo
    from pathitem import PathItem
    from application import Application
    from document import Document

class PathItems():
    """
    The collection of PathItem objects in the document.Note: See ‘PathItem ’ on page 109 for information on PathItem objects.
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
        Read-only. The number of PathItem objects in the PathItems collection.
        """
        ...

    @property
    def Parent(self) -> Document:
        """
        Read-only. The PathItems object's container.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced PathItems object.
        """
        ...

    def Add(self, Name:str, EntirePath:List[SubPathInfo]) -> PathItem:
        """
        Creates a new PathItem object from the sub paths defined in the array provided in the EntirePath parameter. A new SubPathItem object is created for each SubPathInfo object provided in entirePath, and those SubPathItem objects are added to the SubPathItems collection of the returned PathItem.
        """
        ...

    def Index(self, ItemPtr:PathItem) -> int:
        """
        Gets the index of the PathIem into the collection.
        """
        ...

    def Item(self, ItemKey:int) -> PathItem:
        """
        Gets a PathItem object from the PathItems collection.
        """
        ...

    def RemoveAll(self) -> None:
        """
        Removes all PathItem objects from the PathItems collection.
        """
        ...

