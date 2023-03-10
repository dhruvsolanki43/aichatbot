from flask import Flask, request
import speech_recognition as sr
from gTTs import gTTS
import os

app = Flask(__name__)


@app.route('/voice', methods=['POST'])
def voice():
    audio_data = request.data
    with open('audio.wav', 'wb') as f:
        f.write(audio_data)
    r = sr.Recognizer()
    with sr.AudioFile('audio.wav') as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio)
        tts = gTTS(text)
        tts.save('output.mp3')
        with open('output.mp3', 'rb') as f:
            audio_data = f.read()
        return audio_data
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return "Error: {0}".format(e)
    
def voice_assistant(voice_command):
    r = sr.Recognizer()
    with sr.AudioFile(voice_command) as source:
        audio = r.record(source)
    try:
        command = r.recognize_google(audio)
    except sr.UnknownValueError:
        return "I'm sorry, I didn't understand that."
    if "hello" in command.lower():
        response = "Hello! How can I help you today?"
    else:
        response = "I'm sorry, I don't know how to respond to that."
    tts = gTTS(text=response, lang='en')
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")

if __name__ == '__main__':
    app.run(debug=True)


