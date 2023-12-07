
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from pspathkind import PsPathKind
    from document import Document
    from subpathitems import SubPathItems
    from application import Application
    from psselectiontype import PsSelectionType

class PathItem():
    """
    A path or drawing object, such as the outline of a sh ape or a straight or curved line, which contains sub paths that comprise its geometry. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Kind(self) -> PsPathKind:
        """
        Read-write. The PathItem object’s type.
        """
        ...

    @property
    def Name(self) -> str:
        """
        Read-write. The PathItem object’s name.
        """
        ...

    @property
    def Parent(self) -> Document:
        """
        Read-only. The PathItem object's container.
        """
        ...

    @property
    def SubPathItems(self) -> SubPathItems:
        """
        Read-only. The sub path objects for this PathItem object.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced PathItem object.
        """
        ...

    def Delete(self) -> None:
        """
        Deletes this PathItem object.
        """
        ...

    def Deselect(self) -> None:
        """
        Deselects this PathItem object.
        """
        ...

    def Duplicate(self, Name:str) -> None:
        """
        Duplicates this PathItem object with the new name specified in the argument.
        """
        ...

    def FillPath(self, FillColor, Mode, Opacity, PreserveTransparency, Feather, WholePath, AntiAlias) -> None:
        """
        Fills the area enclosed by the path (Opacity: 0 - 100 as percent; Feather: 0.0 - 250.0 in pixels).
        """
        ...

    def MakeClippingPath(self, Flatness:float) -> None:
        """
        Makes this PathItem object the clipping path for this document; the optional parameter tells the PostScript printer how to approximate curves in the path (0.2 - 100).
        """
        ...

    def MakeSelection(self, Feather:float, AntiAlias:bool, Operation:PsSelectionType) -> None:
        """
        Makes a Selection object, whose border is the path, from this PathItem Object (Feather: 0.0 - 250.0 in pixels). Note:See ‘Selection’ on page 136.
        """
        ...

    def Select(self) -> None:
        """
        Makes this PathItem object the active or selected PathItem object.
        """
        ...

    def StrokePath(self, Tool, SimulatePressure) -> None:
        """
        Strokes the path with the specified information.
        """
        ...

