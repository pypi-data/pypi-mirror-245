import jpype.imports
from typing import List

import aspose.models
from aspose.models import *




class RecognitionSettings():
    JAVA_CLASS_NAME = "com.aspose.ocr.RecognitionSettings"

    def __init__(self):
        asposeClass = jpype.JClass(RecognitionSettings.JAVA_CLASS_NAME)
        self.__javaClass = asposeClass()
        self.__javaClassName = ""

        if self.__javaClassName == None or self.__javaClassName == "":
            self.__javaClassName = str(self.__javaClass.getClass().getName())

    def getJavaClass(self):
        return self.__javaClass

    def set_recognize_single_line(self, recognizeSingleLine : bool):
        self.getJavaClass().setRecognizeSingleLine(recognizeSingleLine)

    def set_detect_areas_mode(self, detectAreasMode : DetectAreasMode):
        jType = aspose.models.ModelsConverter.convertToJavaAreasMode(detectAreasMode)
        self.getJavaClass().setDetectAreasMode(jType)

    def set_language(self, language : Language):
        jType = aspose.models.ModelsConverter.convertToJavaLanguage(language)
        self.getJavaClass().setLanguage(jType)

    def set_ignored_characters(self, ignoredCharacters : str):
        self.getJavaClass().setIgnoredCharacters(ignoredCharacters)

    def set_allowed_characters(self, allowedCharacters: str):
        self.getJavaClass().setAllowedCharacters(allowedCharacters)

    def set_threads_count(self, threadsCount : int):
        self.getJavaClass().setThreadsCount(threadsCount)


class ReceiptRecognitionSettings():
    JAVA_CLASS_NAME = "com.aspose.ocr.ReceiptRecognitionSettings"

    def __init__(self):
        asposeClass = jpype.JClass(ReceiptRecognitionSettings.JAVA_CLASS_NAME)
        self.__javaClass = asposeClass()
        self.__javaClassName = ""

        if self.__javaClassName == None or self.__javaClassName == "":
            self.__javaClassName = str(self.__javaClass.getClass().getName())

    def getJavaClass(self):
        return self.__javaClass

    def set_language(self, language: Language):
        jType = aspose.models.ModelsConverter.convertToJavaLanguage(language)
        self.getJavaClass().setLanguage(jType)

    def set_ignored_characters(self, ignoredCharacters: str):
        self.getJavaClass().setIgnoredCharacters(ignoredCharacters)

    def set_allowed_characters(self, allowedCharacters: str):
        self.getJavaClass().setAllowedCharacters(allowedCharacters)

    def set_threads_count(self, threadsCount: int):
        self.getJavaClass().setThreadsCount(threadsCount)

class CarPlateRecognitionSettings():
    JAVA_CLASS_NAME = "com.aspose.ocr.CarPlateRecognitionSettings"

    def __init__(self):
        asposeClass = jpype.JClass(CarPlateRecognitionSettings.JAVA_CLASS_NAME)
        self.__javaClass = asposeClass()
        self.__javaClassName = ""

        if self.__javaClassName == None or self.__javaClassName == "":
            self.__javaClassName = str(self.__javaClass.getClass().getName())

    def getJavaClass(self):
        return self.__javaClass

    def set_language(self, language: Language):
        jType = aspose.models.ModelsConverter.convertToJavaLanguage(language)
        self.getJavaClass().setLanguage(jType)

    def set_ignored_characters(self, ignoredCharacters: str):
        self.getJavaClass().setIgnoredCharacters(ignoredCharacters)

    def set_allowed_characters(self, allowedCharacters: str):
        self.getJavaClass().setAllowedCharacters(allowedCharacters)

    def set_threads_count(self, threadsCount: int):
        self.getJavaClass().setThreadsCount(threadsCount)