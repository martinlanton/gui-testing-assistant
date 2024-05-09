# TODO : there's a good indication of how that can be done in here :
#  https://stackoverflow.com/questions/24144482/how-to-test-drag-and-drop-behavior-in-pyqt?rq=3
import sys
import threading
from PySide6 import QtTest, QtWidgets, QtCore

from gui_testing_assistant import module_one
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

        source_index = model.index(0, 0, QtCore.QModelIndex())
        source_item_rect = cls.view.visualRect(source_index)
        cls.source_position = source_item_rect.center()

        destination_index = model.index(1, 0, QtCore.QModelIndex())
        destination_item_rect = cls.view.visualRect(destination_index)
        cls.destination_position = destination_item_rect.center()

    def test_module_one(self):
        assert module_one.my_first_var

    def test_module_two(self):
        assert v_2 == 2

    def test_drag_and_drop(self):
        # TODO : turn this into a context manager
        dragThread = threading.Thread(
            target=module_one.mouseDrag,
            args=(self.source_position, self.destination_position),
        )
        dragThread.start()
        # cannot join, use non-blocking wait
        while dragThread.is_alive():
            QtTest.QTest.qWait(1000)

        # check that the drop had the desired effect
        assert self.view.model().rowCount() > 0
