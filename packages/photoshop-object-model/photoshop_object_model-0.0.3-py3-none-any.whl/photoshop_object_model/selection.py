
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .document import Document
    from .psselectiontype import PsSelectionType
    from .application import Application
    from .channel import Channel
    from .pscolorblendmode import PsColorBlendMode
    from .psanchorposition import PsAnchorPosition
    from .psstrokelocation import PsStrokeLocation
    from .solidcolor import SolidColor
    from .historystate import HistoryState

class Selection():
    """
    The selected area of a document or layer. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Bounds(self) -> List[float]:
        """
        Read-only. The bounding rectangle of the entire selection.
        """
        ...

    @property
    def Parent(self) -> Document:
        """
        Read-only. The object's container.
        """
        ...

    @property
    def Solid(self) -> bool:
        """
        Read-only. Indicates if the bounding rectangle is a solid.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced Selection object.
        """
        ...

    def Clear(self) -> None:
        """
        Clears the selection and does not copy it to the clipboard.
        """
        ...

    def Contract(self, By:float) -> None:
        """
        Contracts the selection by the specified amount.
        """
        ...

    def Copy(self, Merge:bool) -> None:
        """
        Copies the selection to the clipboard. When the optional argument is used and set to true, a merged copy is performed (all visible layers in the selection are copied).
        """
        ...

    def Cut(self) -> None:
        """
        Clears the current selection and copies it to the clipboard.
        """
        ...

    def Deselect(self) -> None:
        """
        Deselects the current selection.
        """
        ...

    def Expand(self, By:float) -> None:
        """
        Expands the selection by the specified amount.
        """
        ...

    def Feather(self, By:float) -> None:
        """
        Feathers the edges of the selection by the specified amount.
        """
        ...

    def Fill(self, Filltype:List[SolidColor|HistoryState], Mode:PsColorBlendMode, Opacity:int, PreserveTransparency:bool) -> None:
        """
        Fills the selection (Opacity: 1 - 100 as percent).
        """
        ...

    def Grow(self, Tolerance:int, AntiAlias:bool) -> None:
        """
        Grows the selection to include all adjacent pixels falling within the specified tolerance range.
        """
        ...

    def Invert(self) -> None:
        """
        Inverts the selection (deselects the selection and selects the rest of the layer or document). Note:To flip the selection shape, see Rotate.
        """
        ...

    def Load(self, From, Combination, Inverting) -> None:
        """
        Loads the selection from the specified channel.
        """
        ...

    def MakeWorkPath(self, Tolerance:float) -> None:
        """
        Makes this selection item the work path for this document.
        """
        ...

    def Resize(self, Horizontal:float, Vertical:float, Anchor:PsAnchorPosition) -> None:
        """
        Resizes the selected area to the specified dimensions and anchor position.
        """
        ...

    def ResizeBoundary(self, Horizontal:float, Vertical:float, Anchor:PsAnchorPosition) -> None:
        """
        Changes the size of the selection to the specified dimensions around the specified anchor.
        """
        ...

    def Rotate(self, Angle:float, Anchor:PsAnchorPosition) -> None:
        """
        Rotates the selection by the specified amount around the specified anchor point.
        """
        ...

    def RotateBoundary(self, Angle:float, Anchor:PsAnchorPosition) -> None:
        """
        Rotates the boundary of the selection around the specified anchor.
        """
        ...

    def Select(self, Region, Type, Feather, AntiAlias) -> None:
        """
        Selects the specified region.
        """
        ...

    def SelectAll(self) -> None:
        """
        Selects the entire layer.
        """
        ...

    def SelectBorder(self, Width:float) -> None:
        """
        Selects the selection border only (in the specified width); subsequent actions do not affect the selected area within the borders.
        """
        ...

    def Similar(self, Tolerance:int, AntiAlias:bool) -> None:
        """
        Grows the selection to include pixels throughout the image falling within the tolerance range.
        """
        ...

    def Smooth(self, Radius:int) -> None:
        """
        Cleans up stray pixels left inside or outside a color-based selection (within the radius specified in pixels).
        """
        ...

    def Store(self, Into:Channel, Combination:PsSelectionType) -> None:
        """
        Saves the selection as a channel.
        """
        ...

    def Stroke(self, StrokeColor:SolidColor, Width:int, Location:PsStrokeLocation, Mode:PsColorBlendMode, Opacity:int, PreserveTransparency:bool) -> None:
        """
        Strokes the selection border (Opacity: 1 - 100 as percent).
        """
        ...

    def Translate(self, DeltaX:float, DeltaY:float) -> None:
        """
        Moves the entire selection relative to its current position.
        """
        ...

    def TranslateBoundary(self, DeltaX:float, DeltaY:float) -> None:
        """
        Moves the selection relative to its current position.
        """
        ...

