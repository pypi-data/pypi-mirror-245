import jpype
import os
#from aspose import AsposeOCR, OcrInput, InputType

__asposeocr_dir__ = os.path.dirname(__file__)
__ocr_jar_path__ = __asposeocr_dir__ + "/jlib/aspose-ocr-23.11.0.jar"
__onnx_jar_path__ = __asposeocr_dir__ + "/jlib/onnxruntime-1.16.0.jar"

jpype.startJVM('-ea', classpath=[__ocr_jar_path__, __onnx_jar_path__])
#print(jpype.java.lang.System.getProperty('java.class.path'))
__all__ = ['asposeocr', 'ocrinput', 'models', 'recognitionsettings', 'recognitionresult', 'license', 'helper']

from .models import *
from .recognitionsettings import *
from .recognitionresult import *
from .asposeocr import AsposeOcr
from .ocrinput import *
from .license import *