import jpype.imports
from typing import List
from aspose import *

ocrInput = jpype.JClass("com.aspose.ocr.OcrInput")
class OcrInput:

    def __new__( inputtype: InputType):
        return ocrInput(inputType)

    def __new__(inputtype: InputType, filters: PreprocessingFilter):
        return ocrInput(inputType, filters)

    def add(self, fullPath: str):
        ocrInput.add(fullPath)

    def replaceFilters(filters: PreprocessingFilter):
        ocrInput.replaceFilters(filters)