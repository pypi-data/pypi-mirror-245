
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .application import Application

class PhotoshopSaveOptions():
    """
    Options that can be specified when saving a document in PSD format. 
    """
    @property
    def AlphaChannels(self) -> bool:
        """
        Read-write. Indicates whether to save the alpha channels.
        """
        ...

    @property
    def Annotations(self) -> bool:
        """
        Read-write. Indicates whether to save the annotations.
        """
        ...

    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def EmbedColorProfile(self) -> bool:
        """
        Read-write. Indicates whether to embed the color profile in the document.
        """
        ...

    @property
    def Layers(self) -> bool:
        """
        Read-write. Indicates whether to preserve the layers.
        """
        ...

    @property
    def SpotColors(self) -> bool:
        """
        Read-write. Indicates whether to save the spot colors.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced PhotoshopSaveOptions object.
        """
        ...

