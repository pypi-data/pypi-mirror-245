
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from application import Application

class RGBColor():
    """
    The definition of a color in RGB color mode.
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Blue(self) -> float:
        """
        Read-write. The blue color value ( 0.0 - 255.0; default: 255.0).
        """
        ...

    @property
    def Green(self) -> float:
        """
        Read-write. The green color value (0.0 - 255.0; default: 255.0).
        """
        ...

    @property
    def HexValue(self) -> str:
        """
        Read-write. The hex representation of the color.
        """
        ...

    @property
    def Red(self) -> float:
        """
        Read-write. The red color value (0.0 - 255.0; default: 255.0).
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced RGBColor object.
        """
        ...

