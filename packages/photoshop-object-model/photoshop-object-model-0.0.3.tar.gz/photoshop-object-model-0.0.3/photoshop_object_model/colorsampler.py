
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .solidcolor import SolidColor
    from .document import Document

class ColorSampler():
    """
    A color sampler for the document. Note: For additional information about color sample rs, see Adobe Photoshop help on the Color SamplerTool. 
    """
    @property
    def Color(self) -> SolidColor:
        """
        Read-only. The color of the color sampler.
        """
        ...

    @property
    def Position(self) -> List[float]:
        """
        Read-only. The position of the color sampler in the document.
        """
        ...

    @property
    def Parent(self) -> Document:
        """
        Read-only. The ColorSampler object’s container.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced ColorSampler object.
        """
        ...

    def Move(self, position:List[float]) -> None:
        """
        Moves the color sampler to a new location in the document. The position parameter (x,y) represents the new horizontal and vertical locations, respectively, of the moved color sampler.
        """
        ...

    def Delete(self) -> None:
        """
        Deletes the ColorSampler object.
        """
        ...

