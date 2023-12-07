
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .application import Application

class TextFont():
    """
    Details about a font in the TextFonts collection. Note: See TextFonts for more information on the TextFonts collection.
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Family(self) -> str:
        """
        Read-only. The font family.
        """
        ...

    @property
    def Name(self) -> str:
        """
        Read-only. The name of the font.
        """
        ...

    @property
    def Parent(self) -> Application:
        """
        Read-only. The object's container.
        """
        ...

    @property
    def PostScriptName(self) -> str:
        """
        Read-only. The PostScript name of the font.
        """
        ...

    @property
    def Style(self) -> str:
        """
        Read-only. The font style.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced TextFont object.
        """
        ...

