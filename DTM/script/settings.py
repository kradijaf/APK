from PyQt6 import QtCore, QtWidgets

class Ui_Settings(object):
    '''
    - class for pop-up window for obtaining coordinate parameters for createContourLinesClick function used in programme´s main window (Ui_MainWindow class).

    - Methods:
        - setupUi(settings: QtWidgets.QDialog): Main function called by the constructor
        - retranslateUi(settings: QtWidgets.QDialog): Method created by Qt, necessary for running the program
    '''
    def setupUi(self, settings: QtWidgets.QDialog):
        settings.setObjectName("settings")
        settings.resize(353, 180)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=settings)
        self.buttonBox.setGeometry(QtCore.QRect(0, 130, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QtWidgets.QGroupBox(parent=settings)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 334, 102))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(parent=self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(parent=self.groupBox)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.groupBox)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(parent=self.groupBox)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 2, 1, 1)

        self.retranslateUi(settings)
        self.buttonBox.accepted.connect(settings.accept)
        self.buttonBox.rejected.connect(settings.reject) 
        QtCore.QMetaObject.connectSlotsByName(settings)

    def retranslateUi(self, settings: QtWidgets.QDialog) -> None:
        _translate = QtCore.QCoreApplication.translate
        settings.setWindowTitle(_translate("settings", "Dialog"))
        self.groupBox.setTitle(_translate("settings", "Contour line parameters"))
        self.label.setText(_translate("settings", "Minimum contour line height"))
        self.lineEdit.setText(_translate("settings", "0"))
        self.label_2.setText(_translate("settings", "m"))
        self.label_4.setText(_translate("settings", "Maximum contour line height"))
        self.lineEdit_2.setText(_translate("settings", "3000"))
        self.label_3.setText(_translate("settings", "m"))
        self.label_6.setText(_translate("settings", "Minimum contour line height interval"))
        self.lineEdit_3.setText(_translate("settings", "1"))
        self.label_5.setText(_translate("settings", "m"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    settings = QtWidgets.QDialog()
    ui = Ui_Settings()
    ui.setupUi(settings)
    settings.show()
    sys.exit(app.exec())
