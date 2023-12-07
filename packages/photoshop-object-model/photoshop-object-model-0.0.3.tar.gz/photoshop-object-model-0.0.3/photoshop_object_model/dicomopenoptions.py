
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .application import Application

class DICOMOpenOptions():
    """
    Options that can be specified when opening a DICOM format document. Note:DICOMOpenOptions is available in the Extended Version only.
    """
    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def Anonymize(self) -> bool:
        """
        Read-write. Indicates whether to make the patient information anonymous.
        """
        ...

    @property
    def Columns(self) -> int:
        """
        Read-write. Number of columns in n-up configuration.
        """
        ...

    @property
    def Reverse(self) -> bool:
        """
        Read-write. Indicates whether to reverse (invert) the image.
        """
        ...

    @property
    def Rows(self) -> int:
        """
        Read-write. The number of rows in n-up configuration.
        """
        ...

    @property
    def ShowOverlays(self) -> bool:
        """
        Read-write. Indicates whether to show overlays.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced DICOMOpenOptions object.
        """
        ...

    @property
    def WindowLevel(self) -> int:
        """
        Read-write. The contrast of the image in Houndsfield units.
        """
        ...

    @property
    def WindowWidth(self) -> int:
        """
        Read-write. The brightness of the image in Houndsfield units.
        """
        ...

