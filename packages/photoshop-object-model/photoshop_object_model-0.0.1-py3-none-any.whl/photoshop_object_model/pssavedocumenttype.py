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

class PsMagnificationType():
    """
    The type of magnification to use when viewing an image.
    """
    psActualSize = 0
    psFitPage = 1

class PsMatteType():
    """
    The color to use for matting.
    """
    psNoMatte = 1
    psForegroundColorMatte = 2
    psBackgroundColorMatte = 3
    psWhiteMatte = 4
    psBlackMatte = 5
    psSemiGray = 6
    psNetscapeGrayMatte = 7

class PsMeasurementRange():
    """
    The measurement to take action upon
    """
    psAllMeasurements = 1
    psActiveMeasurements = 2

class PsMeasurementSource():
    """
    The source for recording measurements
    """
    psMeasureSelection = 1
    psMeasureCountTool = 2
    psMeasureRulerTool = 3

class PsNewDocumentMode():
    """
    The color profile to use for the document.
    """
    psNewGray = 1
    psNewRGB = 2
    psNewCMYK = 3
    psNewLab = 4
    psNewBitmap = 5

class PsNoiseDistribution():
    """
    Distribution method to use when applying an Add Noise filter.
    """
    psUniformNoise = 1
    psGaussianNoise = 2

class PsOffsetUndefinedAreas():
    """
    Method to use to fill the empty space left by offsetting a an image or selection.
    """
    psOffsetSetToLayerFill = 1
    psOffsetWraparound = 2
    psOffsetRepeatEdgePixels = 3

class PsOpenDocumentMode():
    """
    The color profile to use.
    """
    psOpenGray = 1
    psOpenRGB = 2
    psOpenCMYK = 3
    psOpenLab = 4

class PsOpenDocumentType():
    """
    The format in which to open a document. Note: psPhotoCDOpen (8) is deprecated. Kodak PhotoCD is now found in the Goodies folder on the Adobe Photoshop Install DVD. Note:The psDICOMOpen (33) option is for the Extended version only.
    """
    psPhotoshopOpen = 1
    psBMPOpen = 2
    psCompuServeGIFOpen = 3
    psPhotoshopEPSOpen = 4
    psFilmstripOpen = 5
    psJPEGOpen = 6
    psPCXOpen = 7
    psPhotoshopPDFOpen = 8
    psPhotoCDOpen = 9
    psPICTFileFormatOpen = 10
    psPICTResourceFormatOpen = 11
    psPixarOpen = 12
    psPNGOpen = 13
    psRawOpen = 14
    psScitexCTOpen = 15
    psTargaOpen = 16
    psTIFFOpen = 17
    psPhotoshopDCS_1Open = 18
    psPhotoshopDCS_2Open = 19
    psPDFOpen = 21
    psEPSOpen = 22
    psEPSPICTPreviewOpen = 23
    psEPSTIFFPreviewOpen = 24
    psAliasPIXOpen = 25
    psElectricImageOpen = 26
    psPortableBitmapOpen = 27
    psWavefrontRLAOpen = 28
    psSGIRGBOpen = 29
    psSoftImageOpen = 30
    psWirelessBitmapOpen = 31
    psCameraRAWOpen = 32
    psDICOMOpen = 33

class PsOperatingSystem():
    """
    The operating system.
    """
    psOS2 = 1
    psWindows = 2

class PsOrientation():
    """
    The page orientation.
    """
    psLandscape = 1
    psPortrait = 2

class PsOtherPaintingCursors():
    """
    The pointer for the following tools: Eraser, Pencil, Paintbrush, Healing Brush, Rubber Stamp, Pattern Stamp, Smudge, Blur, Sharpen, Dodge, Burn, Sponge.
    """
    psStandardOther = 1
    psPreciseOther = 2

class PsPaintingCursors():
    """
    The pointer for the following tools: Marquee, Lasso, Polygonal Lasso, Magic Wand, Crop, Slice, Patch Eyedropper, Pen, Gradient, Line, Paint Bucket, Magnetic Lasso, Magnetic Pen, Freeform Pen, Measure, Color Sampler.
    """
    psStandard = 1
    psPrecise = 2
    psBrushsize = 3

class PsPaletteType():
    """
    The palette type to use.
    """
    psExact = 1
    psMacOSPalette = 2
    psUniform = 5
    psLocalPerceptual = 6
    psLocalSelective = 7
    psLocalAdaptive = 8
    psMasterPerceptual = 9
    psMasterSelective = 10
    psMasterAdaptive = 11
    psPreviousPalette = 12

class PsPathKind():
    """
    The type of path.
    """
    psNormalPath = 1
    psClippingPath = 2
    psWorkPath = 3
    psVectorMask = 4
    psTextMask = 5

class PsPDFCompatibilityType():
    """
    The PDF version to make the document compatible with.
    """
    psPDF13 = 1
    psPDF14 = 2
    psPDF15 = 3
    psPDF16 = 4

class PsPDFEncoding():
    """
    Encoding and compression options to use when saving a document in PDF format.
    """
    psPDFNone = 0
    psPDFZip = 1
    psPDFJPEG = 2
    psPDFPDFZip4Bit = 3
    psPDFJPEGHIGH = 4
    psPDFJPEGMEDHIGH = 5
    psPDFJPEGMED = 6
    psPDFJPEGMEDLOW = 7
    psPDFJPEGLOW = 8
    psPDFJPEG2000High = 9
    psPDFJPEG2000MEDHIGH = 10
    psPDFJPEG2000MED = 11
    psPDFJPEG2000MEDLOW = 12
    psPDFJPEG2000LOW = 13
    psPDFJPEG2000LOSSLESS = 14

class PsPDFResampleType():
    """
    The down sample method to use.
    """
    psNoResample = 0
    psPDFAverage = 1
    psPDFSubSample = 2
    psPDFBicubic = 3

class PsPDFStandardType():
    """
    The PDF standard to make the document compatible with.
    """
    psNoStandard = 0
    psPDFX1A2001 = 1
    psPDFX1A2003 = 2
    psPDFX32002 = 3
    psPDFX32003 = 4

class PsPhotoCDColorSpace():
    """
    The color space to use when creating a Photo CD. Note:Deprecated for Adobe Photoshop. Kodak PhotoCD is now found in the Goodies folder on the Adobe Photoshop Install DVD.
    """
    psRGB8 = 1
    psRGB16 = 2
    psLab8 = 3
    psLab16 = 4

class PsPhotoCDSize():
    """
    The pixel dimensions of the image. psMinimumPhotoCD = 64x96 psSmallPhotoCD = 128x192 psMediumPhotoCD = 256x384 psLargePhotoCD = 512x768 psExtralargePhotoCD = 1024x1536 psMaximumPhotoCD = 2048x3072 Note:Deprecated for Adobe Photoshop. Kodak PhotoCD is now found in the Goodies folder on the Adobe Photoshop Install DVD.
    """
    psMinimumPhotoCD = 1
    psSmallPhotoCD = 2
    psMediumPhotoCD = 3
    psLargePhotoCD = 4
    psExtralargePhotoCD = 5
    psMaximumPhotoCD = 6

class PsPICTBitsPerPixels():
    """
    The number of bits per pixel to use when compression a PICT file. Note:Use 16 or 32 for RGB images; use 2, 4, or 8 for bitmap and grayscale images.
    """
    psPICTTwoBits = 2
    psPICTFourBits = 4
    psPICTEightBits = 8
    psPICTSixteenBits = 16
    psPICTThirtyTwoBits = 32

class PsPICTCompression():
    """
    The type of compression to use when saving an image as a PICT file.
    """
    psNoPICTCompression = 1
    psJPEGLowPICT = 2
    psJPEGMediumPICT = 4
    psJPEGHighPICT = 5
    psJPEGMaximumPICT = 6

class PsPicturePackageTextType():
    """
    The function or meaning of text in a Picture Package.
    """
    psNoText = 1
    psUserText = 2
    psFilenameText = 3
    psCopyrightText = 4
    psCaptionText = 5
    psCreditText = 6
    psOriginText = 7

class PsPointKind():
    """
    The role a PathPoint plays in a PathItem.
    """
    psSmoothPoint = 1
    psCornerPoint = 2

class PsPointType():
    """
    The kind of measurement to use for type points: 1 = 72 points/inch; 2 = 72.27 points/inch.
    """
    psPostScriptPoints = 1
    psTraditionalPoints = 2

class PsPolarConversionType():
    """
    The method of polar distortion to use.
    """
    psRectangularToPolar = 1
    psPolarToRectangular = 2

class PsPreviewType():
    """
    The type of image to use as a low-resolution preview in the destination application.
    """
    psNoPreview = 1
    psMonochromeTIFF = 2
    psEightbitTIFF = 3

class PsPurgeTarget():
    """
    Cache to be targeted in a purge operation.
    """
    psUndoCaches = 1
    psHistoryCaches = 2
    psClipboardCache = 3
    psAllCaches = 4

class PsQueryStateType():
    """
    Permission state for queries.
    """
    psAlways = 1
    psAsk = 2
    psNever = 3

class PsRadialBlurMethod():
    """
    The blur method to use.
    """
    psSpin = 1
    psZoom = 2

class PsRadialBlurQuality():
    """
    The smoothness or graininess of the blurred image.
    """
    psRadialBlurDraft = 1
    psRadialBlurGood = 2
    psRadialBlurBest = 3

class PsRasterizeType():
    """
    The layer element to rasterize.
    """
    psTextContents = 1
    psShape = 2
    psFillContent = 3
    psLayerClippingPath = 4
    psEntireLayer = 5
    psLinkedLayers = 6

class PsReferenceFormType():
    """
    The type of an ActionReference object.
    """
    psReferenceNameType = 1
    psReferenceIndexType = 2
    psReferenceIdentifierType = 3
    psReferenceOffsetType = 4
    psReferenceEnumeratedType = 5
    psReferencePropertyType = 6
    psReferenceClassType = 7

class PsResampleMethod():
    """
    The method to use for image interpolation.
    """
    psNoResampling = 1
    psNearestNeighbor = 2
    psBilinear = 3
    psBicubic = 4
    psBicubicSharper = 5
    psBicubicSmoother = 6
    psBicubicAutomatic = 7
    psAutomatic = 8
    psPreserveDetails = 9

class PsRippleSize():
    """
    The undulation size to use.
    """
    psSmallRipple = 1
    psMediumRipple = 2
    psLargeRipple = 3

class PsSaveBehavior():
    """
    The application’s behavior when a Save method is called.
    """
    psNeverSave = 1
    psAlwaysSave = 2
    psAskWhenSaving = 3

class PsSaveDocumentType():
    """
    The format in which to save a document.
    """
    psPhotoshopSave = 1
    psBMPSave = 2
    psCompuServeGIFSave = 3
    psPhotoshopEPSSave = 4
    psJPEGSave = 6
    psPCXSave = 7
    psPhotoshopPDFSave = 8
    psPICTFileFormatSave = 10
    psPixarSave = 12
    psPNGSave = 13
    psRawSave = 14
    psScitexCTSave = 15
    psTargaSave = 16
    psTIFFSave = 17
    psPhotoshopDCS_1Save = 18
    psPhotoshopDCS_2Save = 19
    psAliasPIXSave = 25
    psElectricImageSave = 26
    psPortableBitmapSave = 27
    psWavefrontRLASave = 28
    psSGIRGBSave = 29
    psSoftImageSave = 30
    psWirelessBitmapSave = 31

