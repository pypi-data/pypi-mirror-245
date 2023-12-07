
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from application import Application
    from psbmpdepthtype import PsBMPDepthType
    from psoperatingsystem import PsOperatingSystem

class BMPSaveOptions():
    """
    Options that can be specified when saving a document in BMP format. 
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
    def Depth(self) -> PsBMPDepthType:
        """
        Read-write. The number of bits per channel.
        """
        ...

    @property
    def FlipRowOrder(self) -> bool:
        """
        Read-write. Indicates whether to write the image from top to bottom. Default: false. Note:Available only when OSType = 2. See OSType.
        """
        ...

    @property
    def OSType(self) -> PsOperatingSystem:
        """
        Read-write. The target OS. Default: 2.
        """
        ...

    @property
    def RLECompression(self) -> bool:
        """
        Read-write. Indicates whether to use RLE compression. Note:Available only when OSType = 2. See OSType.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced BMPSaveOptions object.
        """
        ...

