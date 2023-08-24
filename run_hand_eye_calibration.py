# -*- coding: utf-8 -*-

import sys

from PySide6 import QtWidgets
from QVTKViewer import QVTKViewer

ERROR_THRESHOLD = 0.8
NUM_TRACKING_FRAMES = 40
CYLINDER_RADIUS = 1
CYLINDER_HEIGHT = 100
SPHERE_RADIUS = 15

NUM_PORTS = 2
#PORT_REF = 0
PORT_STYLUS = 0
PORT_CAMERA = 1



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QVTKViewer()
    
    window.show()
    window.overlay.show()
    window.overlay.start()
    window.iren.Initialize()
    sys.exit(app.exec()) 