# TODO : there's a good indication of how that can be done in here :
#  https://stackoverflow.com/questions/24144482/how-to-test-drag-and-drop-behavior-in-pyqt?rq=3
import threading
import unittest
from PySide6 import QtTest

from gui_testing_assistant import module_one
from two.module_two import my_second_var as v_2

from tests.fixtures import list_view


class TestMouseMove:
    def setup_method(self):
        pass
    #     self.view = list_view.DraggableListView()
    #     model = list_view.DraggableListModel()
    #     model.setStringList(["apple", "orange"])
    #     self.view.setModel(model)
    #     # self.view.show()
    #
    #     source_index = model.index(row=0, column=0)
    #     source_item_rect = self.view.visualRect(source_index)
    #     self.source_position = source_item_rect.center()
    #
    #     destination_index = model.index(row=1, column=0)
    #     destination_item_rect = self.view.visualRect(destination_index)
    #     self.destination_position = destination_item_rect.center()

    def test_module_one(self):
        assert module_one.my_first_var

    def test_module_two(self):
        assert v_2 == 2

    def test_drag_and_drop(self):
        pass
        # # TODO : turn this into a context manager
        # dragThread = threading.Thread(target=mouseDrag, args=((self.source_position),
        #                                                       (self.destination_position)))
        # dragThread.start()
        # # cannot join, use non-blocking wait
        # while dragThread.is_alive():
        #     QtTest.QTest.qWait(1000)
        #
        # # check that the drop had the desired effect
        # assert self.dest_widget.hasItemCount() > 0
