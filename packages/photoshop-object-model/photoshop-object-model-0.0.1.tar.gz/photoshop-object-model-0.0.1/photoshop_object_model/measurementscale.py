
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any

class MeasurementScale():
    """
    The measurement scale for the document. See MeasurementScale (in the Properties table for the Document object.)Note: The MeasurementScale feature is available in the Extended Version only.
    """
    @property
    def PixelLength(self) -> int:
        """
        Read-write. The length in pixels this scale equates to.
        """
        ...

    @property
    def LogicalLength(self) -> float:
        """
        Read-write. The logical length this scale equates to.
        """
        ...

    @property
    def LogicalUnits(self) -> str:
        """
        Read-write. The logical units for this scale.
        """
        ...

