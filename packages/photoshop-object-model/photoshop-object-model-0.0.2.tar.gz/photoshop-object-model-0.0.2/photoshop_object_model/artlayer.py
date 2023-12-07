
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from pszigzagtype import PsZigZagType
    from psoffsetundefinedareas import PsOffsetUndefinedAreas
    from psanchorposition import PsAnchorPosition
    from pscreatefields import PsCreateFields
    from artlayer import ArtLayer
    from application import Application
    from psripplesize import PsRippleSize
    from pspolarconversiontype import PsPolarConversionType
    from psspherizemode import PsSpherizeMode
    from layerset import LayerSet
    from pssmartblurquality import PsSmartBlurQuality
    from pselementplacement import PsElementPlacement
    from textitem import TextItem
    from document import Document
    from psrasterizetype import PsRasterizeType
    from psblendmode import PsBlendMode
    from pslayerkind import PsLayerKind
    from psadjustmentreference import PsAdjustmentReference
    from pssmartblurmode import PsSmartBlurMode
    from pseliminatefields import PsEliminateFields
    from pslenstype import PsLensType
    from xmpmetadata import XMPMetadata

class ArtLayer():
    """
    An object within a document that contains the visual elements of the image (equivalent to a layer in the Adobe Photoshop application).
    """
    @property
    def AllLocked(self) -> bool:
        """
        Read-write. Indicates whether to completely lock the layer’s contents and settings.
        """
        ...

    @property
    def Application(self) -> Application:
        """
        Read-only. The application that this art layer belongs to.
        """
        ...

    @property
    def BlendMode(self) -> PsBlendMode:
        """
        Read-write. The layer’s blending mode.
        """
        ...

    @property
    def Bounds(self) -> list:
        """
        Read-only. An array of coordinates that describes the bounding rectangle of the ArtLayer.
        """
        ...

    @property
    def BoundsNoEffects(self) -> list:
        """
        Read-only. An array of coordinates that describes the bounding rectangle of the ArtLayer not including effects.
        """
        ...

    @property
    def FillOpacity(self) -> float:
        """
        Read-write. The interior opacity of the layer (0.0 - 100.0).
        """
        ...

    @property
    def Grouped(self) -> bool:
        """
        Read-write. Indicates whether to group this layer with the layer beneath it.
        """
        ...

    @property
    def IsBackgroundLayer(self) -> bool:
        """
        Read-write. Indicates whether the layer is a background layer or normal layer. Note:A document can have only one background layer.
        """
        ...

    @property
    def Kind(self) -> PsLayerKind:
        """
        Read-write. Sets the layer’s kind (such as 'text layer') for an empty layer. Note:Valid only when the layer is empty and when IsBackgroundLayer is false. See IsBackgroundLayer. Note:You can use the kind property to make a background layer a normal layer; however, to make a layer a background layer, you must set IsBackgroundLayer to true.
        """
        ...

    @property
    def LinkedLayers(self) -> List[ArtLayer|LayerSet]:
        """
        Read-only. The layers linked to this layer. Note:See Link.
        """
        ...

    @property
    def Name(self) -> str:
        """
        Read-write. The layer’s name.
        """
        ...

    @property
    def Opacity(self) -> float:
        """
        Read-write. The master opacity of the layer (0.0 - 100.0).
        """
        ...

    @property
    def Parent(self) -> Document:
        """
        Read-only. The object's container.
        """
        ...

    @property
    def PixelsLocked(self) -> bool:
        """
        Read-write. Indicates whether the pixels in the layer’s image can be edited using the paintbrush tool.
        """
        ...

    @property
    def PositionLocked(self) -> bool:
        """
        Read-write. Indicates whether the pixels in the layer’s image can be moved within the layer.
        """
        ...

    @property
    def TextItem(self) -> TextItem:
        """
        Read-only. The text item that is associated with the layer. Note:Valid only when Kind = 2. See Kind.
        """
        ...

    @property
    def TransparentPixelsLocked(self) -> bool:
        """
        Read-write. Indicates whether editing is confined to the opaque portions of the layer.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced ArtLayer object.
        """
        ...

    @property
    def Visible(self) -> bool:
        """
        Read-write. Indicates whether the layer is visible.
        """
        ...

    @property
    def XMPMetadata(self) -> XMPMetadata:
        """
        Read-only. XMP data for the layer.
        """
        ...

    def AdjustBrightnessContrast(self, Brightness:int, Contrast:int) -> None:
        """
        Adjusts the brightness (-100 - 100) and contrast (-100 - 100).
        """
        ...

    def AdjustColorBalance(self, Shadows, Midtones, Highlights, PreserveLuminosity) -> None:
        """
        Adjusts the color balance of the layer’s component channels. For Shadows, Midtones, and Highlights, the array must include three values (-100 - 100), which represent cyan or red, magenta or green, and yellow or blue, when the document mode is CMYK or RGB. Note:See mode in the Properties table of the Document object.
        """
        ...

    def AdjustCurves(self, CurveShape) -> None:
        """
        Adjusts the tonal range of the selected channel using up to fourteen points.
        """
        ...

    def AdjustLevels(self, InputRangeStart:int, InputRangeEnd:int, InputRangeGamma:float, OutputRangeStart:int, OutputRangeEnd:int) -> None:
        """
        Adjusts the levels of the selected channels (InputRangeStart: 0 - 253; InputRangeEnd: (InputRangeStart + 2) - 255; InputRangeGamma: 0.10 - 9.99; OutputRangeStart: 0 - 253; OutputRangeEnd: (OutputRangeStart + 2) - 255.
        """
        ...

    def ApplyAddNoise(self, Amount, Distribution, Monochromatic) -> None:
        """
        Applies the Add Noise filter (Amount: 0.1 - 400, as a percentage).
        """
        ...

    def ApplyAverage(self) -> None:
        """
        Applies the Average filter.
        """
        ...

    def ApplyBlur(self) -> None:
        """
        Applies the Blur filter.
        """
        ...

    def ApplyBlurMore(self) -> None:
        """
        Applies the Blur More filter.
        """
        ...

    def ApplyClouds(self) -> None:
        """
        Applies the Clouds filter.
        """
        ...

    def ApplyCustomFilter(self, Characteristics:List[int], Scale:int, Offset:int) -> None:
        """
        Applies a custom filter. Note:Required parameter values define the filter. Refer to Adobe Photoshop Help for specific instructions.
        """
        ...

    def ApplyDeInterlace(self, EliminateFields:PsEliminateFields, CreateFields:PsCreateFields) -> None:
        """
        Applies the De-Interlace filter.
        """
        ...

    def ApplyDespeckle(self) -> None:
        """
        Applies the Despeckle filter.
        """
        ...

    def ApplyDifferenceClouds(self) -> None:
        """
        Applies the Difference Clouds filter.
        """
        ...

    def ApplyDiffuseGlow(self, Graininess:int, GlowAmount:int, ClearAmount:int) -> None:
        """
        Applies the Diffuse Glow filter (Graininess: 0 - 10; GlowAmount: 0 - 20; ClearAmount: 0 - 20).
        """
        ...

    def ApplyDisplace(self, HorizontalScale, VerticalScale, DisplacementType, UndefinedAreas, DisplacementMapFiles) -> None:
        """
        Applies the Displace filter using the specified horizontal and vertical scale (-999 - 999), mapping type, treatment of undistorted areas, and path to the distortion image map.
        """
        ...

    def ApplyDustAndScratches(self, Radius:int, Threshold:int) -> None:
        """
        Applies the Dust & Scratches filter (Radius: 1 - 100; Threshold: 0 - 255).
        """
        ...

    def ApplyGaussianBlur(self, Radius:float) -> None:
        """
        Applies the Gaussian Blur filter within the specified radius (in pixels) (0.1 - 250.0).
        """
        ...

    def ApplyGlassEffect(self, Distortion, Smoothness, Scaling, Invert, Texture, TextureFile) -> None:
        """
        Applies the Glass filter (Distortion: 0 - 20; Smoothness: 1 - 15; Scaling (in percent): 50 - 200). Note:The TextureFile parameter represents the path to a texture file as a String.
        """
        ...

    def ApplyHighPass(self, Radius:float) -> None:
        """
        Applies the High Pass filter within the specified radius (in pixels) (0.1 - 250.0).
        """
        ...

    def ApplyLensBlur(self, Source, FocalDistance, InvertDepthMap, Shape, Radius, BladeCurvature, Rotation, Brightness, Threshold, Amount, Distribution, Monochromatic) -> None:
        """
        Applies the Lens Blur filter. source: the source for the depth map. Default: 1 (psNoSource). focalDistance : the blur focal distance for the depth map (default: 0). invertDepthMask : whether the depth map is inverted (default: false). shape: The shape of the iris. Default: 2 (psHexagon). radius: The radius of the iris (default: 15). bladeCurvature: The blade curvature of the iris (default: 0). rotation: The rotation of the iris (default: 0) brightness: The brightness for the specular highlights (default: 0). threshold: The threshold for the specular highlights (default: 0). amount: The amount of noise (default: 0) distribution: The distribution value for the noise. Default: 1 (psUniformNoise). monochromatic: Indicates whether the noise is monochromatic (default: false).
        """
        ...

    def ApplyLensFlare(self, Brightness:int, FlareCenter:List[float], LensType:PsLensType) -> None:
        """
        Applies the Lens Flare filter with the specified brightness (0 - 300, as a percentage), the x and y coordinates (unit value) of the flare center, and the lens type.
        """
        ...

    def ApplyMaximum(self, Radius:float) -> None:
        """
        Applies the Maximum filter within the specified radius (in pixels) (1 - 100).
        """
        ...

    def ApplyMedianNoise(self, Radius:float) -> None:
        """
        Applies the Median Noise filter within the specified radius (in pixels) (1 - 100).
        """
        ...

    def ApplyMinimum(self, Radius:float) -> None:
        """
        Applies the Minimum filter within the specified radius (in pixels) (1 - 100).
        """
        ...

    def ApplyMotionBlur(self, Angle:int, Radius:float) -> None:
        """
        Applies the Motion Blur filter (Angle: -360 - 360; Radius: 1 - 999).
        """
        ...

    def ApplyNTSC(self) -> None:
        """
        Applies the NTSC colors filter.
        """
        ...

    def ApplyOceanRipple(self, Size:int, Magnitude:int) -> None:
        """
        Applies the Ocean Ripple filter in the specified size (1 - 15) and magnitude (0 - 20).
        """
        ...

    def ApplyOffset(self, Horizontal:float, Vertical:float, UndefinedAreas:PsOffsetUndefinedAreas) -> None:
        """
        Moves the layer the specified amount horizontally and vertically (min/max amounts depend on layer size), leaving an undefined area at the layer’s original location.
        """
        ...

    def ApplyPinch(self, Amount:int) -> None:
        """
        Applies the Pinch filter in the specified amount (as a percentage) (-100 - 100).
        """
        ...

    def ApplyPolarCoordinates(self, Conversion:PsPolarConversionType) -> None:
        """
        Applies the Polar Coordinates filter.
        """
        ...

    def ApplyRadialBlur(self, Amount, BlurMethod, BlurQuality, BlurCenter) -> None:
        """
        Applies the Radial Blur filter in the specified amount (1 - 100) using either a spin or zoom effect and the specified quality. The parameter BlurCenter is the position (unit value).
        """
        ...

    def ApplyRipple(self, Amount:int, Size:PsRippleSize) -> None:
        """
        Applies the Ripple filter in the specified amount (-999 to 999) throughout the image and in the specified size.
        """
        ...

    def ApplySharpen(self) -> None:
        """
        Applies the Sharpen filter.
        """
        ...

    def ApplySharpenEdges(self) -> None:
        """
        Applies the Sharpen Edges filter.
        """
        ...

    def ApplySharpenMore(self) -> None:
        """
        Applies the Sharpen More filter.
        """
        ...

    def ApplyShear(self, Curve, UndefinedAreas) -> None:
        """
        Applies the Shear filter (curve: 2 - 255 points). Note:You must define at least two points in the Curve parameter.
        """
        ...

    def ApplySmartBlur(self, Radius:float, Threshold:float, BlurQuality:PsSmartBlurQuality, Mode:PsSmartBlurMode) -> None:
        """
        Applies the smart blur filter (Radius: 0.1 - 100.0; Threshold: 0.1 - 100.0).
        """
        ...

    def ApplySpherize(self, Amount:int, Mode:PsSpherizeMode) -> None:
        """
        Applies the Spherize filter in the specified amount (as percentage) (-100 - 100).
        """
        ...

    def ApplyStyle(self, StyleName:str) -> None:
        """
        Applies the specified style to the layer. Note:You must use a style from the Styles list in the Layer Style dialog.
        """
        ...

    def ApplyTextureFill(self, TextureFile:str) -> None:
        """
        Applies the Texture Fill filter.
        """
        ...

    def ApplyTwirl(self, Angle:int) -> None:
        """
        Applies the Twirl filter at the specified angle (-999 - 999).
        """
        ...

    def ApplyUnSharpMask(self, Amount:float, Radius:float, Threshold:int) -> None:
        """
        Applies the Unsharp Mask filter (Amount: 1 - 500 as percent; Radius: 0.1 - 250.00; Threshold: 0 - 255).
        """
        ...

    def ApplyWave(self, GeneratorNumber, MinimumWavelength, MaximumWavelength, MinimumAmplitude, MaximumAmplitude, HorizontalScale, VerticalScale, WaveType, UndefinedAreas, RandomSeed) -> None:
        """
        Applies the Wave filter (GeneratorNumber: 1 - 999; MinimumWavelength: 1 - 998; MaximumWavelength: 2 - MinimumWavelength + 1; MinimumAmplitude: 1 - 998; MaximumAmplitude: 2 - MinimumAmplitude + 1; AmountScale: 1 - 100, as a percentage; VerticalScale: 1 - 100, as a percentage).
        """
        ...

    def ApplyZigZag(self, Amount:int, Ridges:int, Style:PsZigZagType) -> None:
        """
        Applies the Zigzag filter (Amount: -100 - 100; Ridges: 0 - 20).
        """
        ...

    def AutoContrast(self) -> None:
        """
        Adjusts the contrast of the selected channels automatically.
        """
        ...

    def AutoLevels(self) -> None:
        """
        Adjusts the levels of the selected channels using the auto levels option.
        """
        ...

    def Clear(self) -> None:
        """
        Cuts the layer without moving it to the clipboard.
        """
        ...

    def Copy(self, Merge:bool) -> None:
        """
        Copies the layer to the clipboard. When the optional argument is set to true, a merged copy is performed (that is, all visible layers are copied to the clipboard).
        """
        ...

    def Cut(self) -> None:
        """
        Cuts the layer to the clipboard.
        """
        ...

    def Desaturate(self) -> None:
        """
        Converts a color image to a grayscale image in the current color mode by assigning equal values of each component color to each pixel.
        """
        ...

    def Duplicate(self, RelativeObject:ArtLayer|LayerSet, InsertionLocation:PsElementPlacement):
        """
        Creates a duplicate of the object on the screen.
        """
        ...

    def Equalize(self) -> None:
        """
        Redistributes the brightness values of pixels in an image to more evenly represent the entire range of brightness levels within the image.
        """
        ...

    def Invert(self) -> None:
        """
        Inverts the colors in the layer by converting the brightness value of each pixel in the channels to the inverse value on the 256-step color-values scale.
        """
        ...

    def Link(self, With:ArtLayer|LayerSet) -> None:
        """
        Links the layer with the specified layer.
        """
        ...

    def Merge(self):
        """
        Merges the layer down, removing the layer from the document; returns a reference to the art layer that this layer is merged into.
        """
        ...

    def MixChannels(self, OutputChannels, Monochrome) -> None:
        """
        Modifies a targeted (output) color channel using a mix of the existing color channels in the image. (OutputChannels = An array of channel specifications. For each component channel, specify a list of adjustment values (-200 - 200) followed by a 'constant' value (-200 - 200).) Note:When Monochrome = true, the maximum number of channel value specifications is 1. Note:Valid only when Document.Mode = 2 or Document.Mode = 3. Note:RGB arrays must include four doubles. CMYK arrays must include five doubles.
        """
        ...

    def Move(self, ApplicationObject:ArtLayer|LayerSet, InsertionLocation:PsElementPlacement) -> None:
        """
        Moves the layer relative to the object specified in parameters. Note:For art layers, only the constant values 3 and 4 are valid. For layer sets, only the constant values 3 and 0 are valid.
        """
        ...

    def PhotoFilter(self, FillColor, Density, PreserveLuminosity) -> None:
        """
        Adjust the layer’s color balance and temperature as if a color filter had been applied (Density: 1 - 100, as a percentage).
        """
        ...

    def Posterize(self, Levels:int) -> None:
        """
        Specifies the number of tonal levels (2 - 255) for each channel and then maps pixels to the closest matching level.
        """
        ...

    def Rasterize(self, Target:PsRasterizeType) -> None:
        """
        Converts the targeted contents in the layer into a flat, raster image.
        """
        ...

    def Resize(self, Horizontal:float, Vertical:float, Anchor:PsAnchorPosition) -> None:
        """
        Resizes the layer to the specified dimensions (as a percentage of its current size) and places it in the specified position.
        """
        ...

    def Rotate(self, Angle:float, Anchor:PsAnchorPosition) -> None:
        """
        Rotates the layer around the specified anchor point.
        """
        ...

    def SelectiveColor(self, SelectionMethod:PsAdjustmentReference, Reds:List[int], Yellows:List[int], Greens:List[int], Cyans:List[int], Blues:List[int], Magentas:List[int], Whites:List[int], Neutrals:List[int], Blacks:List[int]) -> None:
        """
        Modifies the amount of a process color in a specified primary color without affecting the other primary colors. Note:Each color array must have four components.
        """
        ...

    def ShadowHighlight(self, ShadowAmount:int, ShadowWidth:int, ShadowRadius:int, HighlightAmount:int, HighlightWidth:int, HighlightRadius:int, ColorCorrection:int, MidtoneContrast:int, BlackClip:float, WhiteClip:float) -> None:
        """
        Adjusts the range of tones in the image’s Shadows and highlights (ShadowAmount: 0 - 100 as percent; ShadowWidth: 0 - 100 as percent; ShadowRadius: 0 - 2500 in pixels; HighlightAmount: 0 - 100 as percent; HighlightWidth: 0 - 100 as percent; HighlightRadius: 0 - 2500 in pixels; ColorCorrection: -100 - 100; MidtoneContrast: -100 - 100; BlackClip: 0.000 - 50.000; WhiteClip: 0.000 - 50.000).
        """
        ...

    def Threshold(self, Level:int) -> None:
        """
        Converts grayscale or color images to high-contrast, B/W images by converting pixels lighter than the specified threshold to white and pixels darker than the threshold to black (level: 1 - 255).
        """
        ...

    def Translate(self, DeltaX:float, DeltaY:float) -> None:
        """
        Moves the layer the specified amount (in pixels) relative to its current position.
        """
        ...

    def Unlink(self) -> None:
        """
        Unlinks the layer.
        """
        ...

