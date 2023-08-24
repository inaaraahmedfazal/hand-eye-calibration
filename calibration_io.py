import csv
import numpy as np
from PySide6 import QtCore

# Readers

def readIntCalFromXml(fname: str):
    qfile = QtCore.QFile(fname)
    intMtx = np.empty((3, 3))
    distCoeffs = np.empty((1, 5))
    if qfile.open(QtCore.QIODevice.ReadOnly):
        reader = QtCore.QXmlStreamReader()
        reader.setDevice(qfile)
        reader.readNextStartElement() # IntrinsicCalibration
        reader.readNextStartElement() # IntrinsicMatrix
        for i in range(3):
            reader.readNextStartElement() # Row
            if str(reader.name()) == "Row":
                for j in range(3):
                    reader.readNextStartElement()
                    if i > 0 and j == 0:
                        reader.readNextStartElement()
                    if str(reader.name()) == "Element":
                        intMtx[i, j] = float(reader.readElementText())
        reader.readNextStartElement() # Row
        reader.readNextStartElement() # IntrinsicMatrix
        reader.readNextStartElement() # DistortionCoefficients
        for i in range(5):
            reader.readNextStartElement() # Coefficient
            if str(reader.name()) == "Coefficient":
                distCoeffs[0, i] = float(reader.readElementText())

    qfile.close()
    return intMtx, distCoeffs

def readTrackingFromXml(fname):
    qfile = QtCore.QFile(fname)
    trackingPositions = []
    trackingRotations = []
    if qfile.open(QtCore.QIODevice.ReadOnly):
        reader = QtCore.QXmlStreamReader()
        reader.setDevice(qfile)
        reader.readNextStartElement() # TrackingCaptures

        while not reader.atEnd():
            if reader.isStartElement():
                if str(reader.name()) == "TrackingCapture":
                    reader.readNextStartElement()
                    if str(reader.name()) == "Position":
                        pt = np.empty((3,))
                        reader.readNextStartElement()
                        if str(reader.name()) == "x":
                            pt[0] = float(reader.readElementText())
                        reader.readNextStartElement()
                        if str(reader.name()) == "y":
                            pt[1] = float(reader.readElementText())
                            reader.readNextStartElement()
                        if str(reader.name()) == "z":
                            pt[2] = float(reader.readElementText())
                        trackingPositions.append(pt)
                    reader.readNextStartElement()
                    reader.readNextStartElement()
                    if str(reader.name()) == "Rotation":
                        rot = np.empty((3,3))
                        for i in range(3):
                            for j in range(3):
                                reader.readNextStartElement()
                                if str(reader.name()) == "MatrixElement":
                                    rot[i, j] = float(reader.readElementText())
                        trackingRotations.append(rot)
                else:
                    reader.readNext()
            else:
                reader.readNext()
    return np.array(trackingPositions), np.array(trackingRotations)

def readTrackingFromTxt(fname):
    trackingPositions = []
    with open(fname) as f:
        for line in f:
            linesplit = line.split(' ')
            trackingPositions.append(np.array([float(linesplit[0]), float(linesplit[1]), float(linesplit[2])]))

    return trackingPositions

def readPivotCalFromXml(fname):
    
    qfile = QtCore.QFile(fname)
    pivotMtx = np.empty((4, 4))
    if qfile.open(QtCore.QIODevice.ReadOnly):
        reader = QtCore.QXmlStreamReader()
        reader.setDevice(qfile)
        reader.readNextStartElement() # PivotCalibrationMatrix
        for i in range(4):
            reader.readNextStartElement() # Row
            if str(reader.name()) == "Row":
                for j in range(4):
                    reader.readNextStartElement()
                    if str(reader.name()) == "Element":
                        pivotMtx[i, j] = float(reader.readElementText())
                    else:
                        reader.readNextStartElement()
                        if str(reader.name()) == "Element":
                            pivotMtx[i, j] = float(reader.readElementText())
    qfile.close()
    return pivotMtx

def readHECalibrationFromXml(fname):
    qfile = QtCore.QFile(fname)
    intMtx = np.empty((3, 3))
    distCoeffs = np.empty((1, 5))
    extMtx = np.empty((4, 4))
    if qfile.open(QtCore.QIODevice.ReadOnly):
        reader = QtCore.QXmlStreamReader()
        reader.setDevice(qfile)
        reader.readNextStartElement() # HandEyeCalibration
        reader.readNextStartElement() # IntrinsicMatrix
        for i in range(3):
            reader.readNextStartElement() # Row
            if str(reader.name()) == "Row":
                for j in range(3):
                    reader.readNextStartElement()
                    if i > 0 and j == 0:
                        reader.readNextStartElement()
                    if str(reader.name()) == "Element":
                        intMtx[i, j] = float(reader.readElementText())
        reader.readNextStartElement() # Row
        reader.readNextStartElement() # IntrinsicMatrix
        reader.readNextStartElement() # DistortionCoefficients
        for i in range(5):
            reader.readNextStartElement() # Coefficient
            if str(reader.name()) == "Coefficient":
                distCoeffs[0, i] = float(reader.readElementText())
        reader.readNextStartElement() # DistortionCoefficients
        reader.readNextStartElement() # ExtrinsicMatrix
        for i in range(4):
            reader.readNextStartElement() # Row
            if str(reader.name()) == "Row":
                for j in range(4):
                    reader.readNextStartElement()
                    if i > 0 and j == 0:
                        reader.readNextStartElement()
                    if str(reader.name()) == "Element":
                        extMtx[i, j] = float(reader.readElementText())
        qfile.close()
        return intMtx, distCoeffs, extMtx

# Writers

def writeErrToCsv(pxErrs, distErrs, angularErrs, output_path):
    fname = f"{output_path}/error_stats.csv"
    n = len(pxErrs)
    with open(fname, 'w', newline='') as csvfile:
        w = csv.writer(csvfile)
        w.writerow(["Frame", "Pixel Error (px)", "Distance Error (mm)", "Angular Error (degrees)"])
        for i in range(n):
            w.writerow([str(i+1), str(pxErrs[i, 0]), str(distErrs[i, 0]), str(angularErrs[i, 0])])
        w.writerow(["Average", str(np.mean(pxErrs)), str(np.mean(distErrs)), str(np.mean(angularErrs))])

def writeTrackingToXml(fname: str, captureList: list):
    qfile = QtCore.QFile(fname)
    qfile.open(QtCore.QIODevice.WriteOnly)
    stream = QtCore.QXmlStreamWriter(qfile)
    stream.writeStartDocument()
    stream.writeStartElement("TrackingCaptures")

    for capture in captureList:
        stream.writeStartElement("TrackingCapture")
        stream.writeStartElement("Position")
        stream.writeTextElement("x", str(capture[0][0]))
        stream.writeTextElement("y", str(capture[0][1]))
        stream.writeTextElement("z", str(capture[0][2]))
        stream.writeEndElement()

        stream.writeStartElement("Rotation")
        for i in range(3):
            for j in range(3):
                stream.writeTextElement("MatrixElement", str(capture[1][i, j]))
        stream.writeEndElement()

        stream.writeEndElement()
    stream.writeEndElement()
    stream.writeEndDocument()

    qfile.close()

def writePivotCalToXml(fname, pivotCalMat):
    qfile = QtCore.QFile(fname)
    qfile.open(QtCore.QIODevice.WriteOnly)
    stream = QtCore.QXmlStreamWriter(qfile)
    stream.writeStartDocument()
    stream.writeStartElement("PivotCalibrationMatrix")
    for row in pivotCalMat:
        stream.writeStartElement("Row")
        for element in row:
            stream.writeTextElement("Element", str(element))
        stream.writeEndElement()
    stream.writeEndElement()
    stream.writeEndDocument()

    qfile.close()

def writeIntCalToXml(fname, intMtx, distCoeffs):
    qfile = QtCore.QFile(fname)
    qfile.open(QtCore.QIODevice.WriteOnly)
    stream = QtCore.QXmlStreamWriter(qfile)
    stream.writeStartDocument()
    stream.writeStartElement("IntrinsicCalibration")

    # intrinsic matrix
    stream.writeStartElement("IntrinsicMatrix")
    for row in intMtx:
        stream.writeStartElement("Row")
        for element in row:
            stream.writeTextElement("Element", str(element))
        stream.writeEndElement()
    stream.writeEndElement()

    # distortion coefficients
    stream.writeStartElement("DistortionCoefficients")
    for coefficient in distCoeffs[0]:
        stream.writeTextElement("Coefficient", str(coefficient))
    stream.writeEndElement()

    stream.writeEndElement()
    stream.writeEndDocument()

    qfile.close()

def writeHECalToXml(fname, intMtx, distCoeffs, extMtx):
    qfile = QtCore.QFile(fname)
    qfile.open(QtCore.QIODevice.WriteOnly)
    stream = QtCore.QXmlStreamWriter(qfile)
    stream.writeStartDocument()
    stream.writeStartElement("HandEyeCalibration")

    # intrinsic matrix
    stream.writeStartElement("IntrinsicMatrix")
    for row in intMtx:
        stream.writeStartElement("Row")
        for element in row:
            stream.writeTextElement("Element", str(element))
        stream.writeEndElement()
    stream.writeEndElement()

    # distortion coefficients
    stream.writeStartElement("DistortionCoefficients")
    for coefficient in distCoeffs[0]:
        stream.writeTextElement("Coefficient", str(coefficient))
    stream.writeEndElement()

    # extrinsic matrix
    stream.writeStartElement("ExtrinsicMatrix")
    for row in extMtx:
        stream.writeStartElement("Row")
        for element in row:
            stream.writeTextElement("Element", str(element))
        stream.writeEndElement()
    stream.writeEndElement()

    stream.writeEndElement()
    stream.writeEndDocument()
    qfile.close()
    