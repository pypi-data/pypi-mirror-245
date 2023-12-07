
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from application import Application
    from document import Document

class HistoryState():
    """
    A version of the document stored automatically (and added to the HistoryStates collection), which preserves the document’s state, each time the document is saved. Note: See “HistoryStates ” on page 90‘ for information about the HistoryStates collection. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Name(self) -> str:
        """
        Read-only. The HistoryState object's name.
        """
        ...

    @property
    def Parent(self) -> Document:
        """
        Read-only. The HistoryState object's container.
        """
        ...

    @property
    def Snapshot(self) -> bool:
        """
        Read-only. Indicates whether the history state is a snapshot.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced HistoryState object.
        """
        ...

