import speech_recognition as sr
import webbrowser
import pyttsx3
import sys
import time
import os
import subprocess

def speak(text, wait=True):
    """Text-to-speech function"""
    try:
        engine = pyttsx3.init("sapi5")
        engine.say(text)
        if wait:
            engine.runAndWait()
        else:
            # Run without waiting
            engine.startLoop(False)
            engine.iterate()
            engine.endLoop()
    except Exception as e:
        print(f"Speech Error: {e}")
        print(f"Assistant: {text}")

def list_microphones():
    """List all available microphones"""
    print("\n🔍 Available Microphones:")
    try:
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"  {index}: {name}")
        return True
    except Exception as e:
        print(f"  Error listing microphones: {e}")
        return False

def get_microphone_index():
    """Let user select microphone or use default"""
    list_microphones()
    try:
        choice = input("\nEnter microphone number (or press Enter for default): ").strip()
        if choice:
            return int(choice)
    except:
        pass
    return None

def process_command(command):
    """Process voice commands"""
    command = command.lower().strip()
    print(f"Processing command: '{command}'")
    
    # OPEN COMMANDS - SIMPLIFIED
    if "open google" in command:
        speak("Opening Google")
        print("Opening https://www.google.com")
        webbrowser.open("https://www.google.com")
        return True
        
    elif "open youtube" in command:
        speak("Opening YouTube")
        print("Opening https://www.youtube.com")
        webbrowser.open("https://www.youtube.com")
        return True
        
    elif "open notepad" in command:
        speak("Opening Notepad")
        print("Opening Notepad")
        os.system("notepad.exe")
        return True
        
    elif "open calculator" in command:
        speak("Opening Calculator")
        print("Opening Calculator")
        os.system("calc.exe")
        return True
        
    elif "open browser" in command or "open chrome" in command:
        speak("Opening Browser")
        print("Opening default browser")
        webbrowser.open("https://www.google.com")
        return True
    
    # EXIT COMMANDS
    elif any(word in command for word in ["exit", "stop", "quit", "goodbye"]):
        speak("Goodbye!")
        print("Shutting down...")
        return "exit"
    
    # HELP
    elif "help" in command or "what can you do" in command:
        help_text = """
        I can help you with:
        - Opening Google: say 'open Google'
        - Opening YouTube: say 'open YouTube'
        - Opening Notepad: say 'open notepad'
        - Opening Calculator: say 'open calculator'
        - Exit: say 'exit' or 'stop'
        """
        print(help_text)
        speak("I can open Google, YouTube, Notepad, Calculator, or help you exit. Try saying 'open Google'")
        return True
    
    else:
        speak(f"I heard: {command}. Try saying 'open Google' or 'help'")
        return True

def test_microphone():
    """Test if microphone is working"""
    print("\n🎤 Testing microphone...")
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("Please say something for testing (3 seconds)...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
            
        print("Processing audio...")
        text = recognizer.recognize_google(audio)
        print(f"✅ Success! Heard: '{text}'")
        return True
    except sr.WaitTimeoutError:
        print("❌ No speech detected")
        return False
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return False
    except Exception as e:
        print(f"❌ Microphone error: {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("JARVIS VOICE ASSISTANT - DEBUG VERSION")
    print("=" * 60)
    
    # Initialize recognizer
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300  # Adjust sensitivity
    recognizer.dynamic_energy_threshold = True
    
    # Test microphone first
    if not test_microphone():
        print("\n⚠️  Microphone test failed. Trying with different settings...")
        choice = input("Continue anyway? (y/n): ").lower()
        if choice != 'y':
            return
    
    speak("Jarvis initialized. Say 'Jarvis' to activate.", wait=True)
    print("\n🎯 Ready! Say 'Jarvis' followed by a command")
    print("   Example: 'Jarvis open Google'")
    print("   Say 'exit' to quit")
    print("-" * 60)
    
    # Get microphone choice
    mic_index = get_microphone_index()
    
    while True:
        try:
            # Listen for audio
            if mic_index is not None:
                with sr.Microphone(device_index=mic_index) as source:
                    print("\n🔊 Listening... (Say 'Jarvis')")
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
            else:
                with sr.Microphone() as source:
                    print("\n🔊 Listening... (Say 'Jarvis')")
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
            
            # Try to recognize
            try:
                text = recognizer.recognize_google(audio).lower()
                print(f"📝 Heard: {text}")
                
                # Check for wake word
                if "jarvis" in text:
                    speak("Yes?", wait=False)
                    time.sleep(0.3)
                    
                    # Listen for command
                    if mic_index is not None:
                        with sr.Microphone(device_index=mic_index) as source:
                            print("🎤 Listening for command...")
                            recognizer.adjust_for_ambient_noise(source, duration=0.3)
                            command_audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
                    else:
                        with sr.Microphone() as source:
                            print("🎤 Listening for command...")
                            recognizer.adjust_for_ambient_noise(source, duration=0.3)
                            command_audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
                    
                    command = recognizer.recognize_google(command_audio)
                    print(f"💡 Command: {command}")
                    
                    # Process command
                    result = process_command(command)
                    if result == "exit":
                        break
                    
            except sr.UnknownValueError:
                print("❓ Could not understand audio")
            except sr.RequestError as e:
                print(f"🌐 API Error: {e}")
                speak("Speech service is unavailable")
            except Exception as e:
                print(f"⚠️  Recognition error: {e}")
                
        except sr.WaitTimeoutError:
            # No speech detected, continue listening
            continue
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down...")
            speak("Goodbye!")
            break
        except Exception as e:
            print(f"💥 Unexpected error: {e}")
            time.sleep(1)  # Prevent tight loop on errors

if __name__ == "__main__":
    main()

    