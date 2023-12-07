
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from actionreference import ActionReference
    from application import Application
    from psdescvaluetype import PsDescValueType
    from actiondescriptor import ActionDescriptor

class ActionList():
    """
    This object provides an array-style mechanism for stor ing dta. It can be used for low-leve access into Photoshop.This object is ideal when storing data of the same type. All items in the list must be the same type.You can use the "put" methods, such as putBoolean(), to append new elements, and can clear the entire list using clear(), but cannoth otherwise modify the list. Note: The actionList object is part of the Action Manager functionality. For details on using the Action Manager, see the Photoshop Scripting Guide.
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Count(self) -> int:
        """
        Read-only. The number of commands that comprise the action.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced actionList object.
        """
        ...

    def Clear(self) -> None:
        """
        Clears the list.
        """
        ...

    def GetBoolean(self, Index:int) -> bool:
        """
        Gets the value of a list item of type boolean.
        """
        ...

    def GetClass(self, Index:int) -> int:
        """
        Gets the value of a list item of type class.
        """
        ...

    def GetDouble(self, Index:int) -> float:
        """
        Gets the value of a list item of type double.
        """
        ...

    def GetEnumerationType(self, Index:int) -> int:
        """
        Gets the enumeration type of a list item.
        """
        ...

    def GetEnumerationValue(self, Index:int) -> int:
        """
        Gets the enumeration value of a list item.
        """
        ...

    def GetInteger(self, Index:int) -> int:
        """
        Gets the value of a list item of type integer.
        """
        ...

    def GetLargeInteger(self, Index:int) -> int:
        """
        Gets the value of a list item of type large integer.
        """
        ...

    def GetList(self, Index:int):
        """
        Gets the value of a list item of type list.
        """
        ...

    def GetObjectType(self, Index:int) -> int:
        """
        Gets the class ID of a list item of type object.
        """
        ...

    def GetObjectValue(self, Index:int) -> ActionDescriptor:
        """
        Gets the value of a list item of type object.
        """
        ...

    def GetPath(self, Index:int) -> str:
        """
        Gets the value of a list item of type Alias. Retuns a String that represents a file path.
        """
        ...

    def GetReference(self, Index:int) -> ActionReference:
        """
        Gets the value of a list item of type ActionReference.
        """
        ...

    def GetString(self, Index:int) -> str:
        """
        Gets the value of a list item of type String.
        """
        ...

    def GetType(self, Index:int) -> PsDescValueType:
        """
        Gets the type of a list item.
        """
        ...

    def GetUnitDoubleType(self, Index:int) -> int:
        """
        Gets the unit value type of a list item of type Double.
        """
        ...

    def GetUnitDoubleValue(self, Index:int) -> float:
        """
        Gets the unit value of a list item of type double.
        """
        ...

    def PutBoolean(self, Value:bool) -> None:
        """
        Sets the value to either true or false.
        """
        ...

    def PutClass(self, Value:int) -> None:
        """
        Sets the class or data type.
        """
        ...

    def PutDouble(self, Value:float) -> None:
        """
        Sets the value type as a double.
        """
        ...

    def PutEnumerated(self, EnumType:int, Value:int) -> None:
        """
        Sets the value type as an enumerated, or constant, value.
        """
        ...

    def PutInteger(self, Value:int) -> None:
        """
        Sets the value of a list item of type integer.
        """
        ...

    def PutLargeInteger(self, Value:int) -> None:
        """
        Sets the value of a list item of type large integer.
        """
        ...

    def PutList(self, Value) -> None:
        """
        Sets the value of a list item of type list or array.
        """
        ...

    def PutObject(self, ClassID:int, Value:ActionDescriptor) -> None:
        """
        Sets the value of a list item of type object.
        """
        ...

    def PutPath(self, Value:str) -> None:
        """
        Sets the value of a list item of type path. The Value parameter takes a String that represents a file path.
        """
        ...

    def PutReference(self, Value:ActionReference) -> None:
        """
        Sets the value of a list item whose type a reference to an object created in the script.
        """
        ...

    def PutString(self, Value:str) -> None:
        """
        Sets the value of a list item of type String.
        """
        ...

    def PutUnitDouble(self, UnitID:int, Value:float) -> None:
        """
        Sets the value of a list item of type unit value represented as a double.
        """
        ...

