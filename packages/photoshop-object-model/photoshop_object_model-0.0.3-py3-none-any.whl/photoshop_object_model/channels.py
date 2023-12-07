
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .numberlong import NumberLong
    from .channel import Channel
    from .application import Application
    from .document import Document

class Channels():
    """
    The collection of Channel objects in the document. See ‘Channel ’ on page 43.
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the collection belongs to.
        """
        ...

    @property
    def Count(self) -> int:
        """
        Read-only. The number of elements in the Channels collection.
        """
        ...

    @property
    def Parent(self) -> Document:
        """
        Read-only. The object’s container.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced Channels object.
        """
        ...

    def Add(self) -> Channel:
        """
        Creates a new Channel object.
        """
        ...

    def Index(self, ItemPtr:Channel) -> int:
        """
        Gets the index of the specified Channel object.
        """
        ...

    def Item(self, ItemKey:NumberLong) -> Channel:
        """
        Gets an element from the Channels collection.
        """
        ...

    def RemoveAll(self) -> None:
        """
        Removes all Channel objects from the Channels collection.
        """
        ...

