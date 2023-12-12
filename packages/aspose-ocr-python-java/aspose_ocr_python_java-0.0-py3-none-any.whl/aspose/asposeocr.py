# Aspose.OCR for Python via Java
# Main functionality of the interface
#
# Author:   aspose
# Created:  Nov 2023
#
# Copyright (C) 2013 Aspose
# For license information, see LICENSE.txt

"""
Python interface to the Aspose OCR

**Aspose.OCR for Python via .Java** is a powerful,
while easy-to-use optical character recognition (OCR)
 engine for your Python applications and notebooks.
In less than **10** lines of code, you can recognize
text in **28** languages based on Latin, Cyrillic,
and Asian scripts, returning results in the most popular
document and data interchange formats.
There is no need to learn complex mathematical models,
build machine learning algorithms and train neural
networks — our simple and robust API will do everything for you.
"""

##########################################################################
## Imports
##########################################################################

import jpype.imports
from typing import List

import aspose.recognitionsettings
from .helper import *
from .ocrinput import OcrInput
from .recognitionresult import *
from .recognitionsettings import *
from .models import *

from com.aspose.ocr import *

##########################################################################
## Main Functionality
##########################################################################



class AsposeOcr():
    __JAVA_CLASS_NAME = "com.aspose.ocr.AsposeOCR"

    def __init__(self):
        asposeClass = jpype.JClass(AsposeOcr.__JAVA_CLASS_NAME)
        self.__initJavaClass(asposeClass())

    def __initJavaClass(self, javaClass):
        self.__javaClass = javaClass
        self.__javaClassName = ""

        if self.__javaClassName == None or self.__javaClassName == "":
            self.__javaClassName = str(self.__javaClass.getClass().getName())

    def imageHasText(self, fullPath : str, text : str, settings : RecognitionSettings = None, ignoreCase : bool = True) -> bool:
        if (settings == None):
            settings = aspose.recognitionsettings.RecognitionSettings()
        settings = settings.getJavaClass()
        return self.__getJavaClass().ImageHasText(fullPath, text, settings, ignoreCase)

    def compareImageTexts(self, fullPath1 : str, fullPath2 : str, settings : RecognitionSettings = None, ignoreCase : bool = True) -> bool:
        if (settings == None):
            settings = aspose.recognitionsettings.RecognitionSettings()
        settings = settings.getJavaClass()
        return self.__getJavaClass().CompareImageTexts(fullPath1, fullPath2, settings, ignoreCase)

    def imageTextDiff(self, fullPath1 : str, fullPath2 : str, settings : RecognitionSettings, ignoreCase : bool = True) -> float:
        if (settings == None):
            settings = aspose.recognitionsettings.RecognitionSettings()
        settings = settings.getJavaClass()
        return self.__getJavaClass().ImageTextDiff(fullPath1, fullPath2, settings, ignoreCase)

    def recognize(self, input: OcrInput, settings : RecognitionSettings = None):
        if (settings == None):
            settings = aspose.recognitionsettings.RecognitionSettings()
        settings = settings.getJavaClass()

        inputJava = input.getJavaClass()
        results = self.__getJavaClass().Recognize(inputJava, settings)

        pythonResult = []
        for result in results:
            r = aspose.recognitionresult.RecognitionResult(result)
            pythonResult.append(r)

        return pythonResult

    def recognize_receipt(self, input: aspose.ocrinput.OcrInput, settings: aspose.recognitionsettings.ReceiptRecognitionSettings = None):
        if (settings == None):
            settings = aspose.recognitionsettings.ReceiptRecognitionSettings()
        settings = settings.getJavaClass()

        inputJava = input.getJavaClass()
        results = self.__getJavaClass().RecognizeReceipt(inputJava, settings)

        pythonResult = []
        for result in results:
            r = aspose.recognitionresult.RecognitionResult(result)
            pythonResult.append(r)

        return pythonResult

    def recognize_car_plate(self, input: aspose.ocrinput.OcrInput, settings: aspose.recognitionsettings.CarPlateRecognitionSettings = None):
        if (settings == None):
            settings = aspose.recognitionsettings.CarPlateRecognitionSettings()
        settings = settings.getJavaClass()

        inputJava = input.getJavaClass()
        results = self.__getJavaClass().RecognizeCarPlate(inputJava, settings)

        pythonResult = []
        for result in results:
            r = aspose.recognitionresult.RecognitionResult(result)
            pythonResult.append(r)

        return pythonResult

    def recognize_fast(self, input : OcrInput):
        inputJava = input.getJavaClass()
        results = self.__javaClass.RecognizeFast(inputJava)
        pythonResult = []
        for result in results:
            r = str(result)
            pythonResult.append(r)

        return pythonResult

    def recognize_lines(self, input: OcrInput, settings: RecognitionSettings = None):
        if (settings == None):
            settings = aspose.recognitionsettings.RecognitionSettings()
        settings.set_recognize_single_line(True)
        settings = settings.getJavaClass()

        inputJava = input.getJavaClass()
        results = self.__getJavaClass().Recognize(inputJava, settings)

        pythonResult = []
        for result in results:
            r = aspose.recognitionresult.RecognitionResult(result)
            pythonResult.append(r)

        return pythonResult

    def calculate_skew(self, input: OcrInput):
        inputJava = input.getJavaClass()
        results = self.__getJavaClass().CalculateSkew(inputJava)

        pythonResult = []
        for result in results:
            r = aspose.recognitionresult.SkewOutput(result)
            pythonResult.append(r)
        return pythonResult

    def correct_spelling(self, text : str, language : SpellCheckLanguage):
        jType = ModelsConverter.convertToJavaSpellCheckLanguage(language)
        return self.__javaClass.CorrectSpelling(text, jType)



    @staticmethod
    def save_multipage_document(fullFileName: str, saveFormat: Format, results: List):
        javaList = Helper.converToArrayList(results)
        javaStrClass = jpype.JClass('java.lang.String')
        javaStr = javaStrClass(fullFileName)
        asposeClass = jpype.JClass(AsposeOcr.__JAVA_CLASS_NAME)

        format = ModelsConverter.convertToJavaFormat(saveFormat)
        asposeClass.SaveMultipageDocument(javaStr, format, javaList)


    def shutdown(self):
        jpype.shutdownJVM()

    def __del__(self):
        """
        Destructor.

        """

      #  self.shutdown()


    def __getJavaClass(self):
        return self.__javaClass


class ImageProcessing():
    __JAVA_CLASS_NAME = "com.aspose.ocr.ImageProcessing"

    @staticmethod
    def save(images, folderPath):
        asposeClass = jpype.JClass(ImageProcessing.__JAVA_CLASS_NAME)
        inputJava = images.getJavaClass()
        output = asposeClass.Save(inputJava, folderPath)
        outputJava = aspose.ocrinput.OcrInput(aspose.ocrinput.InputType.SINGLE_IMAGE)
        outputJava.init(output)
        return outputJava

    @staticmethod
    def render(images):
        asposeClass = jpype.JClass(ImageProcessing.__JAVA_CLASS_NAME)
        inputJava = images.getJavaClass()
        output = asposeClass.Render(inputJava)
        outputJava = aspose.ocrinput.OcrInput(aspose.ocrinput.InputType.SINGLE_IMAGE)
        outputJava.init(output)
        return outputJava
