from flask import Flask, render_template, request, redirect
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            try:
                audio = AudioSegment.from_mp3(file)
                audio.export("temp.wav", format="wav")
                audio_file = sr.AudioFile("temp.wav")
                recognizer = sr.Recognizer()
                with audio_file as source:
                    audio_data = recognizer.record(source)
                transcript = recognizer.recognize_google(audio_data, key=None)
            except Exception as e:
                transcript = f"Error: {str(e)}"

    return render_template('index.html', transcript=transcript)

if __name__ == "__main__":
    app.run(debug=True, threaded=True,host='0.0.0.0', port=8080)
