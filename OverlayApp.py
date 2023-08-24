from sksurgeryutils.common_overlay_apps import OverlayBaseWidget
import cv2
# Defines video feed widget with VTK overlay
class OverlayApp(OverlayBaseWidget):
    def __init__(self, video_source: int, parentViewer):
        super().__init__(video_source)
        self.open_camera_settings()
        self.video_source.source.set(cv2.CAP_PROP_FOCUS, 0)
        #self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)

        self.setFixedWidth(int(self.video_source.source.get(cv2.CAP_PROP_FRAME_WIDTH)))
        self.setFixedHeight(int(self.video_source.source.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.parentViewer = parentViewer

        self.intMat = None
        self.distCoeffs = None
        self.newCamMat = None
    def update_view(self):
        """
        Reads and displays video frames
        """
        _, image = self.video_source.read()
        if self.newCamMat is not None:
            image = cv2.undistort(image, self.intMat, self.distCoeffs, None, self.newCamMat)
        self.vtk_overlay_window.set_video_image(image)
        self.vtk_overlay_window.Render()
        
        # Handles image capture flag and calls capture method
        if self.parentViewer.capture:
            self.parentViewer.capture = False
            self.parentViewer.handleCapture(self.get_output_frame())

    def open_camera_settings(self):
        """Opens camera's own settings software in a new window"""
        self.video_source.source.set(cv2.CAP_PROP_SETTINGS, 1)

    def get_output_frame(self):
        """
        Converts frame to NumPy array and returns it 
        """
        output_frame = self.vtk_overlay_window.convert_scene_to_numpy_array()
        output_frame = cv2.cvtColor(output_frame, cv2.COLOR_RGB2BGR)

        return output_frame
    
    def closeEvent(self, QCloseEvent) -> None:
        """Handles window close"""
        super().closeEvent(QCloseEvent)
        self.stop()

    def set_camera_matrix(self, intMat, distCoeffs):
        """Uses intrinsic matrix and distortion coefficients to undistort frames of video stream"""
        w = self.width()
        h = self.height()
        
        self.intMat = intMat
        self.distCoeffs = distCoeffs
        self.newCamMat, roi = cv2.getOptimalNewCameraMatrix(self.intMat, self.distCoeffs, (w, h), 1, (w, h))