
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .psshapeoperation import PsShapeOperation
    from .application import Application
    from .pathpoints import PathPoints
    from .pathitem import PathItem

class SubPathItem():
    """
    Information about a path. Note: You do not use the SubPathItem object to create a path. Rather, you create path segments using the SubPathInfo object. Use the SubPathItem object to retrieve information about a path. (Note that all of the SubPathItem object’s properties are Read-only.)
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
        Read-only. Indicates whether the path is closed.
        """
        ...

    @property
    def Operation(self) -> PsShapeOperation:
        """
        Read-only. The sub path operation on other sub paths.
        """
        ...

    @property
    def Parent(self) -> PathItem:
        """
        Read-only. The object's container.
        """
        ...

    @property
    def PathPoints(self) -> PathPoints:
        """
        Read-only. The PathPoints collection.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced SubPathItem object.
        """
        ...

