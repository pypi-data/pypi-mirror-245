
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from layersets import LayerSets
    from layerset import LayerSet
    from layers import Layers
    from document import Document
    from psanchorposition import PsAnchorPosition
    from artlayer import ArtLayer
    from application import Application
    from artlayers import ArtLayers
    from psblendmode import PsBlendMode
    from channel import Channel
    from pselementplacement import PsElementPlacement

class LayerSet():
    """
    A group of layer object s, which can include ArtLayer objects and other (nested) LayerSet objects. A single command or set of commands manipulates all layers in a LayerSet object. 
    """
    @property
    def AllLocked(self) -> bool:
        """
        Read-write. Indicates whether the contents in the layers contained in the LayerSet object are editable.
        """
        ...

    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def ArtLayers(self) -> ArtLayers:
        """
        Read-only. The ArtLayers in this LayerSet.
        """
        ...

    @property
    def BlendMode(self) -> PsBlendMode:
        """
        Read-write. The blend mode to use for the layer set.
        """
        ...

    @property
    def Bounds(self) -> List[float]:
        """
        Read-only. The bounding rectangle of the layer set.
        """
        ...

    @property
    def EnabledChannels(self) -> List[Channel]:
        """
        Read-write. The channels enabled for the layer set; must be a list of component channels. Note:See Kind in the Properties table for the Channel Object (‘Channel’ on page 43).
        """
        ...

    @property
    def Layers(self) -> Layers:
        """
        Read-only. The layers in this LayerSet object.
        """
        ...

    @property
    def LayerSets(self) -> LayerSets:
        """
        Read-only. The top level LayerSets in this document.
        """
        ...

    @property
    def LinkedLayers(self) -> List[ArtLayer]:
        """
        Read-only. The layers linked to this LayerSet object.
        """
        ...

    @property
    def Name(self) -> str:
        """
        Read-write. The name of the LayerSet object.
        """
        ...

    @property
    def Opacity(self) -> float:
        """
        Read-write. The master opacity of the LayerSet Object (0.0 - 100.0).
        """
        ...

    @property
    def Parent(self) -> Document|LayerSet:
        """
        Read-only. The LayerSet object's container.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced LayerSet object.
        """
        ...

    @property
    def Visible(self) -> bool:
        """
        Read-write. Indicates whether the LayerSet object is visible.
        """
        ...

    def Delete(self) -> None:
        """
        Deletes the LayerSet object.
        """
        ...

    def Duplicate(self, RelativeObject:ArtLayer|LayerSet, InsertionLocation:PsElementPlacement):
        """
        Creates a duplicate of the LayerSet object.
        """
        ...

    def Link(self, With:ArtLayer|LayerSet) -> None:
        """
        Links the layer set with another layer.
        """
        ...

    def Merge(self) -> ArtLayer:
        """
        Merges the layerset; returns a reference to the art layer created by this method.
        """
        ...

    def Move(self, RelativeObject:Application, InsertionLocation:PsElementPlacement) -> None:
        """
        Moves the LayerSet object.
        """
        ...

    def Resize(self, Horizontal:float, Vertical:float, Anchor:PsAnchorPosition) -> None:
        """
        Resizes all layers in the layer set to the specified dimensions (as a percentage of its current size) and places the layer set in the specified position.
        """
        ...

    def Rotate(self, Angle:float, Anchor:PsAnchorPosition) -> None:
        """
        Rotates all layers in the layer set around the specified anchor point.
        """
        ...

    def Translate(self, DeltaX:float, DeltaY:float) -> None:
        """
        Moves the position relative to its current position.
        """
        ...

    def Unlink(self) -> None:
        """
        Unlinks the layer set.
        """
        ...

