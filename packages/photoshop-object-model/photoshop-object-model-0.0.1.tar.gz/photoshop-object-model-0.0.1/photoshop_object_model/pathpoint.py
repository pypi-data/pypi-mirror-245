
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from pspointkind import PsPointKind
    from application import Application
    from subpathitem import SubPathItem

class PathPoint():
    """
    Information about an array of PathPointInfo objects.Note: You do not use the PathPoint object to create points that make up a path. Rather, you use the PathPoint object to retrieve information about the points that describe path segments. To create path points, use the PathPointInfo objects. See ‘PathPointInfo ’ on page 115.
    """
    @property
    def Anchor(self) -> List[float]:
        """
        Read-only. The point on the curve (LeftDirection/RightDirection are points representing the control handle end points).
        """
        ...

    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Kind(self) -> PsPointKind:
        """
        Read-only. The PathPoint object’s type.
        """
        ...

    @property
    def LeftDirection(self) -> List[float]:
        """
        Read-only. The x and y coordinates that define the left handle.
        """
        ...

    @property
    def Parent(self) -> SubPathItem:
        """
        Read-only. The PathPoint object's container.
        """
        ...

    @property
    def RightDirection(self) -> List[float]:
        """
        Read-only. The x and y coordinates that define the right handle.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced PathPoint object.
        """
        ...

