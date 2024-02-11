# TODO : there's a good indication of how that can be done in here :
#  https://stackoverflow.com/questions/24144482/how-to-test-drag-and-drop-behavior-in-pyqt?rq=3
import unittest
import time, threading
import math

from PySide6 import QtCore, QtTest
import mouse

def mouseDrag(source_widget, dest_widget, rate=1000):
    """Simulate a mouse visible mouse drag from source to dest, rate is pixels/second"""
    source = center(source_widget)
    dest = center(dest_widget)

    mouse.press(source.x(), source.y())

    # smooth move from source to dest
    npoints = int(math.sqrt((dest.x()-source.x())**2 + (dest.y()-source.y())**2 ) / (rate/1000))
    for i in range(npoints):
        x = int(source.x() + ((dest.x()-source.x())/npoints)*i)
        y = int(source.y() + ((dest.y()-source.y())/npoints)*i)
        mouse.move(x,y)
        time.sleep(0.001)

    mouse.release(*dest)

def center(widget):
    midpoint = QtCore.QPoint(widget.width()/2, widget.height()/2)
    return widget.mapToGlobal(midpoint)

class TestMouseMove(unittest.TestCase):
    def setUpClass(cls):
        cls.widget = MyWidget()
        cls.source_widget = cls.widget.child1
        cls.dest_widget = cls.widget.child2

    def testDragAndDrop(self):
        source_widget = self.source_widget
        dest_widget = self.dest_widget
        # grab the center of the widgets
        dragThread = threading.Thread(target=mouseDrag, args=(source_widget, dest_widget))
        dragThread.start()
        # cannot join, use non-blocking wait
        while dragThread.is_alive():
            QtTest.QTest.qWait(1000)

        # check that the drop had the desired effect
        assert dest_widget.hasItemCount() > 0