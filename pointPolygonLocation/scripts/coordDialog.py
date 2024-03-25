from PyQt6 import QtCore, QtGui, QtWidgets

class UiDialog(QtWidgets.QDialog):
    '''
    - Class for pop-up window used for obtaining float coordinates of tested point.

    - parameters:
        - QtWidgets.QDialog - Parent class

    - Methods:
        - setupUi() - Main function called by the constructor
        - setCoordsAccept() - Sets line edits´ text as coordinates when OK button is pressed, closes the window with 'accept' parameter
        - getCoords() - returns the coordinates
        - retranslateUi() - Method created by Qt, necessary for running the window
    '''
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(351, 102)
        self.line_edit1 = QtWidgets.QLineEdit(parent=self)
        self.line_edit1.setGeometry(QtCore.QRect(25, 65, 200, 21))
        self.line_edit1.setText("")
        self.line_edit1.setObjectName("lineEdit_2")
        self.line_edit = QtWidgets.QLineEdit(parent=self)
        self.line_edit.setGeometry(QtCore.QRect(25, 15, 200, 21))
        self.line_edit.setText("")
        self.line_edit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(parent=self)
        self.label.setGeometry(QtCore.QRect(10, 17, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label1 = QtWidgets.QLabel(parent=self)
        self.label1.setGeometry(QtCore.QRect(10, 67, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label1.setFont(font)
        self.label1.setObjectName("label_2")
        self.push_button = QtWidgets.QPushButton(parent=self)
        self.push_button.setGeometry(QtCore.QRect(240, 40, 100, 24))
        self.push_button.setObjectName("pushButton")
        self.line_edit.setText('0')
        self.line_edit1.setText('0')
        self.line_edit.setFocus()
        self.x = None
        self.y = None

        self.retranslateUi(self)
        self.push_button.clicked.connect(self.setCoordsAccept)
        QtCore.QMetaObject.connectSlotsByName(self)

    def setCoordsAccept(self):
        self.x = self.line_edit.text()
        self.y = self.line_edit1.text()
        self.accept()

    def getCoords(self):
        return self.x, self.y

    def retranslateUi(self, Dialog):
        translate_func = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(translate_func("Dialog", "Input new coordinates"))
        self.label.setText(translate_func("Dialog", "X:"))
        self.label1.setText(translate_func("Dialog", "Y:"))
        self.push_button.setText(translate_func("Dialog", "Apply"))