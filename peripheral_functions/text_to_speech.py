import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()

# Say something
engine.say("Hello! I'm your Python voice.")
engine.runAndWait()
