
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from notifier import Notifier
    from application import Application

class Notifiers():
    """
    The collection of Notifier objects in the document; the Notifiers property of the Application object. Note: See ‘Notifier ’ on page 106 for information on Notifier objects. See Notifiers (in the Properties table of the Application object).
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
        Read-only. The number of elements in the Notifiers collection.
        """
        ...

    @property
    def EventClass(self) -> str:
        """
        Read-only. The class ID of the event.
        """
        ...

    @property
    def Parent(self) -> Application:
        """
        Read-only. The Notifiers object’s container
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced Notifiers object.
        """
        ...

    def Add(self, Event:str, EventFile:str, EventClass:str) -> Notifier:
        """
        Creates a Notifier object. Note: EventClass defines the class ID of the event: four characters or a unique string . For a list of four-character codes, see Appendix A: Event ID Codes. Tip:Remember to omit the single quotes when including a four-character ID in your code. Note: EventFile defines the script file that executes when the event occurs. Note:An eventClass value corresponds to the class of object the event is applied to: four characters or a unique string. When an event applies to multiple types of objects, you use the EventClass parameter to distinguish which object this Notifier applies to. For example, the Make event (“Mk “)applies to documents (“Dcmn”), channels (“Chnl”) and other objects.
        """
        ...

    def Index(self, ItemPtr:Notifier) -> int:
        """
        Gets the index of the Notifier into the collection.
        """
        ...

    def Item(self, ItemKey:int) -> Notifier:
        """
        Gets an element from the Notifiers collection.
        """
        ...

    def RemoveAll(self) -> None:
        """
        Removes all Notifier objects from the Notifiers collection. Note:You can remove a notifier object from the Script Events Manager drop-down list by deleting the file named Script Events Manager.xml from in the Photoshop preferences folder. See Adobe Photoshop help for more information.
        """
        ...

