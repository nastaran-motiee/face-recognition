import subprocess
import wolframalpha
import pyttsx3
import tkinter
import json
import random
import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import feedparser
import smtplib
import ctypes
import time
import requests
import shutil
from twilio.rest import Client
from clint.textui import progress
from ecapture import ecapture as ec
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen
import pyaudio


class VoiceAssistant:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)

    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def hello(self, name):
        try:
            hour = int(datetime.datetime.now().hour)
            if name != 'Unknown':
                if 0 <= hour < 12:
                    self.speak(f"Good Morning{name}")

                elif 12 <= hour < 18:
                    self.speak(f"Good Afternoon{name}")

                else:
                    self.speak(f"Good Evening{name}")

                self.speak("Do you need to get home?")
            else:
                self.speak("Sorry, can't recognize you")
        except:
            print("Already in process...")





