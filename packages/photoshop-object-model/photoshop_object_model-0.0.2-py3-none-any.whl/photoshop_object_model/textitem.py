
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from events import *
    from typing import List, Any
    from solidcolor import SolidColor
    from pscase import PsCase
    from pswarpstyle import PsWarpStyle
    from psantialias import PsAntiAlias
    from pstexttype import PsTextType
    from psautokerntype import PsAutoKernType
    from pstextcomposer import PsTextComposer
    from psunderlinetype import PsUnderlineType
    from psdirection import PsDirection
    from application import Application
    from artlayer import ArtLayer
    from pslanguage import PsLanguage
    from psjustification import PsJustification
    from psstrikethrutype import PsStrikeThruType

class TextItem():
    """
    The text in an ArtLayer object whose Kind property’s value is 2.Note: See ArtLayer , specifically the Kind property, for more information.
    """
    @property
    def AlternateLigatures(self) -> bool:
        """
        Read-write. Indicates whether to use alternate ligatures. Note:Alternate ligatures are the same as Discretionary Ligatures. Please refer to Adobe Photoshop Help for more information.
        """
        ...

    @property
    def AntiAliasMethod(self) -> PsAntiAlias:
        """
        Read-write. The method of anti aliasing to use.
        """
        ...

    @property
    def Application(self) -> Application:
        """
        Read-only. The application that the object belongs to.
        """
        ...

    @property
    def AutoKerning(self) -> PsAutoKernType:
        """
        Read-write. The auto kerning option to use.
        """
        ...

    @property
    def AutoLeadingAmount(self) -> float:
        """
        Read-write. The percentage to use for auto. Default) leading (0.01 - 5000.00 in points). Note:Valid only when UseAutoLeading = true. See UseAutoLeading.
        """
        ...

    @property
    def BaselineShift(self) -> float:
        """
        Read-write. The unit value to use in the baseline offset of text.
        """
        ...

    @property
    def Capitalization(self) -> PsCase:
        """
        Read-write. The text case.
        """
        ...

    @property
    def Color(self) -> SolidColor:
        """
        Read-write. The text color.
        """
        ...

    @property
    def Contents(self) -> str:
        """
        Read-write. The actual text in the layer.
        """
        ...

    @property
    def DesiredGlyphScaling(self) -> float:
        """
        Read-write. The desired amount (percentage) to scale the horizontal size of the text letters (50 - 200; at 100, the width of characters is not scaled). Note:Valid only when Justification = 4 (psLeftJustified); 5 (psCenterJustified); 6 (psRightJustified); or 7 (psFullyJustified). See Justification. The following values are also required: MinimumGlyphScaling and MaximumGlyphScaling.
        """
        ...

    @property
    def DesiredLetterScaling(self) -> float:
        """
        Read-write. The amount of space between letters (100 - 500; at 0, no space is added between letters). Note:Valid only when Justification = 4 (psLeftJustified); 5 (psCenterJustified); 6 (psRightJustified); or 7 (psFullyJustified). See Justification. The following values are also required: MinimumLetterScaling and MaximumLetterScaling.
        """
        ...

    @property
    def DesiredWordScaling(self) -> float:
        """
        Read-write. The amount (percentage) of space between words (0 -1000; at 100, no additional space is added between words). Note:Valid only when Justification = 4 (psLeftJustified); 5 (psCenterJustified); 6 (psRightJustified); or 7 (psFullyJustified). See Justification. The following values are also required: MinimumWordScaling and MaximumWordScaling.
        """
        ...

    @property
    def Direction(self) -> PsDirection:
        """
        Read-write. The text orientation.
        """
        ...

    @property
    def FauxBold(self) -> bool:
        """
        Read-write. Indicates whether to use faux bold. Default: false. Note:Using FauxBold.true is equivalent to selecting text and clicking the Faux Bold button in the Character palette.
        """
        ...

    @property
    def FauxItalic(self) -> bool:
        """
        Read-write. Indicates whether to use faux italic. Default: false. Note:Using FauxItalic.true is equivalent to selecting text and clicking the Faux Italic button in the Character palette.
        """
        ...

    @property
    def FirstLineIndent(self) -> float:
        """
        Read-write. The amount (unit value) to indent the first line of paragraphs (-1296 - 1296).
        """
        ...

    @property
    def Font(self) -> str:
        """
        Read-write. The text face of the character.
        """
        ...

    @property
    def HangingPunctuation(self) -> bool:
        """
        Read-write. Indicates whether to use roman Hanging Punctuation.
        """
        ...

    @property
    def Height(self) -> float:
        """
        Read-write. The height of the bounding box (unit value) for paragraph text. Note:Valid only when Kind = 2 (psParagraphText). See Kind.
        """
        ...

    @property
    def HorizontalScale(self) -> int:
        """
        Read-write. Character scaling (horizontal) in proportion to vertical scale (0 - 1000 in percent). See VerticalScale.
        """
        ...

    @property
    def HyphenateAfterFirst(self) -> int:
        """
        Read-write. The number of letters after which hyphenation in word wrap is allowed (1 - 15).
        """
        ...

    @property
    def HyphenateBeforeLast(self) -> int:
        """
        Read-write. The number of letters before which hyphenation in word wrap is allowed (1 - 15).
        """
        ...

    @property
    def HyphenateCapitalWords(self) -> bool:
        """
        Read-write. Indicates whether to allow hyphenation in word wrap of capitalized words.
        """
        ...

    @property
    def HyphenateWordsLongerThan(self) -> int:
        """
        Read-write. The minimum number of letters a word must have in order for hyphenation in word wrap to be allowed (2 - 25).
        """
        ...

    @property
    def Hyphenation(self) -> bool:
        """
        Read-write. Indicates whether to use hyphenation in word wrap.
        """
        ...

    @property
    def HyphenationZone(self) -> float:
        """
        Read-write. The distance at the end of a line that will cause a word to break in unjustified type (0 - 720 pica).
        """
        ...

    @property
    def HyphenLimit(self) -> int:
        """
        Read-write. The maximum number of consecutive lines that can end with a hyphenated word.
        """
        ...

    @property
    def Justification(self) -> PsJustification:
        """
        Read-write. The paragraph justification.
        """
        ...

    @property
    def Kind(self) -> PsTextType:
        """
        Read-write. The text-wrap type.
        """
        ...

    @property
    def Language(self) -> PsLanguage:
        """
        Read-write. The language to use.
        """
        ...

    @property
    def Leading(self) -> float:
        """
        Read-write. The leading amount (unit value).
        """
        ...

    @property
    def LeftIndent(self) -> float:
        """
        Read-write. The amount (unit value) of space to indent text from the left (-1296 - 1296).
        """
        ...

    @property
    def Ligatures(self) -> bool:
        """
        Read-write. Indicates whether to use ligatures.
        """
        ...

    @property
    def MaximumGlyphScaling(self) -> float:
        """
        Read-write. The maximum amount (percentage) to scale the horizontal size of the text letters (50 - 200; at 100, the width of characters is not scaled). Note:Valid only when Justification = 4 (psLeftJustified); 5 (psCenterJustified); 6 (psRightJustified); or 7 (psFullyJustified). See Justification. The following values are also required: MinimumGlyphScaling and DesiredGlyphScaling.
        """
        ...

    @property
    def MaximumLetterScaling(self) -> float:
        """
        Read-write. The maximum amount of space to allow between letters (100 - 500; at 0, no space is added between letters). Note:Valid only when Valid only when Justification = 4 (psLeftJustified); 5 (psCenterJustified); 6 (psRightJustified); or 7 (psFullyJustified). See Justification. The following values are also required: MaximumLetterScaling and DesiredLetterScaling.
        """
        ...

    @property
    def MaximumWordScaling(self) -> float:
        """
        Read-write. The maximum amount (percentage) of space to allow between words (0 -1000; at 100, no additional space is added between words). Note:Valid only when Justification = 4 (psLeftJustified); 5 (psCenterJustified); 6 (psRightJustified); or 7 (psFullyJustified). See Justification. The following values are also required: MaximumWordScaling and DesiredWordScaling.
        """
        ...

    @property
    def MinimumGlyphScaling(self) -> float:
        """
        Read-write. The minimum amount (percentage) to scale the horizontal size of the text letters (50 - 200; at 100, the width of characters is not scaled). Note:Valid only when Justification = 4 (psLeftJustified); 5 (psCenterJustified); 6 (psRightJustified); or 7 (psFullyJustified). See Justification. The following values are also required: MaximumGlyphScaling and DesiredGlyphScaling.
        """
        ...

    @property
    def MinimumLetterScaling(self) -> float:
        """
        Read-write. The minimum amount (percentage) of space between letters (100 - 500; at 0, no space is removed between letters). Note:Valid only when Justification = 4 (psLeftJustified); 5 (psCenterJustified); 6 (psRightJustified); or 7 (psFullyJustified). See Justification. The following values are also required: MaximumLetterScaling and DesiredLetterScaling.
        """
        ...

    @property
    def MinimumWordScaling(self) -> float:
        """
        Read-write. The minimum amount (percentage) of space between words (0 -1000; at 100, no space is removed between words). Note:Valid only when Justification = 4 (psLeftJustified); 5 (psCenterJustified); 6 (psRightJustified); or 7 (psFullyJustified). See Justification. The following values are also required: MaximumWordScaling and DesiredWordScaling.
        """
        ...

    @property
    def NoBreak(self) -> bool:
        """
        Read-write. Indicates whether to allow words to break at the end of a line. Tip:When enacted on large amounts of consecutive characters, noBreak = true can prevent word wrap and thus may prevent some text from appearing on the screen.
        """
        ...

    @property
    def OldStyle(self) -> bool:
        """
        Read-write. Indicates whether to use old style type.
        """
        ...

    @property
    def Parent(self) -> ArtLayer:
        """
        Read-write. The TextItem object's container.
        """
        ...

    @property
    def Position(self) -> List[float]:
        """
        Read-write. The position of origin for the text. The array must contain two values (unit value). Tip:Setting the Position property is basically equivalent to clicking the text tool at a point in the document to create the point of origin for text.
        """
        ...

    @property
    def RightIndent(self) -> float:
        """
        Read-write. The amount of space (unit value) to indent text from the right (-1296 - 1296).
        """
        ...

    @property
    def Size(self) -> float:
        """
        Read-write. The font size (unit value).
        """
        ...

    @property
    def SpaceAfter(self) -> float:
        """
        Read-write. The amount of space (unit value) to use after each paragraph (-1296 - 1296).
        """
        ...

    @property
    def SpaceBefore(self) -> float:
        """
        Read-write. The amount of space (unit value) to use before each paragraph (-1296 - 1296).
        """
        ...

    @property
    def StrikeThru(self) -> PsStrikeThruType:
        """
        Read-write. The text strike through option to use.
        """
        ...

    @property
    def TextComposer(self) -> PsTextComposer:
        """
        Read-write. The composition method to use to evaluate line breaks and optimize the specified hyphenation and Justification options. Note:Valid only when Kind = 2 (psParagraphText). See Kind.
        """
        ...

    @property
    def Tracking(self) -> float:
        """
        Read-write. The amount of uniform spacing between multiple characters (-1000 - 10000). Note:Tracking units are 1/1000 of an em space. The width of an em space is relative to the current type size. In a 1-point font, 1 em equals 1 point; in a 10-point font, 1 em equals 10 points. So, for example, 100 units in a 10-point font are equivalent to 1 point.
        """
        ...

    @property
    def typename(self) -> str:
        """
        Read-only. The class name of the referenced TextItem object.
        """
        ...

    @property
    def Underline(self) -> PsUnderlineType:
        """
        Read-write. The text underlining options.
        """
        ...

    @property
    def UseAutoLeading(self) -> bool:
        """
        Read-write. Indicates whether to use a font's built-in leading information.
        """
        ...

    @property
    def VerticalScale(self) -> int:
        """
        Read-write. Character scaling (vertical) in proportion to horizontal scale (0 - 1000 in percent). See HorizontalScale.
        """
        ...

    @property
    def WarpBend(self) -> float:
        """
        Read-write. The warp bend percentage (-100 - 100).
        """
        ...

    @property
    def WarpDirection(self) -> PsDirection:
        """
        Read-write. The warp direction.
        """
        ...

    @property
    def WarpHorizontalDistortion(self) -> float:
        """
        Read-write. The horizontal distortion (as percentage) of the warp (-100 - 100).
        """
        ...

    @property
    def WarpStyle(self) -> PsWarpStyle:
        """
        Read-write. The style of warp to use.
        """
        ...

    @property
    def WarpVerticalDistortion(self) -> float:
        """
        Read-write. The vertical distortion (as percentage) of the warp (-100 - 100).
        """
        ...

    @property
    def Width(self) -> float:
        """
        Read-write. The width of the bounding box (unit value) for paragraph text. Note:Valid only when Kind = 2 (psParagraphText). See Kind.
        """
        ...

    def ConvertToShape(self) -> None:
        """
        Converts the text item and its containing layer to a fill layer with the text changed to a clipping path.
        """
        ...

    def CreatePath(self) -> None:
        """
        Creates a clipping path from the outlines of the actual text items (such as letters or words).
        """
        ...

