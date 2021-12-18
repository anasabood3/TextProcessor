from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import *
from openpyxl import Workbook

from data import load_data
Errors = load_data("Errors.pkl")


class Table(QMainWindow):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, data):
        super().__init__()
        uic.loadUi("assets/UIs/table2.ui", self)
        self.data_table = self.findChild(QTableWidget, "DataTable")
        self.setWindowIcon(QtGui.QIcon("assets/images/table.png"))
        self.data = data
        self.data_table.cellChanged.connect(self.cellchanged)
        self.Export.clicked.connect(lambda: self.save_as(data=self.data))
        self.Cancel.clicked.connect(lambda: self.close())
        self.status = self.findChild(QStatusBar, "statusbar")
        sshFile = "assets/styles/style.qss"
        with open(sshFile, "r") as fh:
            self.setStyleSheet(fh.read())

    def addTableRow(self, row_data):
        row = self.data_table.rowCount()
        self.data_table.setRowCount(row + 1)
        col = 0
        for item in row_data.__iter__():
            cell = QTableWidgetItem(str(item))
            self.data_table.setItem(row, col, cell)
            col += 1

    def run_window(self):
        for i in range(self.data_table.rowCount()):
            while self.data_table.rowCount() > 0:
                self.data_table.removeRow(self.data_table.rowCount() - 1)
        # self.data_table.clear()
        for i in range(len(self.data)):
            self.addTableRow(self.data[i])
        self.show()

    def sync_data(self):
        pass

    def cellchanged(self):
        try:
            current_item = self.data_table.currentRow()
            current_attr = self.data_table.currentColumn()
            cell_value = self.data_table.item(current_item, current_attr)
            setattr(self.data[current_item], list(self.data[current_item].__dict__.keys())[current_attr],
                    cell_value.text())
        except:
            pass

    def delete_item(self):
        try:
            row = self.data_table.currentRow()
            self.data_table.removeRow(row)
            del self.data[row]
        except:
            pass

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        delAct = contextMenu.addAction("Delete Item")
        quitAct = contextMenu.addAction("Quit")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == delAct:
            self.delete_item()
        elif action == quitAct:
            self.closeEvent(event)

    def show_message(self, title):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setWindowIcon(QtGui.QIcon("assets/images/error icon.png"))
        msg.setText(Errors[title])
        msg.exec_()

    def save_as(self, data):
        if self.data:
            options = QFileDialog.Options()
            save_dir = QFileDialog.getSaveFileName(self, "Save generated list into ...",
                                                   "C:\\Users\\anas-1024\\Documents\\d.xlsx", "Excel Files (*.xlsx)",
                                                   options=options)
            saved_dir = save_dir[0]

            if saved_dir != "":
                try:
                    workbook = Workbook()
                    sheet = workbook.active
                    for i in data:
                        reversed = i.__iter__().copy()
                        reversed.reverse()
                        sheet.append(tuple(reversed))
                    workbook.save(filename=saved_dir)
                    self.status.showMessage("List was Exported into:  " + saved_dir, 1500)
                except:
                    self.show_message("Saving Error")
            else:
                pass
        else:
            self.show_message("Empty List")
