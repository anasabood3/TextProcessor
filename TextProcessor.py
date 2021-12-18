import pickle
import sys

from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QPushButton, QAction, QTextEdit, QLineEdit, QMessageBox

from Detector import Detector
from Item import Item
from data import load_data, save_data
from data import load_data
from table import Table

Errors = load_data("Errors.pkl")


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        # load UI
        uic.loadUi("assets/UIs/main2.ui", self)
        # Special Elements
        self.data_ls = []
        self.detector = Detector()
        self.patterns = load_data("patterns.pkl")
        self.cities = load_data("cities.pkl")
        self.table = Table(self.data_ls)
        self.saving_path = ""

        # Actions
        # menuFile
        self.auto_action = self.findChild(QAction, "AutoAction")
        self.batch_action = self.findChild(QAction, "BatchAction")
        self.exit_action = self.findChild(QAction, "QuitAction")

        # menuEdit
        self.undo_action = self.findChild(QAction, "actionUndo")
        self.redo_action = self.findChild(QAction, "actionRedo")

        # menuList
        self.display_list_action = self.findChild(QAction, "actionDisplay_List")
        self.clear_list_action = self.findChild(QAction, "actionClear_List")
        self.save_list_action = self.findChild(QAction, "actionSave_List")
        self.load_list_action = self.findChild(QAction, "actionImport_List")

        # menuHelp
        self.about_action = self.findChild(QAction, "actionAbout")

        # Text areas and text lines
        self.text_area = self.findChild(QTextEdit, "input_space")
        self.sender_line = self.findChild(QLineEdit, "Sender")
        self.receiver_line = self.findChild(QLineEdit, "Receiver")
        self.area_line = self.findChild(QLineEdit, "Destination")
        self.amount_line = self.findChild(QLineEdit, "Amount")
        self.ph_number_line = self.findChild(QLineEdit, "PhNumber")

        # Buttons
        self.generate_btn = self.findChild(QPushButton, "Generate")
        self.add_to_list_btn = self.findChild(QPushButton, "AddIntoList")

        # Misc
        self.pattern = self.findChild(QComboBox, "Pattern")
        self.status = self.findChild(QStatusBar, "statusbar")

        # print()
        # ActionListeners
        self.generate_btn.clicked.connect(
            lambda: self.organize(self.text_area.toPlainText(), self.batch_action.isChecked()))

        self.add_to_list_btn.clicked.connect(lambda: self.add_items([Item(self.sender_line.text(),
                                                                          self.receiver_line.text(),
                                                                          self.ph_number_line.text(),
                                                                          self.area_line.text(),
                                                                          self.amount_line.text())],
                                                                    self.batch_action.isChecked()))

        self.exit_action.triggered.connect(lambda: self.quit())
        self.about_action.triggered.connect(lambda: self.show_about())
        self.undo_action.triggered.connect(lambda: self.undo())
        self.clear_list_action.triggered.connect(lambda: self.verify_clear())
        self.display_list_action.triggered.connect(lambda: self.display_ls())
        self.load_list_action.triggered.connect(lambda: self.load_list())
        self.save_list_action.triggered.connect(lambda: self.save_list(self.data_ls))
        self.batch_action.triggered.connect(lambda: self.refresh(self.auto_action))

        # lset
        sshFile = "assets/styles/style.qss"
        with open(sshFile, "r") as fh:
            self.setStyleSheet(fh.read())
        self.setWindowTitle("Text Processor")
        self.setWindowIcon(QtGui.QIcon("assets/images/logo.png"))
        # find the widgets in the xml file

    def refresh(self, action):
        action.setEnabled(not (action.isEnabled()))
        if not action.isChecked():
            action.setChecked(True)
        else:
            pass

    def organize(self, text_to_process, batch):
        if text_to_process != "":
            if batch:
                extracted_data = self.detector.detect(text_to_process, batch)
                self.add_items(extracted_data, batch)
            else:
                if len(list(filter(lambda item: item != "", text_to_process.splitlines()))) > 6:
                    self.show_message("Batch Recommended")
                else:
                    extracted_data = self.detector.detect(text_to_process, batch)[0]
                    self.sender_line.setText(extracted_data.sender)
                    self.receiver_line.setText(extracted_data.receiver)
                    self.area_line.setText(extracted_data.destination)
                    self.amount_line.setText(extracted_data.amount)
                    self.ph_number_line.setText(extracted_data.phone_number)
                    if self.auto_action.isChecked():
                        self.add_items([Item(self.sender_line.text(), self.receiver_line.text(),
                                             self.ph_number_line.text(), self.area_line.text(),
                                             self.amount_line.text())], batch)

        else:
            self.status.showMessage("No valid Input", 3000)

    def add_items(self, data, batch):
        try:
            if batch:
                if data:
                    for i in data:
                        if not i in self.data_ls:
                            self.data_ls.append(i)
                        else:
                            self.status.showMessage("Duplicate Element were Detected")
                    message = str(len(self.data_ls)) + "Item(s) added to list"
                    self.status.showMessage(message, 1500)
                else:
                    self.status.showMessage("Can`t Add Empty Item", 3000)
            else:
                if data[0].__iter__() != ["", "", "", "", ""]:
                    if not data[0] in self.data_ls:
                        self.data_ls.extend(data)
                        message = str(len(self.data_ls)) + "Item(s) added to list"
                        self.status.showMessage(message, 1500)
                    else:
                        self.status.showMessage("Element is Already Exist in list", 3000)
                else:
                    self.status.showMessage("Can`t Add Empty Item", 3000)
        except Exception as e:
            self.status.showMessage("Error:" + str(e), 3000)

    def save_list(self, data):
        if self.data_ls:
            if self.saving_path == "":
                options = QFileDialog.Options()
                save_dir = QFileDialog.getSaveFileName(self, "Save list into ...",
                                                       "C:\\Users\\anas-1024\\Documents\\list.pkl",
                                                       "Pickle Files (*.pkl)",
                                                       options=options)
                saved_dir = save_dir[0]
                if saved_dir != "":
                    file = open(saved_dir, 'wb')
                    pickle.dump(data, file)
                    file.close()
                    self.status.showMessage("List was saved into:  " + saved_dir, 1500)
                    self.saving_path = saved_dir
                else:
                    pass
            else:
                file = open(self.saving_path, 'wb')
                pickle.dump(data, file)
                file.close()
                self.status.showMessage("List was saved into:  " + self.saving_path, 1500)
        else:
            self.status.showMessage("List is Empty", 1500)

    def load_list(self):
        options = QFileDialog.Options()
        save_dir = QFileDialog.getOpenFileName(self, "Load list from ...",
                                               "C:\\Users\\anas-1024\\Documents\\list.pkl", "Pickle Files (*.pkl)",
                                               options=options)
        open_dir = save_dir[0]
        if open_dir != "":
            file = open(open_dir, 'rb')
            self.data_ls = pickle.load(file)
            setattr(self.table, "data", self.data_ls)
            self.status.showMessage(str(len(self.data_ls)) + "Item(s) were loaded", 1500)
        else:
            pass

    def display_ls(self):
        try:
            self.table.run_window()
        except Exception as e:
            self.status.showMessage("Error:" + str(e), 3000)

    def undo(self):
        if self.data_ls:
            self.data_ls.pop()
            self.status.showMessage('Adding was Undone', 1500)
            message = str(len(self.data_ls)) + "Item(s) added to list"
            self.status.showMessage(message, 1500)

    def clear_list(self):
        if self.data_ls:
            self.data_ls.clear()
            self.status.showMessage('List has been Cleared', 1500)
        else:
            self.status.showMessage('List is Empty', 1500)

    def show_about(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("About")
        msg.setWindowIcon(QtGui.QIcon("assets/images/help.png"))
        msg.setText("This Program was made as a simple tool for extracting entities from money transfer meassges\nand log them into a file, for archiving for more information: \nanasabood3@gmail.com")
        msg.exec_()

    def show_message(self, title):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setWindowIcon(QtGui.QIcon("assets/images/error icon.png"))
        msg.setText(Errors[title])
        msg.exec_()

    def quit(self):
        for i in self.data_ls:
            if not (i.destination in self.cities) and i != "":
                self.cities.append(i.destination)
        save_data("cities.pkl", self.cities)
        self.close()

    def verify_clear(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Do you really want to clear all items ?")
        msgBox.setWindowTitle("Clear all items")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            self.clear_list()

    def closeEvent(self, event):
        """Generate 'question' dialog on clicking 'X' button in title bar.

        Reimplement the closeEvent() event handler to include a 'Question'
        dialog with options on how to proceed - Save, Close, Cancel buttons
        """
        reply = QMessageBox.question(
            self, "Message",
            "Are you sure you want to quit? Any unsaved work will be lost.",
            QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel, QMessageBox.Save)

        if reply == QMessageBox.Close:
            self.quit()
        elif reply == QMessageBox.Save:
            self.save_list(self.data_ls)
        else:
            event.ignore()

    # def contextMenuEvent(self, event):
    #     contextMenu = QMenu(self)
    #     newAct = contextMenu.addAction("New")
    #     openAct = contextMenu.addAction("Open")
    #     quitAct = contextMenu.addAction("Quit")
    #     action = contextMenu.exec_(self.mapToGlobal(event.pos()))
    #     if action == quitAct:
    #         self.close()


app = QApplication(sys.argv)
window = UI()
window.show()
app.exec_()
