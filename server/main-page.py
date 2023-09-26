# Import necessary libraries
import os
from io import BytesIO

import speech_recognition as sr
import torch
from flask import (Flask, jsonify, redirect, render_template, request,
                   send_from_directory)
from pydub import AudioSegment
from transformers import BartForConditionalGeneration, BartTokenizer
from flask_cors import CORS

# Initialize PyTorch (make sure to do this before loading the model)
torch_device = "cuda" if torch.cuda.is_available() else "cpu"
torch.set_default_tensor_type("torch.FloatTensor")


app = Flask(__name__)
CORS(app)

# BART summarization model and tokenizer
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
summarization_model = BartForConditionalGeneration.from_pretrained(model_name)

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        transcript = data.get("transcript", "")

        # Tokenize and summarize the transcript
        input_ids = tokenizer.encode("summarize: " + transcript, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = summarization_model.generate(input_ids, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host='0.0.0.0', port=8080)
