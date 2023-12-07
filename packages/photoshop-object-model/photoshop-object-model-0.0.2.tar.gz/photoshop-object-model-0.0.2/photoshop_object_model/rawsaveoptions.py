
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from application import Application

class RawSaveOptions():
    """
    Options that can be specified when saving a document in RAW format. 
    """
    @property
    def AlphaChannels(self) -> bool:
        """
        Read-write. Indicates whether alpha channels should be saved.
        """
        ...

    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def SpotColors(self) -> bool:
        """
        Read-write. Indicates whether the spot colors should be saved.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced RawSaveOptions object.
        """
        ...

