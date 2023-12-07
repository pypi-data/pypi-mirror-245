
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .document import Document

class CountItem():
    """
    A counted item in the document. Also see the method AutoCount , defined on Document.Note:CountItem is available in the Extended Version only.For additional information about count items, see Adobe Photoshop help on the Count Tool.
    """
    @property
    def Position(self) -> List[float]:
        """
        Read-only. The position of the count item in the document. The array (x,y) represents the horizontal and vertical location of the count item.
        """
        ...

    @property
    def Parent(self) -> Document:
        """
        Read-only. The CountItem object’s container.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced CountItem object.
        """
        ...

    def Delete(self) -> None:
        """
        Deletes the CountItem object.
        """
        ...

