import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import os
import pygame
import threading
import cv2
import numpy as np
import sounddevice as sd
from gtts import gTTS
import musicdict  # Your own file with a dictionary of songs

# ---------------- SPEAK FUNCTION ----------------
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

# --------------- INTRO VIDEO -----------------
def play_video():
    path = "amigo.mp4"
    cap = cv2.VideoCapture(path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Initializing Vision...", frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# ---------------- ALEXA STYLE WAVEFORM ----------------


# ---------------- PROCESS COMMANDS ----------------
def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play"):
        song = c.split(" ")[1]
        if song in musicdict.music:
            link = musicdict.music[song]
            webbrowser.open(link)
        else:
            speak("Sorry, song not found.")
    else:
        speak("Sorry, I didn't understand the command.")

# ---------------- MAIN LOOP ----------------
if __name__ == "__main__":

    # Start video in separate thread
    threading.Thread(target=play_video).start()
    speak("Initializing hello...")

    recognizer = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

            wake = recognizer.recognize_google(audio)
            print(f"You said: {wake}")

            if wake.lower() == "hello":
                speak("Yes, I am listening.")
                print("Listening for your command...")

                # Start waveform thread
               

                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=5)
                   

                    command = recognizer.recognize_google(audio)
                    print(f"Command: {command}")
                    processCommand(command)

        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
        except sr.UnknownValueError:
            print("Couldn't understand. Try again.")
        except Exception as e:
            print(f"Error: {e}")
