import cv2.cv as cv
import os.path as path

path_root = path.abspath(path.dirname(__file__))
cascade = cv.Load(path.join(path_root, 'data','haarcascade_frontalface_default.xml'))

def find_face(image):
    """
    Returns a bounding box (tuple pair of (x,y) coordinates) if a face was
    detected; None otherwise. For more than one candidate bounding box, the
    largest is returned.

    Arguments:
    image -- an OpenCV image

    Keywords arguments:
    granularity -- a float from 0 to 1 determining how granularly the image will
    be considered for face detection. Raise to improve quality of detection,
    lower to speed up the detector at the cost of detection quality.
    """
    candidates = cv.HaarDetectObjects(image, cascade, cv.CreateMemoryStorage(0))
    if candidates:
        return max(candidates, key=lambda e:(e[0][3] * e[0][2],
                                             -(sum(e[0][0:1]))))
    else:
        return None

def crop(image, bounds):
    pass

if __name__ == '__main__':
    pass
