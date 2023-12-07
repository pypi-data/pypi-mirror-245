
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from application import Application
    from pspointkind import PsPointKind

class PathPointInfo():
    """
    A point on a path, expressed as an array of three coordi nate arrays: the anchor point, left direction point, and right direction point. For paths that are straight segments (not curved), the coordinates of all three points are the same. For curved segments, the coordinates are different. The difference between the anchor point and the left or right direction points determines the arc of the curve. You use the left direction point to bend the curve “outward” or make it convex; you use the right direction point to bend the curve “inward” or make it concave.
    """
    @property
    def Anchor(self) -> list:
        """
        Read-write. The x and y coordinates of one end point of the path segment.
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
        Read-write. The PathPointInfo object’s kind.
        """
        ...

    @property
    def LeftDirection(self) -> List[float]:
        """
        Read-write. The location of the left direction point (’in’ position).
        """
        ...

    @property
    def RightDirection(self) -> List[float]:
        """
        Read-write. The location of the right handle (’out’ position).
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced PathPointInfo object.
        """
        ...

