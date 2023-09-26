# Import necessary libraries
from flask import Flask, render_template, request, redirect, jsonify, send_from_directory
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from transformers import BartTokenizer, BartForConditionalGeneration
import os

app = Flask(__name__)

# BART summarization model and tokenizer
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
summarization_model = BartForConditionalGeneration.from_pretrained(model_name)

#  path to build directory
react_build_dir = os.path.join(os.path.dirname(__file__), 'client/build')

@app.route("/", methods=["GET"])
def index():
    return send_from_directory(react_build_dir, 'index.html')

@app.route("/static/<path:path>", methods=["GET"])
def serve_static(path):
    return send_from_directory(os.path.join(react_build_dir, 'static'), path)

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        transcript = data.get("transcript", "")

        #summarization using BART model
        input_ids = tokenizer.encode("summarize: " + transcript, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = summarization_model.generate(input_ids, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host='0.0.0.0', port=8080)
