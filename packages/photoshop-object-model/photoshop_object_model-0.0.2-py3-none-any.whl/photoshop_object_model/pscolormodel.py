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

class PsBMPDepthType():
    """
    The number of bits per channel (also called pixel depth or color depth). The number selected indicates the exponent of 2. For example, a pixel with a bit-depth of 8 has 28, or 256, possible color values.
    """
    psBMP1Bit = 1
    psBMP4Bits = 4
    psBMP8Bits = 8
    psBMP16Bits = 16
    psBMP24Bits = 24
    psBMP32Bits = 32
    psBMP_X1R5G5B5 = 60
    psBMP_A1R5G5B5 = 61
    psBMP_R5G6B5 = 62
    psBMP_X4R4G4B4 = 63
    psBMP_A4R4G4B4 = 64
    psBMP_R8G8B8 = 65
    psBMP_X8R8G8B8 = 66
    psBMP_A8R8G8B8 = 67

class PsByteOrder():
    """
    The order in which bytes will be read.
    """
    psIBMByteOrder = 1
    psMacOSByteOrder = 2

class PsCameraRAWSettingsType():
    """
    The default CameraRAW settings to use: the camera settings, custom settings, or the settings of the selected image.
    """
    psCameraDefault = 0
    psSelectedImage = 1
    psCustomSettings = 2

class PsCameraRAWSize():
    """
    The camera RAW size type options: 0 = 1536 x 1024 1 = 2048 x 1365 2 = 3072 x 2048 3 = 4096 x 2731 4 = 5120 x 4096 5 = 6144 x 4096
    """
    psMinimumCameraRAW = 0
    psSmallCameraRAW = 1
    psMediumCameraRAW = 2
    psLargeCameraRAW = 3
    psExtraLargeCameraRAW = 4
    psMaximumCameraRAW = 5

class PsCase():
    """
    The case usage for type.
    """
    psNormalCase = 1
    psAllCaps = 2
    psSmallCaps = 3

class PsChangeMode():
    """
    The type of color mode to use. Note:Color images must be changed to grayscale (1) mode before you can change them to bitmap (5) mode.
    """
    psConvertToGrayscale = 1
    psConvertToRGB = 2
    psConvertToCMYK = 3
    psConvertToLab = 4
    psConvertToBitmap = 5
    psConvertToIndexedColor = 6
    psConvertToMultiChannel = 7

class PsChannelType():
    """
    The type of channel: 1: related to document color mode; 2: Alpha channel where color indicates masked area; 3: Alpha channel where color indicates selected area; 4: channel that contains spot colors.
    """
    psComponentChannel = 1
    psMaskedAreaAlphaChannel = 2
    psSelectedAreaAlphaChannel = 3
    psSpotColorChannel = 4

class PsColorBlendMode():
    """
    Controls how pixels in the image are blended.
    """
    psNormalBlendColor = 2
    psDissolveBlend = 3
    psDarkenBlend = 4
    psMultiplyBlend = 5
    psColorBurnBlend = 6
    psLinearBurnBlend = 7
    psLightenBlend = 8
    psScreenBlend = 9
    psColorDodgeBlend = 10
    psLinearDodgeBlend = 11
    psOverlayBlend = 12
    psSoftLightBlend = 13
    psHardLightBlend = 14
    psVividLightBlend = 15
    psLinearLightBlend = 16
    psPinLightBlend = 17
    psDifferenceBlend = 18
    psExclusionBlend = 19
    psHueBlend = 20
    psClearBlend = 25
    psHardMixBlend = 26
    psSubtract = 27
    psDivide = 28

class PsColorModel():
    """
    The color model to use.
    """
    psGrayscaleModel = 1
    psRGBModel = 2
    psCMYKModel = 3
    psLabModel = 4
    psHSBModel = 5
    psNoModel = 50

