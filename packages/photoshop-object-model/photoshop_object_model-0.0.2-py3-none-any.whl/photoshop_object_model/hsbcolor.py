
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from application import Application

class HSBColor():
    """
    Options that can be specified for a co lor object using the HSB color model. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Brightness(self) -> float:
        """
        Read-write. The brightness value (0.0 - 100.0).
        """
        ...

    @property
    def Hue(self) -> float:
        """
        Read-write. The hue value (0.0 - 100.0).
        """
        ...

    @property
    def Saturation(self) -> float:
        """
        Read-write. The saturation value (0.0 - 100.0).
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced HSBColor object.
        """
        ...

