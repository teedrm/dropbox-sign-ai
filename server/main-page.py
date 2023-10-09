import json
import os
import re
from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/api/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        transcript = data.get("transcript", "")
        cleaned_transcript = preprocess_transcript(transcript)

        # summary using GPT-3
        generated_summary = generate_summary(cleaned_transcript)
        print("Generated Summary:", generated_summary) 

        response = openai.Completion.create(
            engine="gpt-3.5-turbo-16k",
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
    # Sending the text to OpenAI's GPT-3.5 Turbo API
    try:
        # Ensure that text length does not exceed the maximum token limit for the model
        if len(text.split()) > 4096:  # Splitting by whitespace for simplicity
            raise ValueError("Text exceeds the maximum token limit for GPT-3.5 Turbo.")
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Summarize: {text}"}
        ]
        
        response = openai.Completion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
            max_tokens=150,  # Adjust max_tokens as per your requirement
            temperature=0.7  # Adjust temperature as per your requirement
        )
        
        summary = response['choices'][0]['message']['content'].strip()
        return summary
    
    except Exception as e:
        print(f"Error in generating summary: {str(e)}")
        return ""


if __name__ == "__main__":
    app.run(debug=True, threaded=True, host='0.0.0.0', port=8080)
