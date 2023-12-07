
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .number import number
    from .document import Document
    from .colorsampler import ColorSampler

class ColorSamplers():
    """
    The collection of ColorSampler objects in the document. See ColorSampler.
    """
    @property
    def Length(self) -> int:
        """
        Read-only. The number of elements in the ColorSamplers collection.
        """
        ...

    @property
    def Parent(self) -> Document:
        """
        Read-only. The ColorSamplers object’s container.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced ColorSamplers object.
        """
        ...

    def Add(self, position:List[float]) -> ColorSampler:
        """
        Creates a new ColorSampler object. The position parameter (x,y) represents the horizontal and vertical locations, respectively, of the new color sampler.
        """
        ...

    def Index(self, ItemPtr:ColorSampler) -> int:
        """
        Gets the index of the ColorSampler into the collection.
        """
        ...

    def Item(self, ItemKey:number) -> ColorSampler:
        """
        Gets an element from the ColorSamplers collection.
        """
        ...

    def RemoveAll(self) -> None:
        """
        Removes all ColorSampler objects from the ColorSamplers collection.
        """
        ...

