
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from psreferenceformtype import PsReferenceFormType
    from application import Application

class ActionReference():
    """
    A reference object that contains the data describing the object you are referring to. Note: The actionReference object is part of the Action Manager functionality. See the Photoshop Scripting Guide.
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced Action object.
        """
        ...

    def GetContainer(self):
        """
        Gets a reference contained in this reference. Container references provide additional pieces to the reference. This looks like another reference, but it is actually part of the same reference.
        """
        ...

    def GetDesiredClass(self) -> int:
        """
        Gets a number representing the class of the object.
        """
        ...

    def GetEnumeratedType(self) -> int:
        """
        Gets the enumeration type.
        """
        ...

    def GetEnumeratedValue(self) -> int:
        """
        Gets the enumeration value.
        """
        ...

    def GetForm(self) -> PsReferenceFormType:
        """
        Gets the form of an ActionReference.
        """
        ...

    def GetIdentifier(self) -> int:
        """
        Gets the identifier value for a reference whose form is identifier.
        """
        ...

    def GetIndex(self) -> int:
        """
        Gets the index value for a reference in a list or array.
        """
        ...

    def GetName(self) -> str:
        """
        Gets the name of a reference.
        """
        ...

    def GetOffset(self) -> int:
        """
        Gets the offset of the object’s index value.
        """
        ...

    def GetProperty(self) -> int:
        """
        Gets the property ID value.
        """
        ...

    def PutClass(self, DesiredClass:int) -> None:
        """
        Puts a new class form and class type into the reference.
        """
        ...

    def PutEnumerated(self, DesiredClass:int, EnumType:int, Value:int) -> None:
        """
        Puts an enumeration type and ID into a reference along with the desired class for the reference.
        """
        ...

    def PutIdentifier(self, DesiredClass:int, Value:int) -> None:
        """
        Puts a new identifier and value into the reference..
        """
        ...

    def PutIndex(self, DesiredClass:int, Value:int) -> None:
        """
        Puts a new index and value into the reference.
        """
        ...

    def PutName(self, DesiredClass:int, Value:str) -> None:
        """
        Puts a new name and value into the reference.
        """
        ...

    def PutOffset(self, DesiredClass:int, Value:int) -> None:
        """
        Puts a new offset and value into the reference.
        """
        ...

    def PutProperty(self, DesiredClass:int, Value:int) -> None:
        """
        Puts a new property and value into the reference.
        """
        ...

