
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from solidcolor import SolidColor
    from pschanneltype import PsChannelType
    from application import Application
    from document import Document

class Channel():
    """
    Object that stores information about a color element in the image, analogous to a plate in the printing process that applies a single color. The document ’s color mode determines the number of default channels; for example, an RGB docu ment has four default channels: ?A composite channel: RGB?Three component channels: red, green, blueA channel can also be an al pha channel, which stores se lections as masks, or a sp ot channel, which stores spot colors.
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Color(self) -> SolidColor:
        """
        Read-write. The color of the channel. Note:Not valid when Type = 1.
        """
        ...

    @property
    def Histogram(self) -> List[int]:
        """
        Read-only. A histogram of the color of the channel. Note:Not valid when Type = 1. For component channel histogram values, use the Histogram property of the Document object instead. See Histogram.
        """
        ...

    @property
    def Kind(self) -> PsChannelType:
        """
        Read-write. The channel type.
        """
        ...

    @property
    def Name(self) -> str:
        """
        Read-write. The channel's name.
        """
        ...

    @property
    def Opacity(self) -> float:
        """
        Read-write. The opacity to use for alpha channels or the solidity to use for spot channels (0 - 100). Note:Valid only when Type = 2 or Type = 3.
        """
        ...

    @property
    def Parent(self) -> Document:
        """
        Read-only. The object's container.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced Channel object.
        """
        ...

    @property
    def Visible(self) -> bool:
        """
        Read-write. Indicates whether the channel is visible.
        """
        ...

    def Delete(self) -> None:
        """
        Deletes the channel.
        """
        ...

    def Duplicate(self, TargetDocument:Document):
        """
        Duplicates the channel.
        """
        ...

    def Merge(self) -> None:
        """
        Merges a spot channel into the component channels.
        """
        ...

