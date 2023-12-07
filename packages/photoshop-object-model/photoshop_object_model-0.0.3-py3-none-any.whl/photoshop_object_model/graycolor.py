
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .application import Application

class GrayColor():
    """
    Options for defining a gray color. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Gray(self) -> float:
        """
        Read-write. The gray value (0.0 - 100.0; default: 0.0).
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced grayColor object.
        """
        ...

