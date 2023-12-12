import jpype
import os
#from aspose import AsposeOCR#, OcrInput, InputType

__asposeocr_dir__ = os.path.dirname(__file__)
__ocr_jar_path__ = __asposeocr_dir__ + "/jlib/aspose-ocr-23.10.0.jar"
#jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=%s" % __ocr_jar_path__)
__all__ = ['AsposeOCR','OcrInput','InputType']

from .AsposeOCR import *
#from .OcrInput import *
#from .InputType import *