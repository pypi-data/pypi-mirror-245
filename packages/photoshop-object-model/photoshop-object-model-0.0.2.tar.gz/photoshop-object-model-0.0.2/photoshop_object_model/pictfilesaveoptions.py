
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from pspictbitsperpixels import PsPICTBitsPerPixels
    from application import Application
    from pspictcompression import PsPICTCompression

class PICTFileSaveOptions():
    """
    Options that can be specified when saving a document in PICT format. 
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
    def Compression(self) -> PsPICTCompression:
        """
        Read-write. Default: 1)
        """
        ...

    @property
    def EmbedColorProfile(self) -> bool:
        """
        Read-write. Indicates whether to embed the color profile in the document.
        """
        ...

    @property
    def Resolution(self) -> PsPICTBitsPerPixels:
        """
        Read-write. The number of bits per pixel.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced PICTFileSaveOptions object.
        """
        ...

