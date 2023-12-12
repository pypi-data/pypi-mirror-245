from io import BytesIO

import jpype.imports
from typing import List

import aspose
from . import helper
from .models import *
from aspose.models import InputType


class ImageData(helper.BaseJavaClass):
    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.initParams()

    def initParams(self):
        self.source = self.getJavaClass().Source;
        self.type = self.getJavaClass().Type;
        self.width = self.getJavaClass().Width;
        self.height = self.getJavaClass().Height;
        self.filters = self.getJavaClass().Filters;
        self.image = self.getJavaClass().Image;

class OcrInput():
    __JAVA_CLASS_NAME = "com.aspose.ocr.OcrInput"

    def __init__(self, type : InputType):
        asposeClass = jpype.JClass(OcrInput.__JAVA_CLASS_NAME)
        jType = ModelsConverter.convertInputTypeToJava(type)
        self.__javaClass = asposeClass(jType)
        self.__javaClassName = ""
        self.__stream = []
        self.type = type

        if self.__javaClassName == None or self.__javaClassName == "":
            self.__javaClassName = str(self.__javaClass.getClass().getName())

    def init(self, javaClass):
        self.__javaClass = javaClass


    def add(self, fullPath : str, startPage : int = None, pagesNumber: int = None):
        if startPage == None or pagesNumber == None:
            self.__javaClass.add(fullPath)
        else:
            self.__javaClass.add(fullPath, startPage, pagesNumber)
        # if self.__type != None:
        #     self.__type =


    def addStream(self, image_data_binary, startPage: int = None, pagesNumber: int = None):
        stream = jpype.JClass('java.io.ByteArrayInputStream')
        streamJava = stream(image_data_binary)
        if startPage == None or pagesNumber == None:
            self.__javaClass.add(streamJava)
        else:
            self.__javaClass.add(streamJava, startPage, pagesNumber)

        self.__stream.append(image_data_binary)

    def clear(self):
        self.__javaClass.clear()

    def size(self):
        return self.__javaClass.size()

    def get(self, index : int) -> ImageData:
        return aspose.ocrinput.ImageData(self.__javaClass.get(index))

    def getJavaClass(self):
        return self.__javaClass






