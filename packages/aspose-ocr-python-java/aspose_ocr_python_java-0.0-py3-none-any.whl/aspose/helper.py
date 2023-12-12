import jpype

class BaseJavaClass(object):

    def __init__(self, javaClass):
        self.__javaClass = javaClass
        self.__javaClassName = ""

        if self.__javaClassName == None or self.__javaClassName == "":
            self.__javaClassName = str(self.__javaClass.getClass().getName())
    #    self.init()

    def init(self):
        raise Exception('You have to implement the method init!')


    def getJavaClass(self):
        return self.__javaClass

    def __setJavaClass(self, javaClass):
        self.__javaClass = javaClass
        if self.__javaClassName == None or self.__javaClassName == "":
            self.__javaClassName = str(self.__javaClass.getClass().getName())
        self.init()

    def __getJavaClassName(self):
        return self.__javaClassName

    def __isNull(self):
        return self.__javaClass.isNull()

    def __printJavaClassName(self):
        print("Java class name => \'" + self.__javaClassName + "\'")


class Helper:
    @staticmethod
    def converToArrayList(pythonList):
        ArrayList = jpype.JClass('java.util.ArrayList')
        javaArray = ArrayList()
        i = 0
        while (i < len(pythonList)):
            javaArray.add(pythonList[i].getJavaClass())
            i += 1

        return javaArray




class Rectangle(BaseJavaClass):
    """!
    A Rectangle specifies an area in a coordinate space that is
    enclosed by the Rectangle object's upper-left point
    in the coordinate space, its width, and its height.
    """

    def init(self):
        pass

    javaClassName = "java.awt.Rectangle"

    def __init__(self, x, y, width, height):
        """!
        Rectangle constructor.
       @param x The x-coordinate of the upper-left corner of the rectangle.
       @param y The y-coordinate of the upper-left corner of the rectangle.
       @param width The width of the rectangle.
       @param height The height of the rectangle.
        """
        javaRectangle = jpype.JClass(self.javaClassName)
        self.javaClass = javaRectangle(x, y, width, height)
        super().__init__(self.javaClass)

    @staticmethod
    def construct(arg):
        rectangle = Rectangle(0, 0, 0, 0)
        rectangle.javaClass = arg
        return rectangle

    def getX(self):
        """!
        Returns the X coordinate of the bounding Rectangle in
        double precision.
        @return the X coordinate of the bounding Rectangle.
        """
        return int(self.getJavaClass().getX())

    def getY(self):
        """!
        Returns the Y coordinate of the bounding Rectangle in
       double precision.
        @return the Y coordinate of the bounding Rectangle.
        """
        return int(self.getJavaClass().getY())

    def getLeft(self):
        """!
        Gets the x-coordinate of the left edge of self Rectangle class.
        @returns The x-coordinate of the left edge of self Rectangle class.
        """
        return self.getX()

    def getTop(self):
        """!
        Gets the y-coordinate of the top edge of self Rectangle class.
        @returns The y-coordinate of the top edge of self Rectangle class.
        """
        return self.getY()

    def getRight(self):
        """!
        Gets the x-coordinate that is the sum of X and Width property values of self Rectangle class.
        @returns The x-coordinate that is the sum of X and Width of self Rectangle.
        """
        return self.getX() + self.getWidth()

    def getBottom(self):
        """!
        Gets the y-coordinate that is the sum of the Y and Height property values of self Rectangle class.
        @returns The y-coordinate that is the sum of Y and Height of self Rectangle.
        """
        return self.getY() + self.getHeight()

    def getWidth(self):
        """!
        Returns the width of the bounding Rectangle in
        double precision.
        @return the width of the bounding Rectangle.
        """
        return int(self.getJavaClass().getWidth())

    def getHeight(self):
        """!
        Returns the height of the bounding Rectangle in
        double precision.
        @return the height of the bounding Rectangle.
        """
        return int(self.getJavaClass().getHeight())

    def toString(self):
        return str(int(self.getX())) + ',' + str(int(self.getY())) + ',' + str(int(self.getWidth())) + ',' + str(
            int(self.getHeight()))

    def equals(self, obj):
        return self.getJavaClass().equals(obj.getJavaClass())

    def intersectsWithInclusive(self, rectangle):
        """!
       Determines if self rectangle intersects with rect.
       @param rectangle
       @returns {boolean
        """
        return not ((self.getLeft() > rectangle.getRight()) | (self.getRight() < rectangle.getLeft()) |
                    (self.getTop() > rectangle.getBottom()) | (self.getBottom() < rectangle.getTop()))

    @staticmethod
    def intersect(a, b):
        """!
        Intersect Shared Method
        Produces a new Rectangle by intersecting 2 existing
        Rectangles. Returns None if there is no    intersection.
        """
        if (not a.intersectsWithInclusive(b)):
            return Rectangle(0, 0, 0, 0)

        return Rectangle.fromLTRB(max(a.getLeft(), b.getLeft()),
                                  max(a.getTop(), b.getTop()),
                                  min(a.getRight(), b.getRight()),
                                  min(a.getBottom(), b.getBottom()))

    @staticmethod
    def fromLTRB(left, top, right, bottom):
        """!
        FromLTRB Shared Method
        Produces a Rectangle class from left, top, right,
        and bottom coordinates.
        """
        return Rectangle(left, top, right - left, bottom - top)

    def isEmpty(self):
        return (self.getWidth() <= 0) | (self.getHeight() <= 0)



class OcrException(Exception):
    """!
    Represents the exception for creating barcode image.
    """

    @staticmethod
    def MAX_LINES():
        return 4

    def __init__(self, exc):
        """!
        Initializes a new instance of the  BarCodeException class with specified error message.
        """
        self.message = None
        super().__init__(self, exc)
        if (isinstance(exc, str)):
            self.setMessage(str(exc))
            return

        exc_message = 'Exception occured in file:line\n'

        self.setMessage(exc_message)

    def setMessage(self, message):
        """!
        Sets message
        """
        self.message = message

    def getMessage(self):
        """!
        Gets message
        """
        return self.message