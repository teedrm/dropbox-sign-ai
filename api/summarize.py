from flask import Flask, jsonify, request
import os
import openai
import re
from transformers import BartForConditionalGeneration, BartTokenizer

# Load environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# BART
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
summarization_model = BartForConditionalGeneration.from_pretrained(model_name)

app = Flask(__name__)

@app.route("/api/summarize", methods=["POST"])
def summarize():
    # Your existing code remains largely the same
    try:
        data = request.get_json()
        transcript = data.get("transcript", "")
        cleaned_transcript = preprocess_transcript(transcript)

        # summary using BART
        generated_summary = generate_summary(cleaned_transcript)

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=generated_summary,
            max_tokens=4000,
            n=1,
            stop=None,
        )

        generated_responses = [choice.text.strip() for choice in response.choices]

        return jsonify({"summary": generated_summary, "responses": generated_responses})

    except Exception as e:
        return jsonify({"error": str(e)})

def preprocess_transcript(transcript):
    cleaned_transcript = re.sub(r'\d{2}:\d{2}:\d{2}:', '. ', transcript)
    sentences = re.split(r'(?<=[.!?])\s+', cleaned_transcript)
    cleaned_sentences = [s.strip() for s in sentences if len(s) > 10]
    return '. '.join(cleaned_sentences)

def generate_summary(text):
    sentences = text.split('. ')
    summarized_sentences = []

    for sentence in sentences:
        input_ids = tokenizer.encode(sentence, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = summarization_model.generate(input_ids, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summarized_sentences.append(summary)

    combined_summary = ' '.join(summarized_sentences)
    summary_without_timestamps = ' '.join([sentence.split(': ', 1)[-1] for sentence in combined_summary.split('. ')])
    
    return summary_without_timestamps.strip()
