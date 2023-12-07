
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .psopendocumentmode import PsOpenDocumentMode
    from .application import Application

class EPSOpenOptions():
    """
    Options that can be specified when opening an EPS format document. 
    """
    @property
    def AntiAlias(self) -> bool:
        """
        Read-write. Indicates whether to use antialias.
        """
        ...

    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def ConstrainProportions(self) -> bool:
        """
        Read-write. Indicates whether to constrain the proportions of the image.
        """
        ...

    @property
    def Height(self) -> float:
        """
        Read-write. The height of the image (unit value).
        """
        ...

    @property
    def Mode(self) -> PsOpenDocumentMode:
        """
        Read-write. The color profile to use as the document mode.
        """
        ...

    @property
    def Resolution(self) -> float:
        """
        Read-write. The resolution of the document in pixels per inch.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced EPSOpenOptions object.
        """
        ...

    @property
    def Width(self) -> float:
        """
        Read-write. The width of the image (unit value).
        """
        ...

