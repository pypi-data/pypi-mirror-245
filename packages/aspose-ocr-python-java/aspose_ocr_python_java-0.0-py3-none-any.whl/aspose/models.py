from enum import Enum
import jpype

import aspose.models
from aspose import helper


class InputType(Enum):
    SINGLE_IMAGE = 0
    PDF = 1
    TIFF = 2
    URL = 3
    DIRECTORY = 4
    ZIP = 5
    BASE64 = 6


class Format(Enum):
    TEXT = 0
    DOCX = 1
    PDF = 2
    XLSX = 3
    XML = 4
    JSON = 5
    HTML = 6
    EPUB = 7
    RTF = 8
    PDF_NO_IMG = 9


class SpellCheckLanguage(Enum):
    ENG = 0
    DEU = 1
    SPA = 2
    FRA = 3
    ITA = 4
    POR = 5
    CZE = 6
    DAN = 7
    DUM = 8
    EST = 9
    FIN = 10
    LAV = 11
    LIT = 12
    POL = 13
    RUM = 14
    SLK = 15
    SLV = 16
    SWE = 17

class Language(Enum):
    NONE = 0
    LATIN = 1
    CYRILLIC = 2
    ENG = 3
    DEU = 4
    POR = 5
    SPA = 6
    FRA = 7
    ITA = 8
    CZE = 9
    DAN = 10
    DUM = 11
    EST = 12
    FIN = 13
    LAV = 14
    LIT = 15
    NOR = 16
    POL = 17
    RUM = 18
    SRP_HRV = 19
    SLK = 20
    SLV = 21
    SWE = 22
    CHI = 23
    BEL = 24
    BUL = 25
    KAZ = 26
    RUS = 27
    SRP = 28
    UKR = 29
    HIN = 30


class DetectAreasMode(Enum):
    NONE = 0
    DOCUMENT = 1
    PHOTO = 2
    COMBINE = 3
    TABLE = 4
    CURVED_TEXT = 5
    TEXT_IN_WILD = 6



class SpellCheckError(helper.BaseJavaClass):

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.suggested_words = []
        self.initParams()

    def initParams(self):
        self.word = self.getJavaClass().word
        self.start_position = self.getJavaClass().startPosition
        self.length = self.getJavaClass().length
        suggestion = self.getJavaClass().suggestedWords
        for item in suggestion:
            self.suggested_words.append(SuggestedWord(item))


class SuggestedWord(helper.BaseJavaClass):

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.initParams()

    def initParams(self):
        self.word = self.getJavaClass().word
        self.distance = self.getJavaClass().distance



class PreprocessingFilter(helper.BaseJavaClass):
    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.initParams()

#    def add(self, filter : aspose.models.PreprocessingFilter.PreprocessingFilter):
#        self.getJavaClass().add(filter)



class ModelsConverter:

    def convertToJavaSpellCheckLanguage(jType):
        return ModelsConverter.__switchSpellCheckLanguage(jType)

    def __switchSpellCheckLanguage(type):
        javaType = "com.aspose.ocr.SpellCheck.SpellCheckLanguage"
        language = jpype.JClass(javaType)
        if type.name == "ENG":
            return language.Eng
        elif type.name == "DEU":
            return language.Deu
        if type.name =="SPA":
            return language.Spa
        if type.name =="FRA":
            return language.Fra
        if type.name =="ITA":
            return language.Ita
        if type.name =="POR":
            return language.Por
        if type.name =="CZE":
            return language.Cze
        if type.name =="DAN":
            return language.Dan
        if type.name =="DUM":
            return language.Dum
        if type.name =="EST":
            return language.Est
        if type.name =="FIN":
            return language.Fin
        if type.name =="LAV":
            return language.Lav
        if type.name =="LIT":
            return language.Lit
        if type.name =="POL":
            return language.Pol
        if type.name =="RUM":
            return language.Rum
        if type.name =="SLK":
            return language.Slk
        if type.name =="SLV":
            return language.Slv
        if type.name =="SWE":
            return language.Swe

    def convertToJavaFormat(jType):
        return ModelsConverter.__switchFormat(jType)

    def __switchFormat(type):
        javaType = "com.aspose.ocr.Format"
        format = jpype.JClass(javaType)
        if type.name == "TEXT":
            return format.Text
        elif type.name == "DOCX":
            return format.Docx
        if type.name == "PDF":
                return format.Pdf
        if type.name == "XLSX":
                return format.Xlsx
        if type.name == "XML":
                return format.Xml
        if type.name == "JSON":
                return format.Json
        if type.name == "HTML":
                return format.Html
        if type.name == "EPUB":
                return format.Epub
        if type.name == "RTF":
                return format.Rtf
        if type.name == "PDF_NO_IMG":
                return format.PdfNoImg


    def convertInputTypeToJava(jType):
        return ModelsConverter.__switchInputType(jType)

    def __switchInputType(type):
        javaType = "com.aspose.ocr.InputType"
        inputType = jpype.JClass(javaType)
        if type.name == "SINGLE_IMAGE":
            return inputType.SingleImage
        elif type.name == "PDF":
            return inputType.PDF
        elif type.name == "TIFF":
            return inputType.TIFF
        elif type.name == "URL":
            return inputType.URL
        elif type.name == "DIRECTORY":
            return inputType.Directory
        elif type.name == "ZIP":
            return inputType.Zip
        elif type.name == "BASE64":
            return inputType.Base64

    def convertToJavaAreasMode(jType):
        return ModelsConverter.__switchAreasMode(jType)

    def __switchAreasMode(type):
        javaType = "com.aspose.ocr.DetectAreasMode"
        detectAreasMode = jpype.JClass(javaType)
        if type.name == "NONE":
            return detectAreasMode.NONE
        elif type.name == "DOCUMENT":
            return detectAreasMode.DOCUMENT
        elif type.name == "PHOTO":
            return detectAreasMode.PHOTO
        elif type.name == "COMBINE":
            return detectAreasMode.COMBINE
        elif type.name == "TABLE":
            return detectAreasMode.TABLE
        elif type.name == "CURVED_TEXT":
            return detectAreasMode.CURVED_TEXT
        elif type.name == "TEXT_IN_WILD":
            return detectAreasMode.TEXT_IN_WILD

    def convertToJavaLanguage(jType):
        return ModelsConverter.__switchLanguage(jType)

    def __switchLanguage(type):
        javaType = "com.aspose.ocr.Language"
        language = jpype.JClass(javaType)
        if type.name == "NONE":
            return language.Latin
        if type.name == "LATIN":
            return language.Latin
        if type.name == "CYRILLIC":
            return language.Cyrillic
        if type.name == "ENG":
            return language.Eng
        if type.name == "DEU":
            return language.Deu
        if type.name == "POR":
            return language.Por
        if type.name == "SPA":
            return language.Spa
        if type.name == "FRA":
            return language.Fra
        if type.name == "ITA":
            return language.Ita
        if type.name == "CZE":
            return language.Cze
        if type.name == "DAN":
            return language.Dan
        if type.name == "DUM":
            return language.Dum
        if type.name == "EST":
            return language.Est
        if type.name == "FIN":
            return language.Fin
        if type.name == "LAV":
            return language.Lav
        if type.name == "LIT":
            return language.Lit
        if type.name == "NOR":
            return language.Nor
        if type.name == "POL":
            return language.Pol
        if type.name == "RUM":
            return language.Rum
        if type.name == "SRP_HRV":
            return language.Srp_hrv
        if type.name == "SLK":
            return language.Slk
        if type.name == "SLV":
            return language.Slv
        if type.name == "SWE":
            return language.Swe
        if type.name == "CHI":
            return language.Chi
        if type.name == "BEL":
            return language.Bel
        if type.name == "BUL":
            return language.Bul
        if type.name == "KAZ":
            return language.Kaz
        if type.name == "RUS":
            return language.Rus
        if type.name == "SRP":
            return language.Srp
        if type.name == "UKR":
            return language.Ukr
        if type.name == "HIN":
            return language.Hin