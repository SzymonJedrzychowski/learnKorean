from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial


class Ui_modifySetScreen(object):
    """Screen for modyfying set"""

    def setupUi(self, mainScreen, **kwargs):
        self.screenName = "modifySetScreen"
        self.mainScreen = mainScreen

        # Create layout for the screen: start
        self.mainScreen.setObjectName("mainScreen")
        self.centralwidget = QtWidgets.QWidget(self.mainScreen)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem)

        self.addWordsButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.addWordsButton.setFont(font)
        self.addWordsButton.setObjectName("addWordsButton")
        self.verticalLayout.addWidget(self.addWordsButton)

        self.removeWordsButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.removeWordsButton.setFont(font)
        self.removeWordsButton.setObjectName("removeWordsButton")
        self.verticalLayout.addWidget(self.removeWordsButton)

        self.modifyWordsButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.modifyWordsButton.setFont(font)
        self.modifyWordsButton.setObjectName("addWordsButton")
        self.verticalLayout.addWidget(self.modifyWordsButton)

        self.returnButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.returnButton.setFont(font)
        self.returnButton.setObjectName("returnButton")
        self.verticalLayout.addWidget(self.returnButton)

        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem1)

        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.mainScreen.setCentralWidget(self.centralwidget)
        # Create layout for the screen: end

        # Assign functions to buttons
        self.addWordsButton.clicked.connect(
            partial(self.mainScreen.useScreen, self.mainScreen.addWordsScreen))
        self.removeWordsButton.clicked.connect(
            partial(self.mainScreen.useScreen, self.mainScreen.removeWordsScreen))
        self.modifyWordsButton.clicked.connect(
            partial(self.mainScreen.useScreen, self.mainScreen.modifyWordsScreen))
        self.returnButton.clicked.connect(self.mainScreen.close)

        self.retranslateUi(self.mainScreen)
        QtCore.QMetaObject.connectSlotsByName(self.mainScreen)

        # Assign shortcuts to buttons
        self.addWordsButton.setShortcut("Ctrl+1")
        self.removeWordsButton.setShortcut("Ctrl+2")
        self.modifyWordsButton.setShortcut("Ctrl+3")
        self.returnButton.setShortcut("Ctrl+Q")

    def retranslateUi(self, mainScreen):
        _translate = QtCore.QCoreApplication.translate
        mainScreen.setWindowTitle(_translate("mainScreen", "MainWindow"))
        self.label.setText(_translate("mainScreen", "Modify set"))
        self.addWordsButton.setText(_translate("mainScreen", "Add words"))
        self.removeWordsButton.setText(
            _translate("mainScreen", "Remove words"))
        self.modifyWordsButton.setText(
            _translate("mainScreen", "Modify words"))
        self.returnButton.setText(_translate("mainScreen", "Return"))
