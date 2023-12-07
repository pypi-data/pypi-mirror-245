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

class PsBatchDestinationType():
    """
    The destination, if any, for batch-processed files: 1: Leave all files open; 2: Save changes and close the files; 3: Save modified versions of the files to a new location (leaving the originals unchanged).
    """
    psNoDestination = 1
    psSaveAndClose = 2
    psFolder = 3

class PsBitmapConversionType():
    """
    Specifies the quality of an image you are converting to bitmap mode.
    """
    psHalfThreshold = 1
    psPatternDither = 2
    psDiffusionDither = 3
    psHalftoneScreen = 4
    psCustomPattern = 5

class PsBitmapHalfToneType():
    """
    Specifies the shape of the dots (ink deposits) in the halftone screen.
    """
    psHalftoneRound = 1
    psHalftoneDiamond = 2
    psHalftoneEllipse = 3
    psHalftoneLine = 4
    psHalftoneSquare = 5
    psHalftoneCross = 6

class PsBitsPerChannelType():
    """
    The number of bits per color channel.
    """
    psDocument1Bit = 1
    psDocument8Bits = 8
    psDocument16Bits = 16
    psDocument32Bits = 32

class PsBlendMode():
    """
    Controls how pixels in the image are blended.
    """
    psPassThrough = 1
    psNormalBlend = 2
    psDissolve = 3
    psDarken = 4
    psMultiply = 5
    psColorBurn = 6
    psLinearBurn = 7
    psLighten = 8
    psScreen = 9
    psColorDodge = 10
    psLinearDodge = 11
    psOverlay = 12
    psSoftLight = 13
    psHardLight = 14
    psVividLight = 15
    psLinearLight = 16
    psPinLight = 17
    psDifference = 18
    psExclusion = 19
    psHue = 20
    psSaturationBlend = 21
    psColorBlend = 22
    psLuminosity = 23
    psHardMix = 26
    psLighterColor = 27
    psDarkerColor = 28
    psSubtract = 29
    psDivide = 30

