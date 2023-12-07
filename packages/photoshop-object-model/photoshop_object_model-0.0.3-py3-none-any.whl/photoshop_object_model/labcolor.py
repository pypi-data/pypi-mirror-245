
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .application import Application

class LabColor():
    """
    Options that can be specified when defining a color object using the LAB color model.
    """
    @property
    def A(self) -> float:
        """
        Read-write. The a-value (-128.0 - 127.0).
        """
        ...

    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def B(self) -> float:
        """
        Read-write. The b-value (-128.0 - 127.0).
        """
        ...

    @property
    def L(self) -> float:
        """
        Read-write. The L-value (0.0 - 100.0).
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced LabColor object.
        """
        ...

