
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from application import Application

class NoColor():
    """
    An object that represents a missing color. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced noColor object.
        """
        ...

