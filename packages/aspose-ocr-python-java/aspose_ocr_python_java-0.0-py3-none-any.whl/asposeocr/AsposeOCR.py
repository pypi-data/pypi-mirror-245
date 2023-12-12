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

jpype.startJVM(
    classpath=['C:\\Users\\Admin\\.m2\\repository\\com\\aspose\\aspose-ocr\\23.10.0\\aspose-ocr-23.10.0.jar',
               'C:\\Users\\Admin\\.m2\\repository\\com\\microsoft\\onnxruntime\\onnxruntime\\1.16.0\\onnxruntime-1.16.0.jar'])

from com.aspose.ocr import *
#from com.aspose.ocr.RecognitionResult import *

##########################################################################
## Main Functionality
##########################################################################

class AsposeOCR:


   # def ImageHasText(self, fullPath : str, text : str, settings : RecognitionSettings, ignoreCase : bool) -> bool:
   #     return self.api.ImageHasText(fullPath, text, settings, ignoreCase)


    def recognize(self, input: OcrInput): #-> RecognitionResult:
        api = jpype.JClass("com.aspose.ocr.AsposeOCR")
        Language=jpype.JClass("com.aspose.ocr.Language")
        RecognitionSettings = jpype.JClass("com.aspose.ocr.RecognitionSettings")
        settings = RecognitionSettings(detectAreas=True, autoSkew=True)
        settings.setLanguage(Language.Eng)
        data = api.Recognize(input, settings)
        return data


    def recognize2(filePath: str) -> List[str]:
        """

        :param filePath:
        """

      #  api = AsposeOCR()

      #  input = OcrInput(InputType.SingleImage)
      #  input.add("D:\\imgs\\10.png")
      #  results = api.RecognizeStreetPhoto(input)
      #  for res in results:
      #      print(res.recognitionText)

    def recognize3(self, filePath: str) -> List[str]:
        """

        :param filePath:
        """

        api = AsposeOCR()

        input = OcrInput(InputType.SingleImage)
        input.add("D:\\imgs\\10.png")
        results = api.RecognizeStreetPhoto(input)
        for res in results:
            print(res.recognitionText)



    def shutdown(self):
        jpype.shutdownJVM()

    def __del__(self):
        """
        Destructor.

        """

      #  self.shutdown()

#api = AsposeOCR()
#input = OcrInput(InputType.SingleImage)
#input.add('D://imgs/10.png')
#api.recognize(input)