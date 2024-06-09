import mouse
from PySide6 import QtCore, QtWidgets

my_first_var = True


def mouseDrag(source, destination):
    """Simulate a mouse visible mouse drag from source to dest, rate is pixels/second.

    :param source: widget or model index to get the position from. When providing a model index, a view must be provided as well.
    :type source: QtWidgets.QWidget or QtCore.QPoint

    :param destination: widget or model index to get the position from. When providing a model index, a view must be provided as well.
    :type destination: QtWidgets.QWidget or QtCore.QPoint
    """
    # TODO : check the type of each of the source/destination arguments
    # TODO :
    #  if it's a widget: get its position as we already do
    #  if it's a position : pass that directly

    mouse.drag(source.x(), source.y(), destination.x(), destination.y(), duration=3)


def center(widget):
    midpoint = QtCore.QPoint(widget.width()/2, widget.height()/2)
    return widget.mapToGlobal(midpoint)
