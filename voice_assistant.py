import os
from threading import Lock
import pyttsx3
import datetime
import sys
import speech_recognition as sr


def _take_command():
    """
    Takes voice instructions from the user
    :return: command
    """

    r = sr.Recognizer()
    r.energy_threshold = 4000  # adjust this value to your liking

    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(e)


class VoiceAssistant:
    def __init__(self, **kwargs):
        super(VoiceAssistant, self).__init__(**kwargs)
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)

    def speak(self, text):
        """
        Makes the engine to speak
        :param text: String for the engine speech
        :return: None
        """
        self.engine.say(text)
        self.engine.runAndWait()

    def hello(self, name, floor_number):
        """
        Greets the user according to the hour
        :param floor_number:
        :param name: name of user
        :return:none
        """
        #   try:
        hour = int(datetime.datetime.now().hour)

        if name != "Unknown" and floor_number != "Unknown":
            if 0 <= hour < 12:
                self.speak(f"Good Morning")

            elif 12 <= hour < 18:
                self.speak(f"Good Afternoon")

            else:
                self.speak(f"Good Evening")

            self.speak(f"Would you like to get to floor {floor_number}?")
            _take_command()

        # else:
        #     self.speak("Sorry, can't recognize you")

    #  except:
    #      print("Already in process...")
