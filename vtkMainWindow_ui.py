# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'vtkMainWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(899, 931)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        font = QFont()
        font.setKerning(True)
        self.centralwidget.setFont(font)
        self.centralwidget.setAutoFillBackground(False)
        self.gridLayout_5 = QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.styTy = QLCDNumber(self.frame)
        self.styTy.setObjectName(u"styTy")
        self.styTy.setAutoFillBackground(True)
        self.styTy.setFrameShadow(QFrame.Plain)
        self.styTy.setSegmentStyle(QLCDNumber.Flat)

        self.gridLayout_6.addWidget(self.styTy, 4, 1, 1, 1)

        self.label_12 = QLabel(self.frame)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label_12, 0, 2, 1, 1)

        self.camTx = QLCDNumber(self.frame)
        self.camTx.setObjectName(u"camTx")
        self.camTx.setAutoFillBackground(True)
        self.camTx.setFrameShadow(QFrame.Plain)
        self.camTx.setSegmentStyle(QLCDNumber.Flat)

        self.gridLayout_6.addWidget(self.camTx, 2, 2, 1, 1)

        self.camTz = QLCDNumber(self.frame)
        self.camTz.setObjectName(u"camTz")
        self.camTz.setAutoFillBackground(True)
        self.camTz.setFrameShadow(QFrame.Plain)
        self.camTz.setSegmentStyle(QLCDNumber.Flat)

        self.gridLayout_6.addWidget(self.camTz, 5, 2, 1, 1)

        self.camTy = QLCDNumber(self.frame)
        self.camTy.setObjectName(u"camTy")
        self.camTy.setAutoFillBackground(True)
        self.camTy.setFrameShadow(QFrame.Plain)
        self.camTy.setSegmentStyle(QLCDNumber.Flat)

        self.gridLayout_6.addWidget(self.camTy, 4, 2, 1, 1)

        self.label_13 = QLabel(self.frame)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_6.addWidget(self.label_13, 2, 0, 1, 1)

        self.label_15 = QLabel(self.frame)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_6.addWidget(self.label_15, 5, 0, 1, 1)

        self.label_14 = QLabel(self.frame)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_6.addWidget(self.label_14, 4, 0, 1, 1)

        self.styTx = QLCDNumber(self.frame)
        self.styTx.setObjectName(u"styTx")
        self.styTx.setAutoFillBackground(True)
        self.styTx.setFrameShadow(QFrame.Plain)
        self.styTx.setSegmentStyle(QLCDNumber.Flat)

        self.gridLayout_6.addWidget(self.styTx, 2, 1, 1, 1)

        self.styTz = QLCDNumber(self.frame)
        self.styTz.setObjectName(u"styTz")
        self.styTz.setAutoFillBackground(True)
        self.styTz.setFrameShadow(QFrame.Plain)
        self.styTz.setSegmentStyle(QLCDNumber.Flat)

        self.gridLayout_6.addWidget(self.styTz, 5, 1, 1, 1)

        self.label_11 = QLabel(self.frame)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label_11, 0, 1, 1, 1)

        self.styErr = QLCDNumber(self.frame)
        self.styErr.setObjectName(u"styErr")
        self.styErr.setAutoFillBackground(True)
        self.styErr.setFrameShadow(QFrame.Plain)
        self.styErr.setSegmentStyle(QLCDNumber.Flat)

        self.gridLayout_6.addWidget(self.styErr, 6, 1, 1, 1)

        self.camErr = QLCDNumber(self.frame)
        self.camErr.setObjectName(u"camErr")
        self.camErr.setAutoFillBackground(True)
        self.camErr.setFrameShadow(QFrame.Plain)
        self.camErr.setSegmentStyle(QLCDNumber.Flat)

        self.gridLayout_6.addWidget(self.camErr, 6, 2, 1, 1)

        self.label_16 = QLabel(self.frame)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_6.addWidget(self.label_16, 6, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 200, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.verticalSpacer_2, 7, 0, 1, 3)


        self.gridLayout_5.addWidget(self.frame, 0, 1, 1, 1)

        self.trackerwidget = QWidget(self.centralwidget)
        self.trackerwidget.setObjectName(u"trackerwidget")
        self.trackerGridLayout = QGridLayout(self.trackerwidget)
        self.trackerGridLayout.setObjectName(u"trackerGridLayout")

        self.gridLayout_5.addWidget(self.trackerwidget, 0, 0, 1, 1)

        self.videowidget = QWidget(self.centralwidget)
        self.videowidget.setObjectName(u"videowidget")
        self.videoGridLayout = QGridLayout(self.videowidget)
        self.videoGridLayout.setObjectName(u"videoGridLayout")

        self.gridLayout_5.addWidget(self.videowidget, 1, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 899, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QDockWidget(MainWindow)
        self.dockWidget.setObjectName(u"dockWidget")
        self.dockWidget.setFocusPolicy(Qt.NoFocus)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.imgFrame = QFrame(self.dockWidgetContents)
        self.imgFrame.setObjectName(u"imgFrame")
        self.imgFrame.setFrameShape(QFrame.StyledPanel)
        self.imgFrame.setFrameShadow(QFrame.Plain)
        self.gridLayout_3 = QGridLayout(self.imgFrame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setVerticalSpacing(4)
        self.imgCaptureButton = QPushButton(self.imgFrame)
        self.imgCaptureButton.setObjectName(u"imgCaptureButton")

        self.gridLayout_3.addWidget(self.imgCaptureButton, 1, 2, 1, 1)

        self.openCamSettingsButton = QPushButton(self.imgFrame)
        self.openCamSettingsButton.setObjectName(u"openCamSettingsButton")

        self.gridLayout_3.addWidget(self.openCamSettingsButton, 1, 1, 1, 1)

        self.label_6 = QLabel(self.imgFrame)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_6, 0, 1, 1, 2)


        self.verticalLayout.addWidget(self.imgFrame)

        self.frame_2 = QFrame(self.dockWidgetContents)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Plain)
        self.gridLayout_7 = QGridLayout(self.frame_2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setVerticalSpacing(3)
        self.trackerToggle = QPushButton(self.frame_2)
        self.trackerToggle.setObjectName(u"trackerToggle")
        self.trackerToggle.setCheckable(True)

        self.gridLayout_7.addWidget(self.trackerToggle, 6, 0, 1, 3)

        self.optTrackerRadio = QRadioButton(self.frame_2)
        self.optTrackerRadio.setObjectName(u"optTrackerRadio")

        self.gridLayout_7.addWidget(self.optTrackerRadio, 1, 1, 1, 2)

        self.styROMField = QLineEdit(self.frame_2)
        self.styROMField.setObjectName(u"styROMField")

        self.gridLayout_7.addWidget(self.styROMField, 3, 1, 1, 1)

        self.label_8 = QLabel(self.frame_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.label_8, 0, 0, 1, 2)

        self.label_9 = QLabel(self.frame_2)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_7.addWidget(self.label_9, 4, 1, 1, 1)

        self.browseStyROM = QToolButton(self.frame_2)
        self.browseStyROM.setObjectName(u"browseStyROM")

        self.gridLayout_7.addWidget(self.browseStyROM, 3, 2, 1, 1)

        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_7.addWidget(self.label_4, 2, 1, 1, 1)

        self.camROMField = QLineEdit(self.frame_2)
        self.camROMField.setObjectName(u"camROMField")

        self.gridLayout_7.addWidget(self.camROMField, 5, 1, 1, 1)

        self.magTrackerRadio = QRadioButton(self.frame_2)
        self.magTrackerRadio.setObjectName(u"magTrackerRadio")

        self.gridLayout_7.addWidget(self.magTrackerRadio, 1, 0, 1, 1)

        self.browseCamROM = QToolButton(self.frame_2)
        self.browseCamROM.setObjectName(u"browseCamROM")

        self.gridLayout_7.addWidget(self.browseCamROM, 5, 2, 1, 1)


        self.verticalLayout.addWidget(self.frame_2)

        self.pivotFrame = QFrame(self.dockWidgetContents)
        self.pivotFrame.setObjectName(u"pivotFrame")
        self.pivotFrame.setFrameShape(QFrame.StyledPanel)
        self.pivotFrame.setFrameShadow(QFrame.Plain)
        self.gridLayout = QGridLayout(self.pivotFrame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(1)
        self.label_3 = QLabel(self.pivotFrame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 4)

        self.browsePivotCalButton = QToolButton(self.pivotFrame)
        self.browsePivotCalButton.setObjectName(u"browsePivotCalButton")

        self.gridLayout.addWidget(self.browsePivotCalButton, 15, 2, 1, 1)

        self.label_20 = QLabel(self.pivotFrame)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout.addWidget(self.label_20, 13, 1, 1, 4)

        self.label_19 = QLabel(self.pivotFrame)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_19, 12, 1, 1, 3)

        self.findPivotCalField = QLineEdit(self.pivotFrame)
        self.findPivotCalField.setObjectName(u"findPivotCalField")

        self.gridLayout.addWidget(self.findPivotCalField, 15, 1, 1, 1)

        self.frame_6 = QFrame(self.pivotFrame)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_6)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setVerticalSpacing(3)
        self.label_5 = QLabel(self.frame_6)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_10.addWidget(self.label_5, 1, 0, 1, 1)

        self.pivotLcd = QLCDNumber(self.frame_6)
        self.pivotLcd.setObjectName(u"pivotLcd")
        self.pivotLcd.setFrameShadow(QFrame.Plain)
        self.pivotLcd.setSegmentStyle(QLCDNumber.Flat)

        self.gridLayout_10.addWidget(self.pivotLcd, 1, 1, 1, 1)

        self.pivotToggle = QPushButton(self.frame_6)
        self.pivotToggle.setObjectName(u"pivotToggle")
        self.pivotToggle.setEnabled(True)
        self.pivotToggle.setCheckable(True)

        self.gridLayout_10.addWidget(self.pivotToggle, 0, 0, 1, 2)


        self.gridLayout.addWidget(self.frame_6, 1, 1, 1, 3)

        self.frame_5 = QFrame(self.pivotFrame)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_5)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setVerticalSpacing(4)
        self.savePivotButton = QPushButton(self.frame_5)
        self.savePivotButton.setObjectName(u"savePivotButton")
        self.savePivotButton.setEnabled(False)

        self.gridLayout_9.addWidget(self.savePivotButton, 0, 1, 1, 1)

        self.applyPivotButton = QPushButton(self.frame_5)
        self.applyPivotButton.setObjectName(u"applyPivotButton")
        self.applyPivotButton.setEnabled(False)

        self.gridLayout_9.addWidget(self.applyPivotButton, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_5, 8, 1, 1, 3)

        self.applyPivotFileButton = QPushButton(self.pivotFrame)
        self.applyPivotFileButton.setObjectName(u"applyPivotFileButton")
        self.applyPivotFileButton.setEnabled(False)

        self.gridLayout.addWidget(self.applyPivotFileButton, 15, 3, 1, 1)


        self.verticalLayout.addWidget(self.pivotFrame)

        self.imgTrackingFrame = QFrame(self.dockWidgetContents)
        self.imgTrackingFrame.setObjectName(u"imgTrackingFrame")
        self.imgTrackingFrame.setFrameShape(QFrame.StyledPanel)
        self.imgTrackingFrame.setFrameShadow(QFrame.Plain)
        self.gridLayout_4 = QGridLayout(self.imgTrackingFrame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setVerticalSpacing(4)
        self.numCapturesBox = QSpinBox(self.imgTrackingFrame)
        self.numCapturesBox.setObjectName(u"numCapturesBox")
        self.numCapturesBox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.numCapturesBox.setMinimum(1)

        self.gridLayout_4.addWidget(self.numCapturesBox, 4, 0, 1, 1)

        self.startImgTrackerButton = QPushButton(self.imgTrackingFrame)
        self.startImgTrackerButton.setObjectName(u"startImgTrackerButton")
        self.startImgTrackerButton.setInputMethodHints(Qt.ImhMultiLine)

        self.gridLayout_4.addWidget(self.startImgTrackerButton, 4, 1, 1, 1)

        self.label_7 = QLabel(self.imgTrackingFrame)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_7, 0, 0, 1, 2)

        self.label_10 = QLabel(self.imgTrackingFrame)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_4.addWidget(self.label_10, 3, 0, 1, 1)


        self.verticalLayout.addWidget(self.imgTrackingFrame)

        self.intFrame = QFrame(self.dockWidgetContents)
        self.intFrame.setObjectName(u"intFrame")
        self.intFrame.setFrameShape(QFrame.StyledPanel)
        self.intFrame.setFrameShadow(QFrame.Plain)
        self.gridLayout_2 = QGridLayout(self.intFrame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(3)
        self.findChessField = QLineEdit(self.intFrame)
        self.findChessField.setObjectName(u"findChessField")

        self.gridLayout_2.addWidget(self.findChessField, 2, 0, 1, 1)

        self.runIntButton = QPushButton(self.intFrame)
        self.runIntButton.setObjectName(u"runIntButton")
        self.runIntButton.setEnabled(True)

        self.gridLayout_2.addWidget(self.runIntButton, 3, 0, 1, 2)

        self.browseChessButton = QToolButton(self.intFrame)
        self.browseChessButton.setObjectName(u"browseChessButton")

        self.gridLayout_2.addWidget(self.browseChessButton, 2, 1, 1, 1)

        self.distCalLabel = QLabel(self.intFrame)
        self.distCalLabel.setObjectName(u"distCalLabel")
        self.distCalLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.distCalLabel, 0, 0, 1, 2)

        self.findChessLabel = QLabel(self.intFrame)
        self.findChessLabel.setObjectName(u"findChessLabel")

        self.gridLayout_2.addWidget(self.findChessLabel, 1, 0, 1, 2)


        self.verticalLayout.addWidget(self.intFrame)

        self.frame_4 = QFrame(self.dockWidgetContents)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Plain)
        self.gridLayout_11 = QGridLayout(self.frame_4)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setVerticalSpacing(4)
        self.browseHETrackingButton = QToolButton(self.frame_4)
        self.browseHETrackingButton.setObjectName(u"browseHETrackingButton")

        self.gridLayout_11.addWidget(self.browseHETrackingButton, 6, 1, 1, 1)

        self.browseIntCalButton = QToolButton(self.frame_4)
        self.browseIntCalButton.setObjectName(u"browseIntCalButton")

        self.gridLayout_11.addWidget(self.browseIntCalButton, 2, 1, 1, 1)

        self.label = QLabel(self.frame_4)
        self.label.setObjectName(u"label")

        self.gridLayout_11.addWidget(self.label, 1, 0, 1, 2)

        self.findHETrackingLabel = QLabel(self.frame_4)
        self.findHETrackingLabel.setObjectName(u"findHETrackingLabel")

        self.gridLayout_11.addWidget(self.findHETrackingLabel, 5, 0, 1, 2)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_11.addWidget(self.label_2, 3, 0, 1, 2)

        self.intCalField = QLineEdit(self.frame_4)
        self.intCalField.setObjectName(u"intCalField")

        self.gridLayout_11.addWidget(self.intCalField, 2, 0, 1, 1)

        self.browseHEImageButton = QToolButton(self.frame_4)
        self.browseHEImageButton.setObjectName(u"browseHEImageButton")

        self.gridLayout_11.addWidget(self.browseHEImageButton, 4, 1, 1, 1)

        self.findHEImageField = QLineEdit(self.frame_4)
        self.findHEImageField.setObjectName(u"findHEImageField")

        self.gridLayout_11.addWidget(self.findHEImageField, 4, 0, 1, 1)

        self.findHETrackingField = QLineEdit(self.frame_4)
        self.findHETrackingField.setObjectName(u"findHETrackingField")

        self.gridLayout_11.addWidget(self.findHETrackingField, 6, 0, 1, 1)

        self.label_21 = QLabel(self.frame_4)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.label_21, 0, 0, 1, 2)

        self.frame_3 = QFrame(self.frame_4)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_3)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setVerticalSpacing(3)
        self.beginHEButton = QPushButton(self.frame_3)
        self.beginHEButton.setObjectName(u"beginHEButton")
        self.beginHEButton.setEnabled(True)

        self.gridLayout_8.addWidget(self.beginHEButton, 0, 0, 1, 1)

        self.saveHEButton = QPushButton(self.frame_3)
        self.saveHEButton.setObjectName(u"saveHEButton")
        self.saveHEButton.setEnabled(False)

        self.gridLayout_8.addWidget(self.saveHEButton, 0, 1, 1, 1)

        self.loadHEButton = QPushButton(self.frame_3)
        self.loadHEButton.setObjectName(u"loadHEButton")

        self.gridLayout_8.addWidget(self.loadHEButton, 1, 0, 1, 1)

        self.testHEToggle = QPushButton(self.frame_3)
        self.testHEToggle.setObjectName(u"testHEToggle")
        self.testHEToggle.setEnabled(False)
        self.testHEToggle.setCheckable(True)

        self.gridLayout_8.addWidget(self.testHEToggle, 1, 1, 1, 1)


        self.gridLayout_11.addWidget(self.frame_3, 7, 0, 1, 2)


        self.verticalLayout.addWidget(self.frame_4)

        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget)
        self.dockWidget.raise_()

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
#if QT_CONFIG(shortcut)
        self.actionExit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+E", None))
#endif // QT_CONFIG(shortcut)
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Camera", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Tx", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Tz", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Ty", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Stylus", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Error", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.imgCaptureButton.setText(QCoreApplication.translate("MainWindow", u"Capture Image", None))
        self.openCamSettingsButton.setText(QCoreApplication.translate("MainWindow", u"Open Camera Settings", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Camera", None))
        self.trackerToggle.setText(QCoreApplication.translate("MainWindow", u"Start/Stop Tracker", None))
        self.optTrackerRadio.setText(QCoreApplication.translate("MainWindow", u"Optical (Polaris)", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Tracking", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Camera ROM File:", None))
        self.browseStyROM.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Stylus ROM File:", None))
        self.magTrackerRadio.setText(QCoreApplication.translate("MainWindow", u"Magnetic (Aurora)", None))
        self.browseCamROM.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Pivot Calibration", None))
        self.browsePivotCalButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Pivot Calibration File (XML):", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"- OR -", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"RMS (mm)", None))
        self.pivotToggle.setText(QCoreApplication.translate("MainWindow", u"Start/Stop Pivot Calibration", None))
        self.savePivotButton.setText(QCoreApplication.translate("MainWindow", u"Save to File", None))
        self.applyPivotButton.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.applyPivotFileButton.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.startImgTrackerButton.setText(QCoreApplication.translate("MainWindow", u"Start Capture Sequence", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Image Capture with Tracking Data", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Number of Captures", None))
        self.runIntButton.setText(QCoreApplication.translate("MainWindow", u"Run Intrinsic Calibration", None))
        self.browseChessButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.distCalLabel.setText(QCoreApplication.translate("MainWindow", u"Intrinsic Calibration", None))
        self.findChessLabel.setText(QCoreApplication.translate("MainWindow", u"Chessboard Image Directory:", None))
        self.browseHETrackingButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.browseIntCalButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Intrinsic Calibration File (XML):", None))
        self.findHETrackingLabel.setText(QCoreApplication.translate("MainWindow", u"Enter Tracking File Name", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Stylus Image Directory:", None))
        self.browseHEImageButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Hand-Eye Calibration", None))
        self.beginHEButton.setText(QCoreApplication.translate("MainWindow", u"Run Hand-Eye Calibration", None))
        self.saveHEButton.setText(QCoreApplication.translate("MainWindow", u"Save Calibration", None))
        self.loadHEButton.setText(QCoreApplication.translate("MainWindow", u"Load Saved Calibration", None))
        self.testHEToggle.setText(QCoreApplication.translate("MainWindow", u"Test Active Calibration", None))
    # retranslateUi

