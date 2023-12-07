
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .psbyteorder import PsByteOrder
    from .application import Application

class RawFormatOpenOptions():
    """
    Options that can be specified when opening a document in RAW format. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def BitsPerChannel(self) -> int:
        """
        Read-write. The number of bits for each channel. Note:The only valid values are BitsPerChannel = 8 or BitsPerChannel = 16.
        """
        ...

    @property
    def ByteOrder(self) -> PsByteOrder:
        """
        Read-write. The order in which bytes will be read. Note:Valid only when BitsPerChannel = 16. See BitsPerChannel.
        """
        ...

    @property
    def ChannelNumber(self) -> int:
        """
        Read-write. The number of channels in the image (1 - 56). Note:The value of ChannelNumber cannot exceed the number of channels in the image. When BitsPerChannel = 16, only the following values are valid: 1, 3, or 4. See BitsPerChannel.
        """
        ...

    @property
    def HeaderSize(self) -> int:
        """
        Read-write. The number of bytes of information that will appear in the file before actual image information begins; that is, the number of zeroes inserted at the beginning of the file as placeholders (0 - 1919999).
        """
        ...

    @property
    def Height(self) -> int:
        """
        Read-write. The height of the image (in pixels).
        """
        ...

    @property
    def InterleaveChannels(self) -> bool:
        """
        Read-write. Indicates whether to store color values sequentially.
        """
        ...

    @property
    def RetainHeader(self) -> bool:
        """
        Read-write. Indicates whether to retain the header when saving. Note:Valid only when HeaderSize is 1 or greater.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced RawFormatOpenOptions object.
        """
        ...

    @property
    def Width(self) -> int:
        """
        Read-write. The image width in pixels.
        """
        ...

