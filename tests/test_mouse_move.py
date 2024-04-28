# TODO : there's a good indication of how that can be done in here :
#  https://stackoverflow.com/questions/24144482/how-to-test-drag-and-drop-behavior-in-pyqt?rq=3
import threading
import time
import math
import unittest

from PySide6 import QtCore, QtTest
from fixtures import list_view
import mouse


def mouseDrag(source_widget, dest_widget, source_view=None, destination_view=None, rate=1000):
    """Simulate a mouse visible mouse drag from source to dest, rate is pixels/second.

    :param source_widget: widget or model index to get the position from. When providing a model index, a view must be provided as well.
    :type source_widget: QtWidgets.QWidget or QtCore.QModelIndex

    :param dest_widget: widget or model index to get the position from. When providing a model index, a view must be provided as well.
    :type dest_widget: QtWidgets.QWidget or QtCore.QModelIndex

    :param source_view: view to get the item position from based on the QModelIndex.
    :type source_view: QAbstractItemView

    :param destination_view: view to get the item position from based on the QModelIndex.
    :type destination_view: QAbstractItemView

    :param rate: number of pixel per second
    :type rate: int
    """
    # TODO : check the type of each of the source/destination arguments
    # TODO :
    #  if it's a widget, get its position as we already do
    #  if it's a QModelIndex, check that a view was passed in the view argument, otherwise raise an
    #  error
    #  then get the position from the view and model index as follows :
    #          destination_item_rect = cls.view.visualRect(destination_index)
    #          destination_position = destination_item_rect.center()
    source = center(source_widget)
    dest = center(dest_widget)

    mouse.press(source.x(), source.y())

    # smooth move from source to dest by moving pixel by pixel based on the specified speed
    millisecond_per_second = 1000
    npoints = int(math.sqrt((dest.x()-source.x())**2 + (dest.y()-source.y())**2 ) / (rate/millisecond_per_second))
    for i in range(npoints):
        x = int(source.x() + ((dest.x()-source.x())/npoints)*i)
        y = int(source.y() + ((dest.y()-source.y())/npoints)*i)
        mouse.move(x, y)
        time.sleep(0.001)

    mouse.release(*dest)


def center(widget):
    midpoint = QtCore.QPoint(widget.width()/2, widget.height()/2)
    return widget.mapToGlobal(midpoint)


class TestMouseMove(unittest.TestCase):
    def setUpClass(cls):
        cls.view = list_view.DraggableListView()
        model = list_view.DraggableListModel()
        model.setStringList(["apple", "orange"])
        cls.view.setModel(model)
        cls.view.show()
        source_index = model.index(row=0, column=0)
        source_item_rect = cls.view.visualRect(source_index)
        source_position = source_item_rect.center()
        destination_index = model.index(row=0, column=0)
        destination_item_rect = cls.view.visualRect(destination_index)
        destination_position = destination_item_rect.center()
        cls.source_widget = cls.view.child1
        cls.dest_widget = cls.view.child2

    def testDragAndDrop(self):
        # TODO : turn this into a context manager
        dragThread = threading.Thread(target=mouseDrag, args=((self.source_widget),
                                                              (self.dest_widget)))
        dragThread.start()
        # cannot join, use non-blocking wait
        while dragThread.is_alive():
            QtTest.QTest.qWait(1000)

        # check that the drop had the desired effect
        assert self.dest_widget.hasItemCount() > 0
