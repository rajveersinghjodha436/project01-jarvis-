import speech_recognition as sr
import webbrowser
import pyttsx3
import sys
import time

recognizer = sr.Recognizer()

def speak(text):
    engine = pyttsx3.init("sapi5")  # re-init EVERY time
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def processCommand(command):
    command = command.lower()

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "exit" in command or "stop" in command:
        speak("Goodbye")
        sys.exit()

    else:
        speak("I did not understand that command")

if __name__ == "__main__":
    speak("Initializing Jarvis")

    while True:
        try:
            # Wake word
            with sr.Microphone() as source:
                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source)

            wake = recognizer.recognize_google(audio)
            print("Heard:", wake)

            if wake.lower() == "jarvis":
                speak("Yes sir")
                time.sleep(0.3)  # IMPORTANT pause

                # Command
                with sr.Microphone() as source:
                    print("Listening for command...")
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source)

                command = recognizer.recognize_google(audio)
                print("Command:", command)
                processCommand(command)

        except sr.UnknownValueError:
            print("Could not understand")

        except Exception as e:
            print("Error:", e)
