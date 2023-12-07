
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from .psmeasurementrange import PsMeasurementRange

class MeasurementLog():
    """
    The measurement log for the application. See MeasurementLog (in the Properties table for the Application object.)Note: The MeasurementLog feature is available in the Extended Version only.Because the MeasurementLog class is a property of the Application object, you use the property name, measurementLog , rather than the class name, MeasurementLog , in your code.
    """
    def ExportMeasurements(self, File, Range) -> None:
        """
        Export some measurement(s).
        """
        ...

    def DeleteMeasurements(self, Range:PsMeasurementRange) -> None:
        """
        Delete a measurement.
        """
        ...

