
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from historystate import HistoryState
    from application import Application
    from document import Document

class HistoryStates():
    """
    The collection of HistoryState objects in the document. Note: See ‘HistoryState ’ on page 89 for more information on HistoryState objects.
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
        Read-only. The number of elements in the HistoryStates collection.
        """
        ...

    @property
    def Parent(self) -> Document:
        """
        Read-only. The HistoryStates object's container.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced HistoryStates object.
        """
        ...

    def Index(self, ItemPtr:HistoryState) -> int:
        """
        Gets the index of the HistoryState into the collection.
        """
        ...

    def Item(self, ItemKey:int) -> HistoryState:
        """
        Gets an element from the HistoryStates collection.
        """
        ...

