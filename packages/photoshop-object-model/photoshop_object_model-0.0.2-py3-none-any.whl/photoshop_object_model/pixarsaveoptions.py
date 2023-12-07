
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from application import Application

class PixarSaveOptions():
    """
    Options that can be specified when saving a document in Pixar format. 
    """
    @property
    def AlphaChannels(self) -> bool:
        """
        Read-write. Indicates whether to save the alpha channels.
        """
        ...

    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced PixarSaveOptions object.
        """
        ...

