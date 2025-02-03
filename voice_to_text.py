import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        audio = recognizer.listen(source)  # Capture audio

    try:
        text = recognizer.recognize_google(audio)  # Convert speech to text using Google API
        print("You said:", text)
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio.")
    except sr.RequestError:
        print("Error with the speech recognition service.")

if __name__ == "__main__":
    recognize_speech()
