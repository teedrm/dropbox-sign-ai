# Import necessary libraries
from flask import Flask, render_template, request, redirect, jsonify
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from transformers import BartTokenizer, BartForConditionalGeneration

# Initialize the Flask app
app = Flask(__name__)

# Load BART summarization model and tokenizer
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
summarization_model = BartForConditionalGeneration.from_pretrained(model_name)

# Define the index route
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

# Define a route for summarization
@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        transcript = data.get("transcript", "")

        # Perform summarization using BART model
        input_ids = tokenizer.encode("summarize: " + transcript, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = summarization_model.generate(input_ids, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host='0.0.0.0', port=8080)
