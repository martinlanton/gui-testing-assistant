# TODO : there's a good indication of how that can be done in here :
#  https://stackoverflow.com/questions/24144482/how-to-test-drag-and-drop-behavior-in-pyqt?rq=3
import sys
import time
from PySide6 import QtWidgets, QtCore

from gui_testing_assistant import mouse_drag
from two.module_two import my_second_var as v_2

from tests.fixtures import list_view


class TestMouseMove:
    @classmethod
    def setup_class(cls):
        cls.app = QtWidgets.QApplication(sys.argv)
        cls.view = list_view.DraggableListView()
        model = list_view.DraggableListModel()
        model.setStringList(["apple", "orange"])
        cls.view.setModel(model)
        cls.view.show()

    def test_module_one(self):
        assert mouse_drag.my_first_var

    def test_module_two(self):
        assert v_2 == 2

    def test_drag_and_drop(self):
        # TODO : potential other solution : trigger custom event :
        #  issue : https://github.com/pytest-dev/pytest-qt/issues/428
        #  PR : https://github.com/pytest-dev/pytest-qt/pull/429/files
        source_index = self.view.model().index(0, 0, QtCore.QModelIndex())
        source_item_rect = self.view.visualRect(source_index)
        self.source_position = self.view.mapToGlobal(source_item_rect.center())

        destination_index = self.view.model().index(1, 0, QtCore.QModelIndex())
        destination_item_rect = self.view.visualRect(destination_index)
        center = self.view.mapToGlobal(destination_item_rect.center())
        self.destination_position = QtCore.QPoint(center.x(), center.y()+20)

        # TODO : make it work
        #  This appears to correctly open the GUI and correctly move the mouse
        #  (with the correct coordinates), however it looks like the GUI is not
        #  properly populated when the thread is created and starts moving the
        #  mouse. As a result, the items aren't moved and the assertions fail,
        #  since the QModelIndex aren't reordered in the model.
        time.sleep(1)

        # TODO : turn this into a context manager
        thread = Thread(self.source_position, self.destination_position)
        thread.finished.connect(thread.deleteLater)
        thread.start()

        thread.wait()  # wait for thread to finish before asserting

        # check that the drop had the desired effect
        assert self.view.model().rowCount() == 2
        assert self.view.model().index(0, 0, QtCore.QModelIndex()).data() == "orange"
        assert self.view.model().index(1, 0, QtCore.QModelIndex()).data() == "apple"


class Thread(QtCore.QThread):
    def __init__(self, source, destination, parent=None):
        super(Thread, self).__init__(parent)
        self.source = source
        self.destination = destination

    def run(self):
        mouse_drag.mouseDrag(self.source, self.destination)
        print("FINISHED")
