
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .application import Application

class CMYKColor():
    """
    The definition of a CMYK color. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Black(self) -> float:
        """
        Read-write. The black color value (as percent) (0.0 - 100.0).
        """
        ...

    @property
    def Cyan(self) -> float:
        """
        Read-write. The cyan color value (as percent) (0.0 - 100.0).
        """
        ...

    @property
    def Magenta(self) -> float:
        """
        Read-write. The magenta color value (as percent) (0.0 - 100.0).
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced CMYKColor object.
        """
        ...

    @property
    def Yellow(self) -> float:
        """
        Read-write. The yellow color value (as percent) (0.0 - 100.0).
        """
        ...

