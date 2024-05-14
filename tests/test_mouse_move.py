# TODO : there's a good indication of how that can be done in here :
#  https://stackoverflow.com/questions/24144482/how-to-test-drag-and-drop-behavior-in-pyqt?rq=3
import sys
import threading
from PySide6 import QtTest, QtWidgets, QtCore

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
        source_index = self.view.model().index(0, 0, QtCore.QModelIndex())
        source_item_rect = self.view.visualRect(source_index)
        self.source_position = self.view.mapToGlobal(source_item_rect.center())

        destination_index = self.view.model().index(1, 0, QtCore.QModelIndex())
        destination_item_rect = self.view.visualRect(destination_index)
        center = self.view.mapToGlobal(destination_item_rect.center())
        self.destination_position = QtCore.QPoint(center.x(), center.y()+20)

        # TODO : turn this into a context manager
        dragThread = threading.Thread(
            target=mouse_drag.mouseDrag,
            args=(self.source_position, self.destination_position),
        )
        dragThread.start()
        # cannot join, use non-blocking wait
        while dragThread.is_alive():
            QtTest.QTest.qWait(1000)

        # check that the drop had the desired effect
        assert self.view.model().rowCount() == 2
        assert self.view.model().index(0, 0, QtCore.QModelIndex()).data() == "orange"
        assert self.view.model().index(1, 0, QtCore.QModelIndex()).data() == "apple"

