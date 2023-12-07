
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .application import Application
    from .textfont import TextFont

class TextFonts():
    """
    The collection of fonts available on your computer.Note: The TextFonts object corresponds to the Fonts property of the Application object. In a script, you use Fonts to refer to a TextFonts object. The following sample demonstrates how to use the Count property of the TextFonts object to display a dialog that indicates the number of fonts installed on the machine. ?Correct:Alert appRef.Fonts.Count?Incorrect:Alert appRef.TextFonts.CountSee ‘Application ’ on page 16’ , specifically the Fonts property, for more information. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the collection belongs to.
        """
        ...

    @property
    def Count(self) -> int:
        """
        Read-only. The number of elements in the TextFonts collection.
        """
        ...

    @property
    def Parent(self) -> Application:
        """
        Read-only. The object's container.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced TextFonts object.
        """
        ...

    def Index(self, ItemPtr:TextFont) -> int:
        """
        Gets the index of the TextFont into the collection.
        """
        ...

    def Item(self, ItemKey:int) -> TextFont:
        """
        Gets an element from the TextFonts collection.
        """
        ...

