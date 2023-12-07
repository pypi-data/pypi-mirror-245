
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from pathitem import PathItem
    from application import Application
    from subpathitem import SubPathItem

class SubPathItems():
    """
    A collection of SubPathItem objects. See SubPathItem.
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
        Read-only. The number of elements in the SubPathItems collection.
        """
        ...

    @property
    def Parent(self) -> PathItem:
        """
        Read-only. The SubPathItems object's container.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced SubPathItems object.
        """
        ...

    def Index(self, ItemPtr:SubPathItem) -> int:
        """
        Gets the index of the SubPathItem into the collection.
        """
        ...

    def Item(self, ItemKey:int) -> SubPathItem:
        """
        Gets an element from the SubPathItems collection.
        """
        ...

