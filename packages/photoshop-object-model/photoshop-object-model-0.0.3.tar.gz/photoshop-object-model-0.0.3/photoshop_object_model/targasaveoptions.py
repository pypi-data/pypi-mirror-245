
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .application import Application
    from .pstargabitsperpixels import PsTargaBitsPerPixels

class TargaSaveOptions():
    """
    Options that can be set when saving a document in TGA (Targa) format. 
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
    def Resolution(self) -> PsTargaBitsPerPixels:
        """
        Read-write. The number of bits per pixel. Default: 24.
        """
        ...

    @property
    def RLECompression(self) -> bool:
        """
        Read-write. Indicates whether RLE compression should be used. Default: true.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced TargaSaveOptions object.
        """
        ...

