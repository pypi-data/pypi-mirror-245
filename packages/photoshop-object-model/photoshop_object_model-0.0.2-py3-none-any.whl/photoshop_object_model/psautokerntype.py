class PsAdjustmentReference():
    """
    Method to use for interpreting selective color adjustment specifications: 1 = % of the existing color amount; 2 = % of the whole.
    """
    psRelative = 1
    psAbsolute = 2

class PsAnchorPosition():
    """
    The point on the object that does not move when the object is rotated or resized.
    """
    psTopLeft = 1
    psTopCenter = 2
    psTopRight = 3
    psMiddleLeft = 4
    psMiddleCenter = 5
    psMiddleRight = 6
    psBottomLeft = 7
    psBottomCenter = 8
    psBottomRight = 9

class PsAntiAlias():
    """
    Method to use to smooth edges by softening the color transition between edge pixels and background pixels.
    """
    psNoAntialias = 1
    psSharp = 2
    psCrisp = 3
    psStrong = 4
    psSmooth = 5

class PsAutoKernType():
    """
    The type of kerning to use for characters.
    """
    psManual = 1
    psMetrics = 2
    psOptical = 3

