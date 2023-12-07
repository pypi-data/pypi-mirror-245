
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .psurgency import PsUrgency
    from .application import Application
    from .document import Document
    from .pscopyrightedtype import PsCopyrightedType

class DocumentInfo():
    """
    Metadata about a Document object. These values can be set by choosing File > File Info in the Adobe Photoshop application. Note: The DocumentInfo object corresponds to the Info property of the Application object. You use the property name Info , rather thanthe object name, DocumentInfo , in a script, as in the following sample, which sets the Author , Caption , and Copyrighted properties:Dim docRefdocRef = Open(fileList[i])' set the file infodocRef.Info.Author = "Mr. Adobe Programmer"docRef.Info.Caption = "Adobe photo shoot"docRef.Info.Copyrighted = 1The following sample uses the DocumentInfo object incorrectly:docRef.DocumentInfo.Author = "Mr. Adobe Programmer"docRef.DocumentInfo.Caption = "Adobe photo shoot"docRef.DocumentInfo.Copyrighted = 1
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Author(self) -> str:
        """
        Read-write.
        """
        ...

    @property
    def authorPosition(self) -> str:
        """
        Read-write.
        """
        ...

    @property
    def Caption(self) -> str:
        """
        Read-write.
        """
        ...

    @property
    def CaptionWriter(self) -> str:
        """
        Read-write.
        """
        ...

    @property
    def Category(self) -> str:
        """
        Read-write.
        """
        ...

    @property
    def City(self) -> str:
        """
        Read-write.
        """
        ...

    @property
    def Copyrighted(self) -> PsCopyrightedType:
        """
        Read-write. The copyrighted status.
        """
        ...

    @property
    def CopyrightNotice(self) -> str:
        """
        Read-write.
        """
        ...

    @property
    def Country(self) -> str:
        """
        Read-write.
        """
        ...

    @property
    def CreationDate(self) -> str:
        """
        Read-write.
        """
        ...

    @property
    def Credit(self) -> str:
        """
        Read-write.
        """
        ...

    @property
    def EXIF(self) -> list:
        """
        Read-only. Camera data that includes camera settings used when the image was taken. Sample array values are: tag = “camera”; tag value = “Cannon”.
        """
        ...

    @property
    def Headline(self) -> str:
        """
        Read-write.
        """
        ...

    @property
    def Instructions(self) -> str:
        """
        Read-write.
        """
        ...

    @property
    def JobName(self) -> str:
        """
        Read-write.
        """
        ...

    @property
    def Keywords(self) -> List[str]:
        """
        Read-write. A list of keywords that can identify the document or its contents.
        """
        ...

    @property
    def OwnerUrl(self) -> str:
        """
        Read-write.
        """
        ...

    @property
    def Parent(self) -> Document:
        """
        Read-only. The Info object's container.
        """
        ...

    @property
    def ProvinceState(self) -> str:
        """
        Read-write.
        """
        ...

    @property
    def Source(self) -> str:
        """
        Read-write.
        """
        ...

    @property
    def SupplementalCategories(self) -> List[str]:
        """
        Read-write.
        """
        ...

    @property
    def Title(self) -> str:
        """
        Read-write.
        """
        ...

    @property
    def TransmissionReference(self) -> str:
        """
        Read-write.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced Info object.
        """
        ...

    @property
    def Urgency(self) -> PsUrgency:
        """
        Read-write.
        """
        ...

