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

class PsColorPicker():
    """
    The color picker to use.
    """
    psAdobeColorPicker = 1
    psAppleColorPicker = 2
    psWindowsColorPicker = 3
    psPlugInColorPicker = 4

class PsColorProfileType():
    """
    The color profile type to use to manage this document.
    """
    psNo = 1
    psWorking = 2
    psCustom = 3

class PsColorReductionType():
    """
    The color reduction algorithm option to use.
    """
    psPerceptualReduction = 0
    psSelective = 1
    psAdaptive = 2
    psRestrictive = 3
    psCustomReduction = 4
    psBlackWhiteReduction = 5
    psSFWGrayscale = 6
    psMacintoshColors = 7
    psWindowsColors = 8

class PsColorSpaceType():
    """
    The type of color space to use.
    """
    psAdobeRGB = 0
    psColorMatchRGB = 1
    psProPhotoRGB = 2
    psSRGB = 3

class PsCopyrightedType():
    """
    The copyright status of the document.
    """
    psCopyrightedWork = 1
    psPublicDomain = 2
    psUnmarked = 3

class PsCreateFields():
    """
    The method to use for creating fields.
    """
    psDuplication = 1
    psInterpolation = 2

class PsCropToType():
    """
    The style to use when cropping a page.
    """
    psBoundingBox = 0
    psMediaBox = 1
    psCropBox = 2
    psBleedBox = 3
    psTrimBox = 4
    psArtBox = 5

class PsDCSType():
    """
    The DCS format to use: 1: Does not create a composite file; 2: Creates a grayscale composite file in addition to DCS files; 3: Creates a color composite file in addition to DCS files.
    """
    psNoComposite = 1
    psGrayscaleComposite = 2
    psColorComposite = 3

class PsDepthMapSource():
    """
    What to use for the depth map.
    """
    psNoSource = 1
    psTransparencyChannel = 2
    psLayerMask = 3
    psImageHighlight = 4

class PsDescValueType():
    """
    The value type of an object.
    """
    psIntegerType = 1
    psDoubleType = 2
    psUnitDoubleType = 3
    psStringType = 4
    psBooleanType = 5
    psListType = 6
    psObjectType = 7
    psEnumeratedType = 8
    psReferenceType = 9
    psClassType = 10
    psAliasType = 11
    psRawType = 12
    psLargeIntegerType = 13

class PsDialogModes():
    """
    Controls the type (mode) of dialogs Photoshop displays when running scripts.
    """
    psDisplayAllDialogs = 1
    psDisplayErrorDialogs = 2
    psDisplayNoDialogs = 3

class PsDirection():
    """
    The orientation of the object.
    """
    psHorizontal = 1
    psVertical = 2

class PsDisplacementMapType():
    """
    Describes how the displacement map fits the image if the image is not the same size as the map.
    """
    psStretchToFit = 1
    psTile = 2

class PsDitherType():
    """
    The default type of dithering to use.
    """
    psNoDither = 1
    psDiffusion = 2
    psPattern = 3
    psNoise = 4

class PsDocumentFill():
    """
    The fill of the document.
    """
    psWhite = 1
    psBackgroundColor = 2
    psTransparent = 3

class PsDocumentMode():
    """
    The color mode of the open document.
    """
    psGrayscale = 1
    psRGB = 2
    psCMYK = 3
    psLab = 4
    psBitmap = 5
    psIndexedColor = 6
    psMultiChannel = 7
    psDuotone = 8

class PsEditLogItemsType():
    """
    The history log edit options: 1: Save history log only for the session; 2: Save a concise history log; 3: Save a detailed history log.
    """
    psSessionOnly = 1
    psConcise = 2
    psDetailed = 3

class PsElementPlacement():
    """
    The object’s position in the Layers palette. Note:Not all values are valid for all object types. Please refer to the object property definition in VBScript Interface to make sure you are using a valid value.
    """
    psPlaceInside = 0
    psPlaceAtBeginning = 1
    psPlaceAtEnd = 2
    psPlaceBefore = 3
    psPlaceAfter = 4

class PsEliminateFields():
    """
    The type of fields to eliminate.
    """
    psOddFields = 1
    psEvenFields = 2

class PsExportType():
    """
    The export options to use.
    """
    psIllustratorPaths = 1
    psSaveForWeb = 2

class PsExtensionType():
    """
    The formatting of the extension in the filename.
    """
    psLowercase = 2
    psUppercase = 3

class PsFileNamingType():
    """
    File naming options for the batch command.
    """
    psDocumentNameMixed = 1
    psDocumentNameLower = 2
    psDocumentNameUpper = 3
    psSerialNumber1 = 4
    psSerialNumber2 = 5
    psSerialNumber3 = 6
    psSerialNumber4 = 7
    psSerialLetterLower = 8
    psSerialLetterUpper = 9
    psMmddyy = 10
    psMmdd = 11
    psYyyymmdd = 12
    psYymmdd = 13
    psYyddmm = 14
    psDdmmyy = 15
    psDdmm = 16
    psExtensionLower = 17
    psExtensionUpper = 18

class psFontPreviewType():
    """
    The type size to use for font previews in the type tool font menus.
    """
    psFontPreviewNone = 0
    psFontPreviewSmall = 1
    psFontPreviewMedium = 2
    psFontPreviewLarge = 3
    psFontPreviewExtraLarge = 4
    psFontPreviewHuge = 5

class PsForcedColors():
    """
    The type of colors to be forced (included) into the color table: 2: Pure black and pure white; 3: Red, green, blue, cyan, magenta, yellow, black, and white; 4: the 216 web-safe colors.
    """
    psNoForced = 1
    psBlackWhite = 2
    psPrimaries = 3
    psWeb = 4

class PsFormatOptionsType():
    """
    The option with which to save a JPEG file: 1: Format recognized by most web browsers; 2: Optimized color and a slightly reduced file size; 3: Displays a series of increasingly detailed scans as the image downloads.
    """
    psStandardBaseline = 1
    psOptimizedBaseline = 2
    psProgressive = 3

class PsGalleryConstrainType():
    """
    The type of proportions to constrain for images.
    """
    psConstrainWidth = 1
    psConstrainHeight = 2
    psConstrainBoth = 3

class PsGalleryFontType():
    """
    The fonts to use for the Web photo gallery captions and other text.
    """
    psArial = 1
    psCourierNew = 2
    psHelvetica = 3
    psTimesNewRoman = 4

class PsGallerySecurityTextPositionType():
    """
    The position of the text displayed over gallery images as an antitheft deterrent.
    """
    psCentered = 1
    psUpperLeft = 2
    psLowerLeft = 3
    psUpperRight = 4
    psLowerRight = 5

class PsGallerySecurityTextRotateType():
    """
    The orientation of the text displayed over gallery images as an antitheft deterrent.
    """
    psZero = 1
    psClockwise45 = 2
    psClockwise90 = 3
    psCounterClockwise45 = 4
    psCounterClockwise90 = 5

class PsGallerySecurityType():
    """
    The content to use for text displayed over gallery images as an antitheft deterrent. Note:All types draw from the image’s file information except 2.
    """
    psNoSecurity = 1
    psCustomSecurityText = 2
    psFilename = 3
    psCopyright = 4
    psCaption = 5
    psCredit = 6
    psTitle = 7

class PsGalleryThumbSizeType():
    """
    The size of thumbnail images in the web photo gallery.
    """
    psSmall = 1
    psMedium = 2
    psLarge = 3
    psCustomThumbnail = 4

class PsGeometry():
    """
    Geometric options for shapes, such as the iris shape in the Lens Blur Filter.
    """
    psTriangle = 0
    psPentagon = 1
    psHexagon = 2
    psSquareGeometry = 3
    psHeptagon = 4
    psOctagon = 5

class PsGridLineStyle():
    """
    The line style for the nonprinting grid displayed over images.
    """
    psGridSolidLine = 1
    psGridDashedLine = 2
    psGridDottedLine = 3

class PsGridSize():
    """
    The value of grid line spacing.
    """
    psNoGrid = 1
    psSmallGrid = 2
    psMediumGrid = 3
    psLargeGrid = 4

class PsGuideLineStyle():
    """
    The line style for nonprinting guides displayed over images.
    """
    psGuideSolidLine = 1
    psGuideDashedLine = 2

class PsIllustratorPathType():
    """
    The paths to export.
    """
    psDocumentBounds = 1
    psAllPaths = 2
    psNamedPath = 3

class PsIntent():
    """
    The rendering intent to use when converting from one color space to another.
    """
    psPerceptual = 1
    psSaturation = 2
    psRelativeColorimetric = 3
    psAbsoluteColorimetric = 4

class PsJavaScriptExecutionMode():
    """
    The debugging behavior to use when executing a JavaScript.
    """
    psNeverShowDebugger = 1
    psDebuggerOnError = 2
    psBeforeRunning = 3

class PsJustification():
    """
    The placement of paragraph text within the bounding box.
    """
    psLeft = 1
    psCenter = 2
    psRight = 3
    psLeftJustified = 4
    psCenterJustified = 5
    psRightJustified = 6
    psFullyJustified = 7

class PsLanguage():
    """
    The language to use.
    """
    psEnglishUSA = 1
    psEnglishUK = 2
    psFrench = 3
    psCanadianFrench = 4
    psFinnish = 5
    psGerman = 6
    psOldGerman = 7
    psSwissGerman = 8
    psItalian = 9
    psNorwegian = 10
    psNynorskNorwegian = 11
    psPortuguese = 12
    psBrazillianPortuguese = 13
    psSpanish = 14
    psSwedish = 15
    psDutch = 16
    psDanish = 17

class PsLayerCompressionType():
    """
    Compression methods for data for pixels in layers.
    """
    psRLELayerCompression = 1
    psZIPLayerCompression = 2

class PsLayerKind():
    """
    The kind of ArtLayer object.
    """
    psNormalLayer = 1
    psTextLayer = 2
    psSolidFillLayer = 3
    psGradientFillLayer = 4
    psPatternfillLayer = 5
    psLevelsLayer = 6
    psCurvesLayer = 7
    psColorBalanceLayer = 8
    psBrightnessContrastLayer = 9
    psHueSaturationLayer = 10
    psSelectiveColorLayer = 11
    psChannelMixerLayer = 12
    psGradientMapLayer = 13
    psInversionLayer = 14
    psThresholdLayer = 15
    psPosterizeLayer = 16
    psSmartObjectLayer = 17
    psPhotoFilterLayer = 18
    psExposureLayer = 19
    psLayer3D = 20
    psVideoLayer = 21
    psBlackAndWhiteLayer = 22
    psVibrance = 23

class PsLayerType():
    """
    The kind of layer object.
    """
    psArtLayer = 1
    psLayerSet = 2

class PsLensType():
    """
    The type of lens to use.
    """
    psZoomLens = 1
    psPrime35 = 2
    psPrime105 = 3
    psMoviePrime = 5

