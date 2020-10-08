import threading
import time

import cv2
import dlib
import imutils
from imutils import face_utils
from scipy.spatial import distance

EAR_THRESHOLD = 0.2
LEAST_CONSECUTIVE_FRAMES = 3

PREDICTOR_PATH = 'models/shape_predictor_68_face_landmarks.dat'
(LEFT_START_INDEX, LEFT_END_INDEX) = (42, 48)
(RIGHT_START_INDEX, RIGHT_END_INDEX) = (36, 42)

FRAME_WIDTH = 640
FRAME_HEIGHT = 480


def eye_aspect_ratio(eye):
    """EAR - Eye Aspect Ratio"""
    a = distance.euclidean(eye[1], eye[5])
    b = distance.euclidean(eye[2], eye[4])

    c = distance.euclidean(eye[0], eye[3])

    return (a + b) / (2.0 * c)


class BlinkDetector:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(PREDICTOR_PATH)

        self.webcam = cv2.VideoCapture(0)
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

        self.total_blinks = 0
        self.blinked = False
        _, self.current_frame = self.webcam.read()

        self.started = False
        self.read_lock = threading.Lock()

    def start(self):
        if self.started:
            print('[!] Threaded video capturing has already been started.')
            return

        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()

    def update(self):
        counter = 0
        while self.started:
            retrieved, frame = self.webcam.read()
            if not retrieved:
                continue

            with self.read_lock:
                self.current_frame = frame

            frame = imutils.resize(frame, width=400)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces_rects = self.detector(gray_frame, 0)

            for rect in faces_rects:
                shape = self.predictor(gray_frame, rect)
                shape = face_utils.shape_to_np(shape)

                left_eye = shape[LEFT_START_INDEX: LEFT_END_INDEX]
                right_eye = shape[RIGHT_START_INDEX: RIGHT_END_INDEX]

                ear_left = eye_aspect_ratio(left_eye)
                ear_right = eye_aspect_ratio(right_eye)
                ear = (ear_left + ear_right) / 2.0

                if ear < EAR_THRESHOLD:
                    counter += 1
                else:
                    if counter >= LEAST_CONSECUTIVE_FRAMES:
                        with self.read_lock:
                            self.total_blinks += 1
                            self.blinked = True

                    counter = 0

            # time.sleep(1 / 30)

    def check_blinked(self):
        with self.read_lock:
            if self.blinked:
                self.blinked = False
                return True
            return False

    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exec_type, exc_value, traceback):
        self.webcam.release()
