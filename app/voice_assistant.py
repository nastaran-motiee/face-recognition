from threading import Lock
import pyttsx3
import datetime
import speech_recognition as sr


def _take_command():
    """
    Takes voice instructions from the user
    :return: command
    """
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
        return "None"

    return query


class VoiceAssistant:
    def __init__(self, **kwargs):
        super(VoiceAssistant, self).__init__(**kwargs)
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)

    def speak(self, audio):
        """
        Makes the engine to speak
        :param audio: String for the engine speech
        :return: None
        """
        self.engine.say(audio)
        self.engine.runAndWait()

    def hello(self, name, floor_number):
        """
        Greets the user according to the hour
        :param name: name of user
        :return:none
        """
        #   try:
        hour = int(datetime.datetime.now().hour)

        if name != "Unknown" and floor_number != "Unknown":
            if 0 <= hour < 12:
                self.speak(f"Good Morning{name}")

            elif 12 <= hour < 18:
                self.speak(f"Good Afternoon{name}")

            else:
                self.speak(f"Good Evening{name}")

            self.speak(f"Your destination is floor {floor_number}")
            # self._take_command()

        else:
            self.speak("Sorry, can't recognize you")

    #  except:
    #      print("Already in process...")
