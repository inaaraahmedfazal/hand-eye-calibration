import numpy as np
import cv2

def hand_eye_p2l(X, Q, A, tol=0.001):
    """
    Based on: https://github.com/TaraKemper/VideoBasedHandEye/blob/main/HandEyeCalibration.py
    Arguments:  X (3xn):    3D coordinates, tracker space
                Q (2xn):    2D pixel locations, image space
                A (3x3):    camera matrix

    Returns:    R (3x3):    orthonormal rotation matrix
                t (3x1):    translation
    """
    n = Q.shape[1]
    e = np.ones(n)
    J = np.identity(n) - (np.divide((np.transpose(e) * e), n))
    Q = np.linalg.inv(A) @ np.vstack((Q, e))
    Y = ([[], [], []])

    # Normalizing the 2D pixel coordinates
    for i in range(n):
        x = Q[:, i]
        y = np.linalg.norm(x)
        z = x / y
        z = np.reshape(z, (3, 1))
        Y = np.hstack((Y, z))

    Q = Y
    err = np.inf
    E_old = 1000 * np.ones((3, n))

    while err > tol:
        a = Y @ J @ X.T.conj()
        U, S, V, = np.linalg.svd(a)

        # Get rotation
        R = U @ np.array([[1, 0, 0], [0, 1, 0], [0, 0, np.linalg.det(U @ V)]]) @ V 

        # Get translation
        T = Y - R @ X
        t = ([])
        for i in range(np.shape(Y)[0]): # could use n?
            t = np.append(t, np.mean(T[i]))
        t = np.reshape(t, (np.shape(Y)[0], 1))

        # Reprojection
        h = R @ X + t * e
        H = ([])
        for i in range(np.shape(Q)[1]):
            H = np.append(H, np.dot(h[:, i], Q[:, i]))
        Y = np.matlib.repmat(H, 3, 1) * Q

        # Get reprojection error
        E = Y - R @ X - t * e
        err = np.linalg.norm(E - E_old, 'fro')
        E_old = E
    
    return R, t
def analyzeFrames(frames, transforms, intMtx, distCoeffs):
    """
    Based on: https://github.com/TaraKemper/VideoBasedHandEye/blob/main/HandEyeCalibration.py
    Arguments:  frames (list[str]):                 list of stylus image file names
                transforms (np.ndarray, nx3):       array of tracking position data
                intMtx (np.ndarray, 3x3):           camera intrinsic matrix
                distCoeffs (np.ndarray, 1x5):       camera distortion coefficients

    Returns:    calibration (np.ndarray, 4x4):      extrinsic calibration matrix
                px (np.ndarray, 2xn)                reprojected pixels (i.e. from 3D points)
                pxErrs (np.ndarray, n,):            pixel reprojection error
                distErrs (np.ndarray, n,):          distance error
                angularErrs (np.ndarray, n,):       angular error
    
    """
    # Lists for 3D data
    StylusTipCoordsX = ([])
    StylusTipCoordsY = ([])
    StylusTipCoordsZ = ([])

    # Lists for 2D data
    CircleCentersX = ([])
    CircleCentersY = ([])

    StylusTipColour = "green"
    # Detect circle center in each frame (2D point)
    numFrames = len(frames)
    for count in range(numFrames):
        img = cv2.imread(frames[count])

        # Undistort
        h, w = img.shape[:2]
        newCameraMtx, roi = cv2.getOptimalNewCameraMatrix(intMtx, distCoeffs, (w, h), 1, (w, h))
        img = cv2.undistort(img, intMtx, distCoeffs, None, newCameraMtx)

        if StylusTipColour == "green":

            # Colour threshold for green
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, (30, 50, 0), (80, 255, 255))
            target = cv2.bitwise_and(img, img, mask=mask)
            # Apply binary mask
            gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
            th, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

            # Smooth
            blurred = cv2.medianBlur(binary, 25)

        else:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blurred = cv2.medianBlur(gray, 25)

        blurred = cv2.blur(blurred, (10, 10))

        # Use Hough to find circles
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 0.1, 1000, param1=50, param2=30, minRadius=0, maxRadius=50)

        c = transforms[count]
        x = c[0]
        y = c[1]
        z = c[2]

        # Draw calculated circle onto image
        if circles is None:
            # If Hough transform detects no circles, allow user to manually segment circle
            print(f"No circles detected in frame {count}. Try manual circle segmentation")
            def click_event(event, cx, cy, flags, params):
                if event == cv2.EVENT_LBUTTONDOWN:
                    cv2.circle(img, (cx, cy), 1, (0, 255, 255), -1)
                    pts.append([cx, cy])

            pts = []

            cv2.namedWindow("Segment Image")

            cv2.setMouseCallback("Segment Image", click_event)

            while True:
                cv2.imshow("Segment Image", img)
                k = cv2.waitKey(1) & 0xFF
                if k == 27:
                    break
            cv2.destroyAllWindows()
            circle = cv2.minEnclosingCircle(np.array(pts))
            circle_x_int = np.uint16(np.around(circle[0][0]))
            circle_y_int = np.uint16(np.around(circle[0][1]))
            circle_r_int = np.uint16(np.around(circle[1]))

            # Draw resultant circle on image
            cv2.circle(img, (circle_x_int, circle_y_int), 1, (0, 100, 100), 3)
            cv2.circle(img, (circle_x_int, circle_y_int), circle_r_int, (255, 0, 255), 3)
            cv2.imshow("circle overlay", img)
            cv2.waitKey(0)
            CircleCentersX = np.append(CircleCentersX, circle[0][0])
            CircleCentersY = np.append(CircleCentersY, circle[0][1])
            
            # Add corresponding transforms to list
            StylusTipCoordsX = np.append(StylusTipCoordsX, x)
            StylusTipCoordsY = np.append(StylusTipCoordsY, y)
            StylusTipCoordsZ = np.append(StylusTipCoordsZ, z)

        else:
            # Convert circle parameters (as detected by Hough transform) a, b, r to ints
            circles_asint = np.uint16(np.around(circles))
            for i in circles_asint[0, :]:
                center_asint = (i[0], i[1])
                cv2.circle(img, center_asint, 1, (0, 100, 100), 3)
                radius = i[2]
                cv2.circle(img, center_asint, radius, (255, 0, 255), 3)
            cv2.imshow("circle overlay", img)
            cv2.waitKey(0)

            for i in circles[0, :]:
                center = (i[0], i[1])

            if len(StylusTipCoordsX) > 0 and StylusTipCoordsX[-1] == x:
                # Repeated 3D coordinate indicates that tracking is lost
                print(f"Spatial tracking lost in frame {count}")
            else:
                # Add circle centers to list
                CircleCentersX = np.append(CircleCentersX, center[0])
                CircleCentersY = np.append(CircleCentersY, center[1])

                # Add corresponding transforms to list
                StylusTipCoordsX = np.append(StylusTipCoordsX, x)
                StylusTipCoordsY = np.append(StylusTipCoordsY, y)
                StylusTipCoordsZ = np.append(StylusTipCoordsZ, z)

    StylusTipCoords = np.vstack((StylusTipCoordsX, StylusTipCoordsY, StylusTipCoordsZ))
    CircleCenters = np.vstack((CircleCentersX, CircleCentersY))

    # Run calibration procedure
    R, t = hand_eye_p2l(StylusTipCoords, CircleCenters, newCameraMtx)
    calibration = np.vstack((np.hstack((R, t)), [0, 0, 0, 1]))
    print("Extrinsic Matrix:", calibration)

    # Validation
    px, pxErrs = PixelValidation(calibration, StylusTipCoords, CircleCenters, intMtx)
    distErrs = DistanceValidation(calibration, StylusTipCoords, CircleCenters, intMtx)
    angularErrs = AngularValidation(calibration, StylusTipCoords, CircleCenters, intMtx)

    return calibration, px, pxErrs, distErrs, angularErrs

def distortionCalibration(chessboardFiles):
    """
    Runs intrinsic calibration on a set of chessboard image files

    Arguments:  chessboardFiles (list [str]):   list of chessboard image file names

    Returns:    intMtx (np.ndarray, 3x3):       camera intrinsic matrix
                distCoeffs (np.ndarray, 1x5):   camera distortion coefficients
    """
    # Termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((9 * 6, 3), np.float32)
    objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)*23

    # Arrays to store object and image points from images
    objPts = [] # 3D points (world space)
    imgPts = [] # 2D points (image plane)
    
    n = len(chessboardFiles)
    for count in range(n):
        fpath = chessboardFiles[count]
        img = cv2.imread(fpath)

        #img = img[0,::-1,::-1,:] # may be unnecessary with sksurg preprocessing (compared to slicer)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Find checkerboard corners
        ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)
        # If found, refine and add image and object points
        if ret:
            objPts.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgPts.append(corners)

            # Draw corners
            cornersdrawn = cv2.drawChessboardCorners(img, (9, 6), corners2, ret)
            
            # cv2.imshow(fpath[-13:], cornersdrawn)
            # cv2.waitKey(0)
            # Save drawn image if necessary?
    shp = gray.shape[::-1]

    ret, intMtx, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(objPts, imgPts, gray.shape[::-1], None, None)
    print("distortion coefficients:", distCoeffs)
    for count in range(n):
        img = cv2.imread(chessboardFiles[count])
        #img = img[0,::-1,::-1,:] # may be unnecessary with sksurg preprocessing (compared to slicer)
        
        # Undistort
        h, w = img.shape[:2]
        newCameraMtx, roi = cv2.getOptimalNewCameraMatrix(intMtx, distCoeffs, (w, h), 1, (w, h))
        img = cv2.undistort(img, intMtx, distCoeffs, None, newCameraMtx)
        # Save raw undistorted image if necessary?

    # Add the obtained intrinsic matrix and distortion coefficients to the UI
    print("intMtx:", intMtx)
    print("distCoeffs:", distCoeffs)
    return intMtx, distCoeffs

def PixelValidation(extMtx, pts3D, pts2D, intMtx):
    """
    Validates hand-eye calibration by finding pixel error

    Arguments:  extMtx (4x4):   extrinsic calibration matrix
                pts3D (nx3):    3D tracker coordinates
                pts2D (nx2):    2D image pixel coordinates
                intMtx (3x3):   intrinsic camera matrix

    Returns:    pxs (nx2):      reprojected pixels (i.e. from 3D points)
                pxErrs (n,):    vector of pixel errors
    """
    proj_pxs = []
    pxErrs = []
    n = pts3D.shape[1]
    for k in range(n):
        # Make 3D pt into column vector
        pt = pts3D[:, k]
        pt = np.reshape(pt, (3, 1))

        # Make 2D pixel into column vector
        px = pts2D[:, k]
        px = np.reshape(px, (2, 1))

        pt = np.vstack((pt, 1))
        
        # Register 3D pt to line
        camPt = extMtx @ pt

        # Convert 3D pt to homogeneous coordinates
        camPt /= camPt[2]
        camPt = camPt[0:2, :]
        camPt = np.vstack((camPt, 1))

        # Project point onto image using intrinsic matrix
        proj_px = intMtx @ camPt
        proj_pxs.append(proj_px)

        xErr = abs(proj_px[0, 0] - px[0, 0])
        yErr = abs(proj_px[1, 0] - px[1, 0])
        print("proj_px[0, 0]:", proj_px[0, 0])
        print("px[0, 0]:", px[0, 0])
        print("xErr:", xErr)

        print("proj_px[1, 0]:", proj_px[1, 0])
        print("px[1, 0]:", px[1, 0])
        print("yErr:", yErr)

        pxErrs.append(np.sqrt(xErr * xErr + yErr * yErr))
    pxErrs = np.reshape(pxErrs, (n, 1))
    return proj_pxs, pxErrs

def DistanceValidation(extMtx, pts3D, pts2D, intMtx):
    """
    Validates hand-eye calibration by finding distance error

    Arguments:  extMtx (4x4):   extrinsic calibration matrix
                pts3D (3xn):    3D tracker coordinates
                pts2D (2xn):    2D image pixel coordinates
                intMtx (3x3):   intrinsic camera matrix

    Returns:    distErrs (n,):  vector of distance errors
    """
    n = pts3D.shape[1]
    e = np.ones((n,))
    pts2D = np.linalg.inv(intMtx) @ np.vstack((pts2D, e))
    Y = np.empty((3, n))
    for i in range(n):
        x = pts2D[:, i]
        y = np.linalg.norm(x)
        z = x / y
        Y[:, i] = z

    pts2D = Y

    # Transform optical point to camera space
    pts3D = extMtx @ np.vstack((pts3D, e))

    # Store point magnitudes
    mags = np.empty((n, 1))
    for i in range(n):
        mags[i, 0] = np.sqrt(pts3D[0, i] * pts3D[0, i] + pts3D[1, i] * pts3D[1, i] + pts3D[2, i] * pts3D[2, i])
    
    # Normalize vector
    Y = np.empty((4, n))
    for i in range(n):
        x = pts3D[:, i]
        y = np.linalg.norm(x)
        z = x / y
        Y[:, i] = z
    pts3D = Y

    distErrs = np.empty((n, 1))
    for i in range(n):
        x = pts3D[0:3, i]
        q = pts2D[:, i]

        rot_axis = np.cross(x, q) / np.linalg.norm(np.cross(x, q))
        rot_angle = np.arccos(np.dot(x, q) / (np.linalg.norm(x) * np.linalg.norm(q)))
        R = np.hstack((rot_axis, rot_angle))

        angle = rot_angle
        distErrs[i, 0] = mags[i, 0] * np.tan(angle)
    return distErrs

def AngularValidation(extMtx, pts3D, pts2D, intMtx):
    """
    Validates hand-eye calibration by finding distance error

    Arguments:  extMtx (4x4):   extrinsic calibration matrix
                pts3D (3xn):    3D tracker coordinates
                pts2D (2xn):    2D image pixel coordinates
                intMtx (3x3):   intrinsic camera matrix

    Returns:    angularErrs (n,):   vector of angular errors
    """
    n = pts3D.shape[1]
    e = np.ones((n,))
    pts2D = np.linalg.inv(intMtx) @ np.vstack((pts2D, e))
    Y = np.empty((3, n))
    for i in range(n):
        x = pts2D[:, i]
        y = np.linalg.norm(x)
        z = x / y
        Y[:, i] = z
    pts2D = Y

    # Transform optical point to camera space
    pts3D = extMtx @ np.vstack((pts3D, e))

    # Normalize vector
    Y = np.empty((4, n))
    for i in range(n):
        x = pts3D[:, i]
        y = np.linalg.norm(x)
        z = x / y
        Y[:, i] = z
    pts3D = Y

    angularErrs = np.empty((n, 1))
    for i in range(n):
        x = pts3D[0:3, i]
        q = pts2D[:, i]

        rot_axis = np.cross(x, q) / np.linalg.norm(np.cross(x, q))
        rot_angle = np.arccos(np.dot(x, q) / (np.linalg.norm(x) * np.linalg.norm(q)))
        R = np.hstack((rot_axis, rot_angle))
        angularErrs[i, 0] = np.degrees(rot_angle)

    return angularErrs