
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .subpathitem import SubPathItem
    from .application import Application
    from .pathpoint import PathPoint

class PathPoints():
    """
    A collection of PathPoint objects that comprises the PathPoints property of the SubPathItem object.Note: See ‘SubPathItem ’ on page 144 for more information.
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
        Read-only. The number of elements in the PathPoints collection.
        """
        ...

    @property
    def Parent(self) -> SubPathItem:
        """
        Read-only. The PathPoints object's container.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced PathPoints object.
        """
        ...

    def Index(self, ItemPtr:PathPoint) -> int:
        """
        Gets the index of the PathPoint into the collection.
        """
        ...

    def Item(self, ItemKey:int) -> PathPoint:
        """
        Gets an element from the PathPoints collection.
        """
        ...

