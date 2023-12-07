
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .application import Application
    from .document import Document

class LayerComp():
    """
    A snapshot of a state of the layers in a document (can be used to view different page layouts or compositions). 
    """
    @property
    def Appearance(self) -> bool:
        """
        Read-write. Indicates whether to use layer appearance (layer styles) settings.
        """
        ...

    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Comment(self) -> str:
        """
        Read-write. A description of the layer comp.
        """
        ...

    @property
    def Name(self) -> str:
        """
        Read-write. The name of the layer comp.
        """
        ...

    @property
    def Parent(self) -> Document:
        """
        Read-write. The LayerComp object's container.
        """
        ...

    @property
    def Position(self) -> bool:
        """
        Read-write. Indicates whether to use layer position.
        """
        ...

    @property
    def Selected(self) -> bool:
        """
        Read-only. Indicates whether the layer comp is currently selected.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced LayerComp object.
        """
        ...

    @property
    def Visibility(self) -> bool:
        """
        Read-write. Indicates whether to use layer visibility settings.
        """
        ...

    def Apply(self) -> None:
        """
        Applies the layer comp to the document.
        """
        ...

    def Delete(self) -> None:
        """
        Deletes the LayerComp object.
        """
        ...

    def Recapture(self) -> None:
        """
        Recaptures the current layer state(s) for this layer comp.
        """
        ...

    def ResetfromComp(self) -> None:
        """
        Resets the layer comp state to the document state.
        """
        ...

