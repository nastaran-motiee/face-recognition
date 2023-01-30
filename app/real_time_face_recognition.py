from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import face_recognition
import numpy as np
import cv2
from model.mongo_db import Model
from voice_assistant import VoiceAssistant
from concurrent.futures import ThreadPoolExecutor


class KivyCamera(Image):
    """
    kivy camera - gets open-cv video capture as argument and integrates it into kivy camera.
                - when the "Verify" button is pressed, the _identity_check method whill be invoked.
    """

    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.identification_event = None
        self.executor = ThreadPoolExecutor(1)
        self.frame = None
        self.ret = None
        self.last_face_encoding = None
        self.current_small_frame = None
        self.small_frame = None
        self.rgb_small_frame = None
        self.all_face_locations = []
        self._load_data()
        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.fps = 33.
        self.talking = False
        self.voice_assistant = VoiceAssistant()
        self.face_recognition_event = Clock.schedule_interval(self._update, 1.0 / self.fps)

    # self.identification_event = Clock.schedule_interval(self._identity_check, 1.0 / self.fps)

    def _update(self, dt):

        """
        updates the captured video from open-cv each 30 sec
        """
        # if 'q' key is pressed , stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False

        # get the current frame from the video stream as an image
        self.ret, self.frame = self.capture.read()

        self.current_small_frame = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)
        all_faces_locations = face_recognition.face_locations(self.current_small_frame)

        if self.process_this_frame and len(all_faces_locations) > 0:
            if self.last_face_encoding is None:
                self._identity_check()
            else:
                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                self.rgb_small_frame = self.current_small_frame[:, :, ::-1]
                face_encodings = face_recognition.face_encodings(
                    self.rgb_small_frame, self.face_locations)

                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(face_encoding, self.last_face_encoding)

                    for match in matches:
                        if not match:
                            self._identity_check()

        if self.ret:
            # convert it to texture
            buf1 = cv2.flip(self.frame, 0)
            buf = buf1.tobytes()
            image_texture = Texture.create(
                size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture


    def _load_data(self):
        """
        Loads the necessary data for the application to run
        :return: None
        """

        # Load a sample picture and learn how to recognize it.

        # Load a second sample picture and learn how to recognize it.
        # self.biden_image = face_recognition.load_image_file("app\model\images\Joe_Biden_presidential_portrait.jpg")
        # self.biden_face_encoding = face_recognition.face_encodings(self.biden_image)[0]
        # Model.add_user(name="Joe", face_encoding=list(self.biden_face_encoding), floor_number=4)

        # get all face_encodings from DB
        known_face_encodings_from_mongo = Model.get_all_face_encodings()
        self.known_face_encodings = []
        for face_encoding_dict in known_face_encodings_from_mongo:
            self.known_face_encodings.append(
                np.array(face_encoding_dict["face_encoding"]))

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

    def _identity_check(self):
        """
        checks the identity of the person which is in front of the camera
        if the person is recognized - shows the name of the person
        else - shows unknown
        """

        # Only process every other frame of video to save time
        global first_match_index
        if self.process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            self.rgb_small_frame = small_frame[:, :, ::-1]

            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(
                self.rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(
                self.rgb_small_frame, self.face_locations)

            for face_encoding in self.face_encodings:
                self.last_face_encoding = [np.array(face_encoding)]
                break

            face_names = []

            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                self.matches = face_recognition.compare_faces(
                    self.known_face_encodings, face_encoding)
                name = "Unknown"
                floor_number = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in self.matches:
                    first_match_index = self.matches.index(True)
                    name = Model.get_user_info(self.known_face_encodings[first_match_index])['name']
                    floor_number = Model.get_user_info(self.known_face_encodings[first_match_index])['floor_number']

                # Or instead, use the known face with the smallest distance to the new face
                self.face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                self.best_match_index = np.argmin(self.face_distances)

                if self.matches[self.best_match_index]:
                    name = Model.get_user_info(self.known_face_encodings[first_match_index])['name']
                    floor_number = Model.get_user_info(self.known_face_encodings[first_match_index])['floor_number']

                face_names.append(name)

                print(name)

                if len(face_names) != 0:
                    self.executor.submit(self.voice_assistant.hello, name, floor_number)

    def verify_button_action(self):
        """
        -Schedules identification
        -used when verify button is pressed
        :return: None
        """
        self.identification_event = Clock.schedule_interval(
            self._identity_check, 1.0 / 30.0)

    def stop(self):
        self.capture.release()
        cv2.destroyAllWindows()
