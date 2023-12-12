from . import helper
import jpype.imports
from aspose.models import *



class LinesResult(helper.BaseJavaClass):
    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.text_in_line = None
        self.line = None
        self.initParams()

    def initParams(self):
        self.text_in_line = self.getJavaClass().textInLine
        self.line = self.getJavaClass().line

class RecognitionResult():
    __JAVA_CLASS_NAME = "com.aspose.ocr.RecognitionResult"

    def __init__(self, javaClass):
        self.__javaClass = javaClass
        self.__javaClassName = ""

        if self.__javaClassName == None or self.__javaClassName == "":
            self.__javaClassName = str(self.__javaClass.getClass().getName())

        self.recognition_areas_text = []
        self.recognition_lines_result = []
        self.init()


    def init(self):
        for t in self.getJavaClass().recognitionAreasText:
            self.recognition_areas_text.append(t)

        for t in self.getJavaClass().recognitionLinesResult:
            lines = LinesResult(t)
            self.recognition_lines_result.append(lines)
        self.recognition_text = self.getJavaClass().recognitionText
        self.recognition_areas_rectangles = self.getJavaClass().recognitionAreasRectangles
        self.skew = self.getJavaClass().skew
        self.warnings = self.getJavaClass().warnings
        self.recognition_characters_list = self.getJavaClass().recognitionCharactersList


    def getJavaClass(self):
        return self.__javaClass

    def get_json(self):
        return self.getJavaClass().GetJson()

    def get_xml(self):
        return self.getJavaClass().GetXml()

    def save(self, fullFileName : str, format : Format):
        jTypeFormat = ModelsConverter.convertToJavaFormat(format)
        self.getJavaClass().save(fullFileName, jTypeFormat)

    def save_spell_check_corrected_text(self, fullFileName : str, format : Format, language : SpellCheckLanguage = SpellCheckLanguage.ENG):
        jTypeLang = ModelsConverter.convertToJavaSpellCheckLanguage(language)
        jTypeFormat = ModelsConverter.convertToJavaFormat(format)
        self.getJavaClass().saveSpellCheckCorrectedText(fullFileName, jTypeFormat, jTypeLang)

    def get_spell_check_corrected_text(self, language : SpellCheckLanguage):
        jType = ModelsConverter.convertToJavaSpellCheckLanguage(language)
        return self.getJavaClass().getSpellCheckCorrectedText(jType)

    def get_spell_check_error_list(self, language : SpellCheckLanguage = SpellCheckLanguage.ENG):
        jType = ModelsConverter.convertToJavaSpellCheckLanguage(language)
        list = self.getJavaClass().getSpellCheckErrorList(jType)
        pythonList = []
        for elem in list:
            pythonList.append(SpellCheckError(elem))
        return pythonList

    def use_user_dictionary(self, dictionaryPath : str):
        self.getJavaClass().useUserDictionary(dictionaryPath)

    @staticmethod
    def save_multipage_document(self, fullPath : str):
        self.getJavaClass().add(fullPath)


class SkewOutput(helper.BaseJavaClass):
    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.initParams()

    def initParams(self):
        self.source = self.getJavaClass().Source;
        self.angle = self.getJavaClass().Angle;
        self.page = self.getJavaClass().Page;
        self.image_index = self.getJavaClass().ImageIndex;


