
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from actionreference import ActionReference
    from application import Application
    from psdescvaluetype import PsDescValueType
    from actionlist import ActionList

class ActionDescriptor():
    """
    A record of key-value pairs for actions, such as those included on the Adobe Photoshop Actions menu. Note: The ActionDescriptor class is part of the Action Manager functionality. See the Photoshop Scripting Guide.
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
        Read-only. The number of keys contained in the descriptor.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced ActionDescriptor object.
        """
        ...

    def Clear(self) -> None:
        """
        Clears the descriptor.
        """
        ...

    def Erase(self, Key:int) -> None:
        """
        Erases a key from the descriptor.
        """
        ...

    def GetBoolean(self, Key:int) -> bool:
        """
        Gets the value of a key of type boolean.
        """
        ...

    def GetClass(self, Key:int) -> int:
        """
        Gets the value of a key of type class.
        """
        ...

    def GetDouble(self, Key:int) -> float:
        """
        Gets the value of a key of type double.
        """
        ...

    def GetEnumerationType(self, Key:int) -> int:
        """
        Gets the enumeration type of a key.
        """
        ...

    def GetEnumerationValue(self, Key:int) -> int:
        """
        Gets the enumeration value of a key.
        """
        ...

    def GetInteger(self, Key:int) -> int:
        """
        Gets the value of a key of type integer.
        """
        ...

    def GetKey(self, Index:int) -> int:
        """
        Gets the ID of the Nth key.
        """
        ...

    def GetLargeInteger(self, Key:int) -> int:
        """
        Gets the value of a key of type large integer.
        """
        ...

    def GetList(self, Key:int) -> ActionList:
        """
        Gets the value of a key of type list.
        """
        ...

    def GetObjectType(self, Key:int) -> int:
        """
        Gets the class ID of an object in a key of type object.
        """
        ...

    def GetObjectValue(self, Key:int):
        """
        Gets the value of a key of type object.
        """
        ...

    def GetPath(self, Key:int) -> str:
        """
        Gets the value of a key of type Alias. Returns a String that represents a file path.
        """
        ...

    def GetReference(self, Key:int) -> ActionReference:
        """
        Gets the value of a key of type ActionReference.
        """
        ...

    def GetString(self, Key:int) -> str:
        """
        Gets the value of a key of type String.
        """
        ...

    def GetType(self, Key:int) -> PsDescValueType:
        """
        Gets the type of a key.
        """
        ...

    def GetUnitDoubleType(self, Key:int) -> int:
        """
        Gets the unit type of a key of type UnitDouble.
        """
        ...

    def GetUnitDoubleValue(self, Key:int) -> float:
        """
        Gets the value of a key of type UnitDouble.
        """
        ...

    def HasKey(self, Key:int) -> bool:
        """
        Checks whether the descriptor contains the provided key.
        """
        ...

    def IsEqual(self, otherDesc) -> bool:
        """
        Determines whether the descriptor is the same as another descriptor.
        """
        ...

    def PutBoolean(self, Key:int, Value:bool) -> None:
        """
        Sets the value for a key whose type is Boolean.
        """
        ...

    def PutClass(self, Key:int, Value:int) -> None:
        """
        Sets the value for a key whose type is class.
        """
        ...

    def PutDouble(self, Key:int, Value:float) -> None:
        """
        Sets the value for a key whose type is double.
        """
        ...

    def PutEnumerated(self, Key:int, EnumType:int, Value:int) -> None:
        """
        Sets the enumeration type and value for a key.
        """
        ...

    def PutInteger(self, Key:int, Value:int) -> None:
        """
        Sets the value for a key whose type is integer.
        """
        ...

    def PutLargeInteger(self, Key:int, Value:int) -> None:
        """
        Sets the value for a key whose type is large integer.
        """
        ...

    def PutList(self, Key:int, Value:ActionList) -> None:
        """
        Sets the value for a key whose type is an ActionList object.
        """
        ...

    def PutObject(self, Key:int, ClassID:int, Value) -> None:
        """
        Sets the value for a key whose type is an Action Descriptor.
        """
        ...

    def PutPath(self, Key:int, Value:str) -> None:
        """
        Sets the value for a key whose type is path. The Value argument takes a String that represents a file path.
        """
        ...

    def PutReference(self, Key:int, Value:ActionReference) -> None:
        """
        Sets the value for a key whose type is an object reference.
        """
        ...

    def PutString(self, Key:int, Value:str) -> None:
        """
        Sets the value for a key whose type is String.
        """
        ...

    def PutUnitDouble(self, Key:int, UnitID:int, Value:float) -> None:
        """
        Sets the value for a key whose type is a unit value formatted as a double.
        """
        ...

