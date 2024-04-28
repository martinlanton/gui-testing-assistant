from PySide6 import QtCore, QtWidgets


class DraggableListModel(QtCore.QStringListModel):
    def supportedDropActions(self):
        return QtCore.Qt.MoveAction

    def flags(self, index):
        default_flags = super().flags(index)
        if index.isValid():
            return default_flags | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled
        else:
            return default_flags | QtCore.Qt.ItemIsDropEnabled

    def mimeData(self, indexes):
        mime_data = super().mimeData(indexes)
        encoded_data = QtCore.QByteArray()
        stream = QtCore.QDataStream(encoded_data, QtCore.QIODevice.WriteOnly)
        for index in indexes:
            if index.isValid():
                text = self.data(index, QtCore.Qt.DisplayRole)
                stream.writeString(text)
        mime_data.setData('application/vnd.text.list', encoded_data)
        return mime_data

    def dropMimeData(self, data, action, row, column, parent):
        if action == QtCore.Qt.IgnoreAction:
            return True
        if not data.hasFormat('application/vnd.text.list'):
            return False
        if column > 0:
            return False
        if row != -1:
            begin_row = row
        elif parent.isValid():
            begin_row = parent.row()
        else:
            begin_row = self.rowCount()
        encoded_data = data.data('application/vnd.text.list')
        stream = QtCore.QDataStream(encoded_data, QtCore.QIODevice.ReadOnly)
        new_items = []
        rows = 0
        while not stream.atEnd():
            text = stream.readString()
            new_items.append(text)
            rows += 1
        self.insertRows(begin_row, rows, QtCore.QModelIndex())
        for text in new_items:
            index = self.index(begin_row, 0, QtCore.QModelIndex())
            self.setData(index, text)
            begin_row += 1
        return True


class DraggableListView(QtWidgets.QListView):
    def __init__(self, parent=None):
        super(DraggableListView, self).__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QtWidgets.QListView.InternalMove)


class MainApp(QtWidgets.QApplication):
    def __init__(self):
        QtWidgets.QApplication.__init__(self, [])
        self.view = DraggableListView()
        self.model = DraggableListModel()
        self.model.setStringList(["apple", "orange"])
        self.view.setModel(self.model)
        self.view.show()


if __name__ == '__main__':
    app = MainApp()
    app.exec()
