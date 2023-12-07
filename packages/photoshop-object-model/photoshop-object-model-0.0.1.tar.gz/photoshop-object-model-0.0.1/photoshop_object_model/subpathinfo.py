
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from pathpoint import PathPoint
    from psshapeoperation import PsShapeOperation
    from application import Application

class SubPathInfo():
    """
    An array of PathPointInfo objects that describes a straight or curved segment of a path. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Closed(self) -> bool:
        """
        Read-write. Indicates whether the path describes an enclosed area.
        """
        ...

    @property
    def EntireSubPath(self) -> List[PathPoint]:
        """
        Read-write.
        """
        ...

    @property
    def Operation(self) -> PsShapeOperation:
        """
        Read-write. The sub path’s operation on other sub paths.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced SubPathInfo object.
        """
        ...

