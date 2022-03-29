import pyqtgraph as pg
import time
import pandas as pd
import numpy as np
from tkinter import Y
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib import cm
from copy import deepcopy


class Ui_graphScreen(object):
    """Screen to display words"""

    def setupUi(self, mainScreen, **kwargs):
        self.screenName = "graphScreen"
        self.mainScreen = mainScreen
        self.data = self.mainScreen.data

        graphType = kwargs.get("graphType")
        graphLimits = deepcopy(kwargs.get("graphLimits"))

        self.d0 = (int(time.time())+time.localtime().tm_gmtoff)//(3600*24)
        self.firstDay = (self.data["logs"][0]["time"] +
                         self.data["logs"][0]["localTime"])//(3600*24)
        self.lastDay = max([self.data["words"][i]["date"]+self.data["words"]
                           [i]["localTime"] for i in range(len(self.data["words"]))])//(3600*24)

        # Create layout for the screen: start
        self.mainScreen.setObjectName("mainScreen")
        self.centralwidget = QtWidgets.QWidget(self.mainScreen)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(30, 30, 30, 30)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.graphWidget = pg.PlotWidget()
        self.verticalLayout_2.addWidget(self.graphWidget)

        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.returnButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.returnButton.setFont(font)
        self.returnButton.setObjectName("returnButton")
        self.verticalLayout.addWidget(self.returnButton)

        self.verticalLayout.setStretch(1, 1)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.mainScreen.setCentralWidget(self.centralwidget)
        # Create layout for the screen: end

        # Assign functions to buttons
        self.returnButton.clicked.connect(self.mainScreen.close)

        self.retranslateUi(self.mainScreen)
        QtCore.QMetaObject.connectSlotsByName(self.mainScreen)

        # Assign shortcuts to buttons
        self.returnButton.setShortcut("Ctrl+Q")

        # Modify labels and graph displayed for given graphType
        if graphType == "wordsDaily":
            self.label.setText("Words daily graph")
            self.createWordsDailyGraph(self.calculateLimits(graphLimits, True))
        elif graphType == "wordsTypesDaily":
            self.label.setText("Words types daily graph")
            self.createWordsTypesDailyGraph(self.calculateLimits(graphLimits))
        elif graphType == "wordsFromPreviousDaysDaily":
            self.label.setText("Words from previous days daily graph")
            self.createWordsFromPreviousDaysDailyGraph(
                self.calculateLimits(graphLimits))
        elif graphType == "accuracyDaily":
            self.label.setText("Accuracy daily")
            self.createAccuracyDailyGraph(self.calculateLimits(graphLimits))
        elif graphType == "wordsTypesHistory":
            self.label.setText("Words types history")
            self.createWordsTypesHistoryGraph(
                self.calculateLimits(graphLimits))

    def createWordsDailyGraph(self, graphLimits):
        """Create words daily graph

        :param graphLimits: list() of two int limits
        """

        x = [i for i in range(graphLimits[0], graphLimits[1]+1)]
        wordData = []
        for i in x:
            if str(i-(self.firstDay-self.d0)) in self.data["logsSave"].keys():
                wordData.append(self.data["logsSave"][str(
                    i-(self.firstDay-self.d0))]["1"]+[0])
            else:
                wordData.append([0, 0, 0])

        for j, i in enumerate(self.data["words"]):
            try:
                day = int((i["date"]+i["localTime"])//(3600*24)-self.d0)
                wordData[x.index(day)][2] += 1
            except:
                pass

        df = pd.DataFrame({"x": x,
                           "y1": [i[0] for i in wordData],
                           "y2": [i[1] for i in wordData],
                           "y3": [i[2] for i in wordData]})
        df = df.set_index("x")

        bottom = np.zeros(len(df))
        cmap = cm.get_cmap("tab10")
        colors = [tuple(255*x for x in cmap(i/10))[:-1]
                  for i in range(len(df.columns))]

        for col, color in zip(df.columns, colors):
            bargraph = pg.BarGraphItem(x=df.index, height=df[col], y0=bottom, width=0.6, brush=pg.mkBrush(
                color=color), pen=pg.mkPen(color=color))
            self.graphWidget.addItem(bargraph)
            bottom += df[col]

    def createWordsTypesDailyGraph(self, graphLimits):
        """Create words types daily graph

        :param graphLimits: list() of two int limits
        """

        x = [i for i in range(graphLimits[0], graphLimits[1]+1)]
        wordData = []
        for i in x:
            if str(int(i)-(self.firstDay-self.d0)) in self.data["logsSave"]:
                wordData.append(self.data["logsSave"][str(
                    int(i)-(self.firstDay-self.d0))]["2"])
            else:
                wordData.append([0, 0, 0, 0, 0, 0])

        df = pd.DataFrame({"x": x,
                           "y1": [i[0] for i in wordData],
                           "y2": [i[1] for i in wordData],
                           "y3": [i[2] for i in wordData],
                           "y4": [i[3] for i in wordData],
                           "y5": [i[4] for i in wordData],
                           "y6": [i[5] for i in wordData]})
        df = df.set_index("x")

        bottom = np.zeros(len(df))
        cmap = cm.get_cmap("tab10")
        colors = [tuple(255*x for x in cmap(i/10))[:-1]
                  for i in range(len(df.columns))]

        for col, color in zip(df.columns, colors):
            bargraph = pg.BarGraphItem(x=df.index, height=df[col], y0=bottom, width=0.6, brush=pg.mkBrush(
                color=color), pen=pg.mkPen(color=color))
            self.graphWidget.addItem(bargraph)
            bottom += df[col]

    def createWordsFromPreviousDaysDailyGraph(self, graphLimits):
        """Create words frpm previous days daily graph

        :param graphLimits: list() of two int limits
        """

        x = [i for i in range(graphLimits[0], graphLimits[1]+1)]
        wordData = []
        for i in x:
            if str(int(i)-(self.firstDay-self.d0)) in self.data["logsSave"]:
                wordData.append(self.data["logsSave"][str(
                    int(i)-(self.firstDay-self.d0))]["3"])
            else:
                wordData.append([0, 0, 0, 0, 0, 0])

        df = pd.DataFrame({"x": x,
                           "y1": [i[0] for i in wordData],
                           "y2": [i[1] for i in wordData],
                           "y3": [i[2] for i in wordData],
                           "y4": [i[3] for i in wordData],
                           "y5": [i[4] for i in wordData],
                           "y6": [i[5] for i in wordData]})
        df = df.set_index("x")

        bottom = np.zeros(len(df))
        cmap = cm.get_cmap("tab10")
        colors = [tuple(255*x for x in cmap(i/10))[:-1]
                  for i in range(len(df.columns))]

        for col, color in zip(df.columns, colors):
            bargraph = pg.BarGraphItem(x=df.index, height=df[col], y0=bottom, width=0.6, brush=pg.mkBrush(
                color=color), pen=pg.mkPen(color=color))
            self.graphWidget.addItem(bargraph)
            bottom += df[col]

    def createAccuracyDailyGraph(self, graphLimits):
        """Create accuracy daily graph

        :param graphLimits: list() of two int limits
        """

        toDelete = 0
        x = [i for i in range(graphLimits[0], graphLimits[1]+1)]
        if int(x[0])-6 > self.firstDay-self.d0:
            toDelete = 6
            x = [str(i) for i in range(int(x[0])-6, int(x[0]))]+x
        elif int(x[0]) > self.firstDay-self.d0:
            toDelete = self.firstDay-self.d0-int(x[0])
            x = [str(i) for i in range(int(x[0]), int(x[0]))]+x

        wordData = []
        for i in x:
            if str(int(i)-(self.firstDay-self.d0)) in self.data["logsSave"]:
                wordData.append(self.data["logsSave"][str(
                    int(i)-(self.firstDay-self.d0))]["4"])
            else:
                wordData.append([0, 0])

        accuracyDaily = [i[0]/i[1] if i[1] > 0 else 0 for i in wordData]
        for i in range(len(accuracyDaily)):
            if accuracyDaily[i] == 0:
                accuracyDaily.pop(i)
                x.pop(i)

        average3 = [sum(accuracyDaily[max(0, i-2):i+1])/min(i+1, 3)
                    for i in range(len(accuracyDaily))]
        average7 = [sum(accuracyDaily[max(0, i-6):i+1])/min(i+1, 7)
                    for i in range(len(accuracyDaily))]

        for _ in range(0, toDelete):
            x.pop(0)
            accuracyDaily.pop(0)
            average3.pop(0)
            average7.pop(0)

        df = pd.DataFrame({"x": x,
                           "y1": accuracyDaily,
                           "y2": average3,
                           "y3": average7})
        df = df.set_index("x")

        cmap = cm.get_cmap("tab10")
        colors = [tuple(255*x for x in cmap(i/10))[:-1]
                  for i in range(len(df.columns))]

        self.graphWidget.addLegend(offset=-1, labelTextSize="12pt",
                                   labelTextColor=QtGui.QColor(0, 0, 0), brush=QtGui.QColor(255, 255, 255))
        for col, color in zip(df.columns, colors):
            if col == "y1":
                bargraph = pg.BarGraphItem(x=df.index, height=df[col], width=0.6, brush=pg.mkBrush(
                    color=color), pen=pg.mkPen(color=color))
                self.graphWidget.addItem(bargraph)
            elif col == "y2":
                self.graphWidget.plot(x, average3, pen=pg.mkPen(
                    color=color), name="Accuracy 3 day average")
            elif col == "y3":
                self.graphWidget.plot(x, average7, pen=pg.mkPen(
                    color=color), name="Accuracy 7 day average")

    def createWordsTypesHistoryGraph(self, graphLimits):
        """Create words types history graph

        :param graphLimits: list() of two int limits
        """

        x = [i for i in range(graphLimits[0], graphLimits[1]+1)]
        wordData = []

        for i in x:
            if str(int(i)-(self.firstDay-self.d0)) in self.data["logsSave"]:
                wordData.append(self.data["logsSave"][str(
                    int(i)-(self.firstDay-self.d0))]["5"])
            else:
                wordData.append(self.data["logsSave"][str(
                    int(i)-(self.firstDay-self.d0)-1)]["5"])

        df = pd.DataFrame({"x": x,
                           "y1": [i[0] for i in wordData],
                           "y2": [i[1] for i in wordData],
                           "y3": [i[2] for i in wordData],
                           "y4": [i[3] for i in wordData],
                           "y5": [i[4] for i in wordData]})
        df = df.set_index("x")

        bottom = np.zeros(len(df))
        cmap = cm.get_cmap("tab10")
        colors = [tuple(255*x for x in cmap(i/10))[:-1]
                  for i in range(len(df.columns))]

        for col, color in zip(df.columns, colors):
            bargraph = pg.BarGraphItem(x=df.index, height=df[col], y0=bottom, width=0.6, brush=pg.mkBrush(
                color=color), pen=pg.mkPen(color=color))
            self.graphWidget.addItem(bargraph)
            bottom += df[col]

    def calculateLimits(self, graphLimits, allowFuture=False):
        """Calculate and confirm limits for graphs

        :param graphLimits: list() of two string limits,
        :param allowFuture: bool if future values are allowed for the limits calculation
        """

        if graphLimits[0] != "":
            graphLimits[0] = int(graphLimits[0])
        else:
            graphLimits[0] = self.firstDay-self.d0

        self.mainScreen.viewLogsScreen.deliberateZero = False
        if graphLimits[1] != "":
            graphLimits[1] = int(graphLimits[1])
            if graphLimits[1] == 0:
                self.mainScreen.viewLogsScreen.deliberateZero = True
        else:
            graphLimits[1] = self.lastDay-self.d0

        if graphLimits[0] > graphLimits[1]:
            graphLimits[0] = self.firstDay-self.d0
            graphLimits[1] = self.lastDay-self.d0

        graphLimits[0] = max(graphLimits[0], self.firstDay-self.d0)
        graphLimits[1] = min(graphLimits[1], self.lastDay-self.d0)

        if not allowFuture:
            if graphLimits[0] > 0:
                graphLimits[0] = self.firstDay-self.d0
            if graphLimits[1] > 0:
                graphLimits[1] = 0

        return [int(graphLimits[0]), int(graphLimits[1])]

    def retranslateUi(self, mainScreen):
        _translate = QtCore.QCoreApplication.translate
        mainScreen.setWindowTitle(_translate("mainScreen", "Graph"))
        self.label.setText(_translate("mainScreen", "Graph"))
        self.returnButton.setText(_translate("mainScreen", "Return"))
