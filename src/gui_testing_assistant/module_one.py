import math
import time

import mouse
from PySide6 import QtCore

my_first_var = True


def mouseDrag(source, destination, rate=1000):
    """Simulate a mouse visible mouse drag from source to dest, rate is pixels/second.

    :param source: widget or model index to get the position from. When providing a model index, a view must be provided as well.
    :type source: QtWidgets.QWidget or QtCore.QPoint

    :param destination: widget or model index to get the position from. When providing a model index, a view must be provided as well.
    :type destination: QtWidgets.QWidget or QtCore.QPoint

    :param rate: number of pixel per second
    :type rate: int
    """
    # TODO : check the type of each of the source/destination arguments
    # TODO :
    #  if it's a widget: get its position as we already do
    #  if it's a QPoint:  pass that directly
    # source = center(source)
    # dest = center(destination)

    mouse.press(source)

    # smooth move from source to dest by moving pixel by pixel based on the specified speed
    millisecond_per_second = 1000
    npoints = int(math.sqrt((destination.x()-source.x())**2 + (destination.y()-source.y())**2 ) / (rate/millisecond_per_second))
    for i in range(npoints):
        x = int(source.x() + ((destination.x()-source.x())/npoints)*i)
        y = int(source.y() + ((destination.y()-source.y())/npoints)*i)
        mouse.move(x, y)
        time.sleep(0.001)

    mouse.release(*destination)


def center(widget):
    midpoint = QtCore.QPoint(widget.width()/2, widget.height()/2)
    return widget.mapToGlobal(midpoint)
