import vtk
import cv2
import os
import Stats

import numpy as np
import calibration_io as cio
import HandEyeCalLogic as he

from PySide6 import QtWidgets, QtCore, QtGui
from vtkMainWindow_ui import Ui_MainWindow
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from sksurgerynditracker.nditracker import NDITracker

from OverlayApp import OverlayApp

SPHERE_RADIUS = 15
NUM_TRACKING_FRAMES = 40
NUM_PORTS = 2
PORT_STYLUS = 0
PORT_CAMERA = 1
ERROR_THRESHOLD = 0.8

class QVTKViewer(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, video_source = 0, parent=None):
        super().__init__()
        self.setupUi(self)
        
        # Video widget setup
        self.overlay = OverlayApp(video_source, self)
        
        self.videoGridLayout.addWidget(self.overlay, 0, 0)

        # Tracker widget setup
        self.ren = vtk.vtkRenderer()
        self.qvtkwin = QVTKRenderWindowInteractor(self.trackerwidget)
        self.qvtkwin.GetRenderWindow().AddRenderer(self.ren)
        self.ren.SetBackground(.1, .2, .4)
        self.iren = self.qvtkwin.GetRenderWindow().GetInteractor()
        self.trackerGridLayout.addWidget(self.qvtkwin, 0, 0)

        # Tracker setup
        self.tracker = None
        self.trackerTimer = QtCore.QTimer()
        self.isTrackerInitialized = False
        self.trackerSettings = {}

        # Tracker widget status graphic setup
        self.logoWidgetX = 16
        self.logoWidgetY = 10
        self.trackerDrawing = vtk.vtkImageCanvasSource2D()
        self.trackerLogoWidget = vtk.vtkLogoWidget()
        self.trackerLogoRepresentation = vtk.vtkLogoRepresentation()

        # Tracked objects
        self.sphereSource = vtk.vtkSphereSource()
        self.sphereActor = vtk.vtkActor()
        self.sphereMapper = vtk.vtkPolyDataMapper()
        self.styTransform = vtk.vtkTransform()
        self.refTransform = vtk.vtkTransform()
        self.tipTransform = vtk.vtkTransform()
        self.camTransform = vtk.vtkTransform()

        # Image/data capture setup
        self.capture = False
        self.captureMsg = QtWidgets.QMessageBox()
        self.styTrackingCaptures = []
        self.camTrackingCaptures = []
        self.singleCaptureButton = self.captureMsg.addButton("Capture", QtWidgets.QMessageBox.ActionRole)
        self.captureSequenceIdx = 0
        self.captureSequenceDir = ""

        # Pivot calibration setup
        self.minimizer = vtk.vtkAmoebaMinimizer()
        self.pivotCalArray = vtk.vtkDoubleArray()
        self.pivotCalArray.SetNumberOfComponents(16)
        self.pivotCalMat = np.empty((4,4))
        self.appliedPivotCal = vtk.vtkTransform()
        self.loadedPivotCal = vtk.vtkTransform()
        self.collectPivotCalData = False
        self.stylusActor = vtk.vtkActor()

        # Visual calibration test object setup
        self.showHETest = False
        self.testSphereSource = vtk.vtkSphereSource()
        self.testSphereActor = vtk.vtkActor()
        self.testTransform = vtk.vtkTransform()
        self.testSphereMapper = vtk.vtkPolyDataMapper()
        self.overlayCamWidth = 0
        self.overlayCamHeight = 0

        # Calibration matrices
        self.extMatHE = np.eye(4)
        self.intMatHE = np.eye(3)
        self.distCoeffs = np.zeros((1, 5))

        # Other setup function calls
        self.setupVtkObjects()
        self.connectSignalsSlots()
        self.setQtDefaults()

    def connectSignalsSlots(self):
        """Connects signals from Qt UI components with slot functions defined in this program"""

        # Browse buttons
        self.browseHEImageButton.clicked.connect(self.browseHEImage)
        self.browseHETrackingButton.clicked.connect(self.browseHETracking)
        self.browseChessButton.clicked.connect(self.browseChess)
        self.browseIntCalButton.clicked.connect(self.browseIntCal)
        self.browseStyROM.clicked.connect(self.browseStyROMClicked)
        self.browseCamROM.clicked.connect(self.browseCamROMClicked)

        # Capture and tracking
        self.imgCaptureButton.clicked.connect(self.captureFrame)
        self.openCamSettingsButton.clicked.connect(self.overlay.open_camera_settings)
        self.startImgTrackerButton.clicked.connect(self.startCaptureSeq)

        # Running procedures
        self.runIntButton.clicked.connect(self.runIntCal)
        self.beginHEButton.clicked.connect(self.runHECal)
        self.testHEToggle.toggled.connect(self.handleTestHEToggle)
        self.saveHEButton.clicked.connect(self.saveHECal)
        self.loadHEButton.clicked.connect(self.loadHECal)
        
        # Pivot calibration
        self.browsePivotCalButton.clicked.connect(self.browsePivotCal)
        self.savePivotButton.clicked.connect(self.savePivotCal)
        self.applyPivotButton.clicked.connect(self.applyPivotCal)
        self.applyPivotFileButton.clicked.connect(self.applyPivotCal)

        # Toggles
        self.trackerToggle.toggled.connect(self.startTracker)
        self.pivotToggle.toggled.connect(self.handlePivotToggle)

    def setupVtkObjects(self):
        """Initializes and connects VTK objects"""
        self.sphereSource.SetCenter(0, 0, 0)
        self.sphereSource.SetRadius(SPHERE_RADIUS)

        # Initialize all transforms to identity
        self.tipTransform.Identity()
        self.appliedPivotCal.Identity()
        self.refTransform.Identity()
        self.styTransform.Identity()
        self.testTransform.Identity()

        # Mapper/actor for tracked sphere
        self.sphereMapper.SetInputConnection(self.sphereSource.GetOutputPort())
        self.sphereActor.SetMapper(self.sphereMapper)

        # Transformation chain to get tip of stylus
        self.tipTransform.PostMultiply()
        self.tipTransform.Concatenate(self.appliedPivotCal)
        self.tipTransform.Concatenate(self.styTransform)
        self.tipTransform.Concatenate(self.camTransform.GetLinearInverse())
        
        # Mapper/actor for visual calibration test sphere
        self.testSphereSource.SetRadius(SPHERE_RADIUS)
        self.testSphereMapper.SetInputConnection(self.testSphereSource.GetOutputPort())
        self.testSphereActor.SetMapper(self.testSphereMapper)
    
    def setQtDefaults(self):
        """Set default file names in fields"""

        # Buttons
        self.optTrackerRadio.setChecked(True)
        self.applyPivotFileButton.setEnabled(True)

        # Default field values
        self.numCapturesBox.setValue(12)

        self.styROMField.setText("GreenStylus.rom")
        self.camROMField.setText("LogitechDRB.rom")
        self.intCalField.setText("intcal.xml")
        self.findHEImageField.setText("sample_calibration_images")
        self.findHETrackingField.setText("sample_calibration_images/stylus_tracking_captures.xml")
        
        self.findPivotCalField.setText("pivotcal.xml")
        fname = self.findPivotCalField.text()
        self.pivotCalMat = cio.readPivotCalFromXml(fname)
        self.loadedPivotCal.SetMatrix(np.reshape(self.pivotCalMat, 16))
    
    def captureFrame(self):
        """ Sets capture flag to true so it can be handled by overlay widget class"""
        self.capture = True

    def browseStyROMClicked(self):
        """ Browsing window for stylus ROM file (optical tracking) """
        fname, d = QtWidgets.QFileDialog.getOpenFileName()
        self.styROMField.setText(fname)

    def browseCamROMClicked(self):
        """ Browsing window for camera ROM file (optical tracking) """
        fname, d = QtWidgets.QFileDialog.getOpenFileName()
        self.camROMField.setText(fname)
    
    def browseChess(self):
        """ Browsing window for chessboard image directory (intrinsic calibration)"""
        dir = QtWidgets.QFileDialog.getExistingDirectory()
        self.findChessField.setText(dir)

    def browsePivotCal(self):
        """ Browsing window for pivot calibration stored in XML file """
        fname, d = QtWidgets.QFileDialog.getOpenFileName()
        self.findPivotCalField.setText(fname)
        self.pivotCalMat = cio.readPivotCalFromXml(fname)
        self.loadedPivotCal.SetMatrix(np.reshape(self.pivotCalMat, 16))
        self.applyPivotFileButton.setEnabled(True)

    def browseHEImage(self):
        """ Browsing window for hand-eye calibration image directory """
        dir = QtWidgets.QFileDialog.getExistingDirectory()
        self.findHEImageField.setText(dir)

    def browseHETracking(self):
        """ Browsing window for hand-eye calibration tracking file """
        fname, d = QtWidgets.QFileDialog.getOpenFileName()
        self.findHETrackingField.setText(fname)

    def browseIntCal(self):
        """ Browsing window for intrinsic calibration stored in XML file """
        fname, d = QtWidgets.QFileDialog.getOpenFileName()
        self.intCalField.setText(fname)
        intmat, distcoeffs = cio.readIntCalFromXml(fname)

    def handleCapture(self, frame):
        """ Receives screenshot as NumPy array and writes it to specified directory"""
        if self.captureSequenceIdx > 0:
            fname = f"{self.captureSequenceDir}/capture_{self.captureSequenceIdx}.png"
        else:
            fname, d = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", QtCore.QDir.currentPath(), "PNG (*.png)")
        cv2.imwrite(fname, frame)

    def startCaptureSeq(self):
        """ Starts sequence of capturing simultaneous image and tracking data """
        numCaptures = self.numCapturesBox.value()
        self.captureSequenceDir = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose Capture Output Directory")
        for i in range(numCaptures):
            self.captureMsg.setText(f"Image and Tracking Data Capture #{i+1}\nPress Capture button when ready")
            self.singleCaptureButton.disconnect(None, None, None)
            self.singleCaptureButton.clicked.connect(lambda: self.singleCapture(i))
            self.captureMsg.exec()
        cio.writeTrackingToXml(f"{self.captureSequenceDir}/stylus_tracking_captures.xml", self.styTrackingCaptures)
        cio.writeTrackingToXml(f"{self.captureSequenceDir}/camera_tracking_captures.xml", self.camTrackingCaptures)
        self.captureSequenceIdx = 0

    def singleCapture(self, i):
        """Captures one image screenshot with corresponding tracking data"""
        self.captureSequenceIdx = i + 1

        # Screenshot
        self.captureFrame()

        progressDialog = QtWidgets.QProgressDialog("Collecting...", "Cancel", 0, NUM_TRACKING_FRAMES, self)
        progressDialog.setMinimumDuration(0)
        progressDialog.setWindowModality(QtCore.Qt.WindowModal)
        sty_pts = []
        sty_rotations = []
        cam_pts = []
        cam_rotations = []

        # Collects positional and rotational tracking data for camera and stylus over NUM_TRACKING_FRAMES
        for j in range(NUM_TRACKING_FRAMES):
            progressDialog.setValue(j)
            styPos = self.tipTransform.GetPosition()
            camPos = self.camTransform.GetPosition()
            if not np.isnan(np.sum(styPos)) and not np.isnan(np.sum(camPos)):
                sty_pts.append(styPos)
                cam_pts.append(camPos)
                styRotMat = self.tipTransform.GetMatrix()
                camRotMat = self.camTransform.GetMatrix()
                styRot = np.empty((9))
                camRot = np.empty((9))
                for k in range(3):
                   for l in range(3):
                       styRot[int(k*l+l)] = styRotMat.GetElement(k, l)
                       camRot[int(k*l+l)] = camRotMat.GetElement(k, l)
                sty_rotations.append(styRot)
                cam_rotations.append(camRot)
        progressDialog.setValue(NUM_TRACKING_FRAMES)
        sty_rotations = np.array(sty_rotations)
        cam_rotations = np.array(cam_rotations)

        # Averages 3D positional tracking data across NUM_TRACKING_FRAMES
        sty_avgPos = Stats.robustAverage3D(np.array(sty_pts))
        cam_avgPos = Stats.robustAverage3D(np.array(cam_pts))

        # Averages rotational tracking data across NUM_TRACKING_FRAMES
        sty_avgRot = np.empty((3, 3))
        cam_avgRot = np.empty((3, 3))
        for j in range(3):
            for k in range(3):
                sty_avgRot[j, k] = Stats.robustAverage1D(np.array(sty_rotations[:, int(k*j+k)]))
                cam_avgRot[j, k] = Stats.robustAverage1D(np.array(cam_rotations[:, int(k*j+k)]))

        # Adds stylus and camera tracking data to respective files
        self.styTrackingCaptures.append([sty_avgPos, sty_avgRot])
        self.camTrackingCaptures.append([cam_avgPos, cam_avgRot])
        self.captureMsg.accept()

    def startTracker(self):
        """ Starts NDI Aurora (magnetic) or Polaris (optical) tracker and sets up VTK tracked objects"""

        # Toggle ON
        if self.trackerToggle.isChecked():
            if not self.isTrackerInitialized:
                try:
                    if self.magTrackerRadio.isChecked():
                        self.trackerSettings = {
                            "tracker type": "aurora",
                            "ports to probe": NUM_PORTS,
                            "verbose": True
                        }
                    elif self.optTrackerRadio.isChecked():
                        self.trackerSettings = {
                            "tracker type": "polaris",
                            "romfiles": [self.styROMField.text(), self.camROMField.text()]
                        }
                    self.tracker = NDITracker(self.trackerSettings)
                    self.isTrackerInitialized = True
                    self.tracker.use_quaternions = False

                    self.sphereActor.SetUserTransform(self.tipTransform)
                    self.trackerTimer.timeout.connect(self.updateTrackerInfo)
                except:
                    print("Unable to connect to NDI Tracker device")
                    self.isTrackerInitialized = False
                    self.trackerToggle.setChecked(False)

            if self.isTrackerInitialized:
                self.tracker.start_tracking()
                self.trackerTimer.start(0)
                self.createTrackerLogo()
                self.trackerLogoWidget.On()
                self.ren.AddActor(self.sphereActor)
                self.qvtkwin.GetRenderWindow().Render()

        # Toggle OFF
        else:
            if self.isTrackerInitialized:
                self.trackerTimer.stop()
                self.tracker.stop_tracking()
                self.trackerLogoWidget.Off()
                self.ren.RemoveActor(self.sphereActor)
                self.ren.RemoveActor(self.stylusActor)
                self.qvtkwin.GetRenderWindow().Render()
                print("Tracking Stopped")

    def updateTrackerInfo(self):
        """
        Updates VTK objects, error display, and volume display with new tracking information (called as often as possible)
        """
        if self.isTrackerInitialized:
            port_handles, time_stamps, frame_numbers, tracking, tracking_quality = self.tracker.get_frame()

            sty_mat = tracking[PORT_STYLUS]
            sty_mat_16 = np.reshape(sty_mat, 16)

            cam_mat = tracking[PORT_CAMERA]
            cam_mat_16 = np.reshape(cam_mat, 16)

            if self.collectPivotCalData and not np.isnan(np.sum(sty_mat_16) + np.sum(cam_mat_16)):
                self.pivotCalArray.InsertNextTuple(sty_mat_16)
            
            self.styTransform.SetMatrix(sty_mat_16)
            self.camTransform.SetMatrix(cam_mat_16)

            self.tipTransform.Update()

            # if testing HE calibration, update transform of overlayed sphere
            if self.showHETest:

                tipMat = self.tipTransform.GetMatrix()
                pt = np.ones((4, 1))
                pt[0, 0] = tipMat.GetElement(0, 3)
                pt[1, 0] = tipMat.GetElement(1, 3)
                pt[2, 0] = tipMat.GetElement(2, 3)
                camPt = np.linalg.inv(self.extMatHE) @ pt

                self.testTransform.Update()
                
                m = self.testSphereActor.GetUserTransform().GetMatrix()
                mx = m.GetElement(0, 3) 
                my = m.GetElement(1, 3)
                mz = m.GetElement(2, 3)

                self.overlay.vtk_overlay_window.foreground_renderer.ResetCameraClippingRange()
                self.overlay.vtk_overlay_window.GetRenderWindow().Render()


            self.updateVolumeDisplay(tracking)
            self.updateTrackingPositions()
            self.updateErrorDisplay(tracking_quality)

            self.ren.ResetCameraClippingRange()
            self.qvtkwin.GetRenderWindow().Render()

    def createTrackerLogo(self):
        """Initializes rectangular icons showing tracked tool status (red = not tracking, green = tracking)"""

        n = NUM_PORTS
        self.trackerDrawing.SetScalarTypeToUnsignedChar()
        self.trackerDrawing.SetNumberOfScalarComponents(3)
        self.trackerDrawing.SetExtent(0, self.logoWidgetX*n + n, 0, self.logoWidgetY + 2, 0, 0)
        self.trackerDrawing.SetDrawColor(255, 255, 255)
        self.trackerDrawing.FillBox(0, self.logoWidgetX*n + n, 0, self.logoWidgetY + 2)

        self.trackerDrawing.Update()
        self.trackerLogoRepresentation.SetImage(self.trackerDrawing.GetOutput())
        self.trackerLogoRepresentation.SetPosition(0.45, 0)
        self.trackerLogoRepresentation.SetPosition2(0.1, 0.1)
        self.trackerLogoRepresentation.GetImageProperty().SetOpacity(0.5)
        
        self.trackerLogoWidget.SetRepresentation(self.trackerLogoRepresentation)
        self.trackerLogoWidget.SetInteractor(self.iren)

    def updateVolumeDisplay(self, tracking):
        """Updates rectangular icons showing tracked tool status (red = not tracking, green = tracking)"""
        for i, trackingInfo in enumerate(tracking):
            if np.isnan(np.sum(trackingInfo)):
                self.trackerDrawing.SetDrawColor(255, 0, 0)
                self.trackerDrawing.FillBox(self.logoWidgetX*i + i + 1, self.logoWidgetX*(i + 1) + i, 1, self.logoWidgetY + 1)
            else:
                self.trackerDrawing.SetDrawColor(0, 255, 0)
                self.trackerDrawing.FillBox(self.logoWidgetX*i + i + 1, self.logoWidgetX*(i + 1) + i, 1, self.logoWidgetY + 1)
                
        self.trackerDrawing.Update()

    def updateErrorDisplay(self, tracking_quality):
        """Updates error LCD such that background is green for values below ERROR_THRESHOLD and red otherwise"""
        styErr = tracking_quality[PORT_STYLUS]
        camErr = tracking_quality[PORT_CAMERA]

        camPalette = self.camErr.palette()
        if camErr < ERROR_THRESHOLD:
            camPalette.setColor(self.camErr.backgroundRole(), QtGui.QColor(QtCore.Qt.GlobalColor.green))
        else:
            camPalette.setColor(self.camErr.backgroundRole(), QtGui.QColor(QtCore.Qt.GlobalColor.red))
            
        styPalette = self.styErr.palette()
        if styErr < ERROR_THRESHOLD:
            styPalette.setColor(self.styErr.backgroundRole(), QtGui.QColor(QtCore.Qt.GlobalColor.green))
        else:
            styPalette.setColor(self.styErr.backgroundRole(), QtGui.QColor(QtCore.Qt.GlobalColor.red))
            
        self.camErr.setPalette(camPalette)
        self.styErr.setPalette(styPalette)
        self.camErr.display(camErr)
        self.styErr.display(styErr)
    
    def updateTrackingPositions(self):
        """Updates LCDs with x, y, z coordinates of both tools from tracker"""
        camPos = self.camTransform.GetPosition()
        self.camTx.display(camPos[0])
        self.camTy.display(camPos[1])
        self.camTz.display(camPos[2])

        styPos = self.tipTransform.GetPosition()
        self.styTx.display(styPos[0])
        self.styTy.display(styPos[1])
        self.styTz.display(styPos[2])

    def minimizerFunc(self):
        """Runs AmoebaMinimizer on pivot calibration tracking data"""
        n = self.pivotCalArray.GetNumberOfTuples()
        x = self.minimizer.GetParameterValue("x")
        y = self.minimizer.GetParameterValue("y")
        z = self.minimizer.GetParameterValue("z")

        #mat = np.empty((4, 4))
        sx = sy = sz = 0.0
        sxx = syy = szz = 0.0

        for i in range(n):
            mat = self.pivotCalArray.GetTuple(i)
            mat = np.reshape(mat, (4,4))
            nx = mat[0,0]*x + mat[0,1]*y + mat[0,2]*z + mat[0,3]
            ny = mat[1,0]*x + mat[1,1]*y + mat[1,2]*z + mat[1,3]
            nz = mat[2,0]*x + mat[2,1]*y + mat[2,2]*z + mat[2,3]

            sx += nx
            sy += ny
            sz += nz

            sxx += nx*nx
            syy += ny*ny
            szz += nz*nz

        if n > 1:
            r = np.sqrt((sxx - sx*sx/n)/(n - 1) + (syy - sy*sy/n)/(n - 1) + (szz - sz*sz/n)/(n - 1))
        else:
            r = 0.0

        self.minimizer.SetFunctionValue(r)
    
    def doPivotCal(self):
        """Sets parameters and calls minimizer function for pivot calibration"""
        self.pivotCalMat = np.eye(4)
        
        self.minimizer.SetFunction(self.minimizerFunc)

        self.minimizer.SetParameterValue("x", 0)
        self.minimizer.SetParameterScale("x", 1000)

        self.minimizer.SetParameterValue("y", 0)
        self.minimizer.SetParameterScale("y", 1000)

        self.minimizer.SetParameterValue("z", 0)
        self.minimizer.SetParameterScale("z", 1000)

        self.minimizer.Minimize()
        minimum = self.minimizer.GetFunctionValue()

        self.pivotCalMat[0, 3] = self.minimizer.GetParameterValue("x")
        self.pivotCalMat[1, 3] = self.minimizer.GetParameterValue("y")
        self.pivotCalMat[2, 3] = self.minimizer.GetParameterValue("z")

        self.pivotLcd.display(minimum)
        self.loadedPivotCal.SetMatrix(np.reshape(self.pivotCalMat, 16))

    def applyPivotCal(self):
        """Applies pivot calibration (live or from file) to VTK sphere, creates VTK stylus object"""
        self.appliedPivotCal.SetMatrix(self.loadedPivotCal.GetMatrix())
        self.createStylusActor(2)

    def handlePivotToggle(self):
        """Handles toggle for pivot calibration data collection"""
        if self.isTrackerInitialized:
            if self.pivotToggle.isChecked():
                self.pivotCalArray.Initialize()
                self.pivotCalArray.SetNumberOfTuples(0)
                self.collectPivotCalData = True
                self.savePivotButton.setEnabled(False)
                self.applyPivotButton.setEnabled(False)
            else:
                self.collectPivotCalData = False
                self.doPivotCal()
                self.savePivotButton.setEnabled(True)
                self.applyPivotButton.setEnabled(True)
        else:
            self.pivotToggle.setChecked(False)
    
    def savePivotCal(self):
        """Writes pivot calibration matrix to XML file"""
        fname, d = QtWidgets.QFileDialog.getSaveFileName(self, "Save XML File", QtCore.QDir.currentPath(), "XML Files (*.xml)")
        cio.writePivotCalToXml(fname, self.loadedPivotCal)

    def createStylusActor(self, dim):
        """Creates VTK object representation of stylus (after pivot calibration)"""
        pos = np.array([0, 0, 0, 1])
        pos[dim] = -1.0
        outpos = np.matmul(self.pivotCalMat, pos)
        pos = outpos/np.linalg.norm(outpos)

        append = vtk.vtkAppendPolyData()
        coneHeight = 25.0
        needleHeight = 150.0
        radius = 1.5
        nSides = 36
        
        line = vtk.vtkLineSource()
        line.SetPoint1(pos[0], pos[1], pos[2])
        line.SetPoint2(outpos[0], outpos[1], outpos[2])

        tube = vtk.vtkTubeFilter()
        tube.SetInputConnection(line.GetOutputPort())
        tube.SetRadius(radius)
        tube.SetNumberOfSides(nSides)

        cone = vtk.vtkConeSource()
        cone.SetHeight(coneHeight)
        cone.SetRadius(radius)
        cone.SetDirection(-pos[0], -pos[1], -pos[2])
        cone.SetResolution(nSides)
        cone.SetCenter(0.5*coneHeight*pos[0], 0.5*coneHeight*pos[1], 0.5*coneHeight*pos[2])

        append.AddInputConnection(tube.GetOutputPort())
        append.AddInputConnection(cone.GetOutputPort())

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(append.GetOutputPort())
        self.stylusActor.SetMapper(mapper)
        self.stylusActor.SetUserTransform(self.tipTransform)

        self.ren.AddActor(self.stylusActor)

    def runIntCal(self):
        """Runs intrinsic calibration on a set of chessboard images using OpenCV"""
        dir_str = self.findChessField.text()
        if len(dir_str) == 0:
            err = QtWidgets.QErrorMessage()
            err.showMessage('Folder holding calibration chessboard images must be provided!')
        else:
            dir = os.fsencode(dir_str)
            chessboardFiles = []
            for file in os.listdir(dir):
                fname = os.fsdecode(file)
                chessboardFiles.append(f"{dir_str}/{fname}")

            intMat, distCoeffs = he.distortionCalibration(chessboardFiles)
            print(distCoeffs)
            fname, d = QtWidgets.QFileDialog.getSaveFileName(self, "Save XML File", QtCore.QDir.currentPath(), "XML Files (*.xml)")
            cio.writeIntCalToXml(fname, intMat, distCoeffs)

            self.overlay.set_camera_matrix(intMat, distCoeffs)
    
    def saveHECal(self):
        """Writes intrinsic matrix, distortion coefficients, and extrinsic matrix to XML file"""
        fname, d = QtWidgets.QFileDialog.getSaveFileName(self, "Save XML File", QtCore.QDir.currentPath(), "XML Files (*.xml)")
        cio.writeHECalToXml(fname, self.intMatHE, self.distCoeffs, self.extMatHE)
    
    def runHECal(self):
        """Runs hand-eye calibration based on point-to-line registration"""

        # Collects captured images from given folder
        frames_dir_str = self.findHEImageField.text()
        frames_dir = os.fsencode(frames_dir_str)
        imageFiles = []
        file_ctr = 0
        for file in os.listdir(frames_dir):
            file_str = os.fsdecode(file)
            if file_str.endswith('.png'):
                file_ctr += 1
                imageFiles.append(f"{frames_dir_str}/capture_{file_ctr}.png")

        # Reads tracking data corresponding to calibration images
        fname = self.findHETrackingField.text()
        trackingPositions, trackingRotations = cio.readTrackingFromXml(fname)

        # Reads intrinsic calibration
        intCalFile = self.intCalField.text()
        intMat, distCoeffs = cio.readIntCalFromXml(intCalFile)
        
        # Calls registration to get extrinsic matrix, reprojection coordinates, and error values
        extMat, px, pxErrs, distErrs, angularErrs = he.analyzeFrames(imageFiles, trackingPositions, intMat, distCoeffs)

        print("\n")
        print("Pixels")
        print(px)
        
        print("\n")
        print("Pixel error")
        print(pxErrs)
        print(f"Average pixel error: {np.sum(pxErrs)/len(pxErrs)} px")

        print("\n")
        print("Distance error")
        print(distErrs)
        print(f"Average distance error: {np.sum(distErrs)/len(distErrs)} mm")

        print("\n")
        print("Angular error")
        print(angularErrs)
        print(f"Average angular error: {np.sum(angularErrs)/len(angularErrs)} deg")

        # Displays and saves images with centroid reprojection
        output_path = f"{frames_dir_str}/output"
        os.mkdir(output_path)
        for i in range(len(px)):
            try:
                img = cv2.imread(f"{frames_dir_str}/capture_{i+1}.png")
                h, w = img.shape[:2]
                newCamMat, roi = cv2.getOptimalNewCameraMatrix(intMat, distCoeffs, (w, h), 1, (w, h))
                img = cv2.undistort(img, intMat, distCoeffs, None, newCamMat)
                if px[i][0, 0] != -1:
                    pxx = np.uint16(np.round(px[i][0, 0]))
                    pxy = np.uint16(np.round(px[i][1, 0]))
                    cv2.circle(img, (pxx, pxy), 1, (0, 255, 255), 2)
                    cv2.imshow("pixel error image", img)
                    cv2.waitKey(0)
                    cv2.imwrite(f"{output_path}/reprojection_{i+1}.png", img)
            except:
                print("could not draw pixel onto image")

        # Writes error values to CSV file
        cio.writeErrToCsv(pxErrs, distErrs, angularErrs, output_path)

        self.extMatHE = extMat
        self.intMatHE = intMat
        self.distCoeffs = distCoeffs

        self.overlay.set_camera_matrix(self.intMatHE, self.distCoeffs)

        self.testHEToggle.setEnabled(True)
        self.saveHEButton.setEnabled(True)
        cv2.destroyAllWindows()

    def loadHECal(self):
        """Loads hand-eye calibration (intrinsic matrix, distortion coefficients, and extrinsic matrix) from XML file"""
        fname, d = QtWidgets.QFileDialog.getOpenFileName()
        intMat, distCoeffs, extMat = cio.readHECalibrationFromXml(fname)
        self.intMatHE = intMat
        self.extMatHE = extMat
        self.distCoeffs = distCoeffs
        self.overlay.set_camera_matrix(self.intMatHE, self.distCoeffs)
        print("int mat", self.intMatHE)
        print("dist coeffs", self.distCoeffs)
        print("ext mat", self.extMatHE)
        self.testHEToggle.setEnabled(True)

    def handleTestHEToggle(self):
        """Handles toggle of AR overlay"""
        if self.testHEToggle.isChecked():
            # create overlay object
            self.showHETest = True
            
            w = self.overlay.width()
            h = self.overlay.height()
            print("width:", w)
            print("height:", h)

            extMatVTK = vtk.vtkTransform()
            extMatVTK.SetMatrix(np.reshape(self.extMatHE, 16))
            self.testTransform.PostMultiply()
            self.testTransform.Identity()
            self.testTransform.Concatenate(self.tipTransform)
            self.testTransform.Concatenate(extMatVTK)
            self.testSphereActor.SetUserTransform(self.testTransform)
            self.overlay.vtk_overlay_window.add_vtk_actor(self.testSphereActor)
            # set up vtk overlay camera
            vtkcam = self.overlay.vtk_overlay_window.foreground_renderer.GetActiveCamera()
            
            vtkcam.SetParallelProjection(False)
            vtkcam.SetPosition(0, 0, 0)
            vtkcam.SetFocalPoint(0, 0, 1)
            vtkcam.SetViewUp(0, -1, 0)

            cx = self.intMatHE[0, 2]
            cy = self.intMatHE[1, 2]
            fx = self.intMatHE[0, 0]
            print("cx:", cx)
            print("cy:", cy)
            wcx = -2 * (cx - float(w) / 2) / w
            wcy = 2 * (cy - float(h) / 2) / h
            vtkcam.SetWindowCenter(wcx, wcy)
            print("wcx:", wcx)
            print("wcy:", wcy)

            view_angle = 180 / np.pi * (2.0 * np.arctan2(h / 2.0, fx))
            print("view angle:", view_angle)
            vtkcam.SetViewAngle(view_angle)

        else:
            self.showHETest = False
            self.overlay.vtk_overlay_window.get_foreground_renderer().RemoveActor(self.testSphereActor)


    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        super().closeEvent(event)
        self.qvtkwin.close()
        self.qvtkwin.Finalize()
        self.overlay.close()
