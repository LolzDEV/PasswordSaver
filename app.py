import sys
from main import Ui_MainWindow
from main import Ui_Dialog
from PyQt5 import QtCore, QtGui, QtWidgets
import base64
import os
import json


class App:
    if not os.path.isdir(os.path.expanduser("~") + "/.passwordholder"):
        os.mkdir(os.path.expanduser("~") + "/.passwordholder")
    if not os.path.isfile(os.path.expanduser("~") + "/.passwordholder/passwords.json"):
        file = open(os.path.expanduser("~") + "/.passwordholder/passwords.json", "w")
        file.write("{}")
        file.close()
    app = QtWidgets.QApplication(sys.argv)
    dialog = Ui_Dialog()
    DialogWindow = QtWidgets.QDialog()
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    table = None
    file = open(os.path.expanduser("~") + "/.passwordholder/passwords.json", "r")
    pswd = json.load(file)
    file.close()

    def __init__(self):
        self.dialog.setupUi(self.DialogWindow)
        self.ui.setupUi(self.MainWindow)
        self.ui.pushButton.clicked.connect(self.on_add_click)
        self.ui.pushButton_2.clicked.connect(self.copy)
        self.table = self.ui.tableWidget
        self.loadTable()
        self.MainWindow.show()
        self.DialogWindow.hide()

        sys.exit(self.app.exec_())

    def cancel(self):
        self.dialog.lineEdit.setText("")
        self.dialog.lineEdit_2.setText("")
        self.DialogWindow.destroy()

    def ok(self):
        if not self.dialog.lineEdit.text() == "" and not self.dialog.lineEdit_2.text() == "" and not self.dialog.lineEdit_3.text() in self.pswd:
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)
            self.table.setColumnCount(3)
            self.table.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(self.dialog.lineEdit_3.text()))
            self.table.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(self.dialog.lineEdit.text()))
            self.table.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(
                str(base64.b85encode(bytes(self.dialog.lineEdit_2.text().encode("UTF-8"))))))
            self.pswd[self.dialog.lineEdit_3.text()] = {"user": self.dialog.lineEdit.text(), "password": str(
                base64.b85encode(bytes(self.dialog.lineEdit_2.text().encode("UTF-8"))))}
            json.dump(self.pswd, open(os.path.expanduser("~") + "/.passwordholder/passwords.json", "w"))
        self.loadTable()
        self.cancel()

    def on_add_click(self):
        self.DialogWindow.show()
        self.dialog.pushButton.clicked.connect(self.ok)
        self.dialog.pushButton_2.clicked.connect(self.cancel)

    def copy(self):
        col = self.table.currentColumn()
        text = self.table.currentItem().text()
        self.app.clipboard().setText(text)

    def loadTable(self):
        self.table.clear()
        self.table.setRowCount(0)
        for k in self.pswd.keys():
            print(k)
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)
            self.table.setColumnCount(3)
            self.table.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(k))
            self.table.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(self.pswd[k]["user"]))
            self.table.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(self.pswd[k]["password"]))


if __name__ == "__main__":
    App()
