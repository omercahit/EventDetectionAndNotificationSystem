# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_uii(object):
    def setupUi(self, uii):
        uii.setObjectName("uii")
        uii.resize(357,202)
        self.widget = QtWidgets.QWidget(uii)
        self.widget.setGeometry(QtCore.QRect(0,0, 361, 201))
        self.widget.setAutoFillBackground(True)
        self.widget.setObjectName("widget")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(80, 130, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setGeometry(QtCore.QRect(80, 40, 211, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.retranslateUi(uii)
        QtCore.QMetaObject.connectSlotsByName(uii)

    def retranslateUi(self, uii):
        _translate = QtCore.QCoreApplication.translate
        uii.setWindowTitle(_translate("uii", "Rasp Gui"))
        self.pushButton.setText(_translate("uii", "Onayla"))
        self.comboBox.setItemText(0, _translate("uii", "Dahil Et"))
        self.comboBox.setItemText(1, _translate("uii", "Çıkar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    uii = QtWidgets.QWidget()
    ui = Ui_uii()
    ui.setupUi(uii)
    uii.show()
    sys.exit(app.exec_())