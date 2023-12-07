
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .application import Application

class Notifier():
    """
    An event-handler object that tells the script to ex ecute specified code when a specified event occurs. 
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Event(self) -> str:
        """
        Read-only. The event ID in four characters or a unique String that the notifier is associated with. Note:For a list of four-character codes, see Appendix A: Event ID Codes.
        """
        ...

    @property
    def EventClass(self) -> str:
        """
        Read-only. The class ID of the event associated with the Notifier object, four characters or a unique string. Note:When an event applies to multiple types of objects, you use this propety to distinguish which object this Notifier applies to. For example, the Make event (“Mk “)applies to documents (“Dcmn”), channels (“Chnl”) and other objects..
        """
        ...

    @property
    def EventFile(self) -> str:
        """
        Read-only. The path to the file to execute when the event occurs/activates the notifier.
        """
        ...

    @property
    def Parent(self) -> Application:
        """
        Read-only. The Notifier object’s container.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced Notifier object.
        """
        ...

    def Remove(self) -> None:
        """
        Deletes the Notifier object. Note:You can remove a Notifier object from the Script Events Manager drop-down list by deleting the file named Script Events Manager.xml from in the Photoshop preferences folder. See Adobe Photoshop help for more information.
        """
        ...

