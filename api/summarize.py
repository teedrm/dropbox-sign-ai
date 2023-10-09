import json
import os
import openai
import re

# Use environment variable for OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')

def handler(event):
    try:
        data = json.loads(event.body)
        transcript = data.get("transcript", "")
        cleaned_transcript = preprocess_transcript(transcript)

        # Generate summary using GPT-3.5-turbo
        generated_summary = generate_summary(cleaned_transcript)

        # Use summary as a prompt for further OpenAI API call
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-16k",  # Adjust engine as needed
            prompt=generated_summary,
            max_tokens=4000,  # Adjust as needed
            n=1,
            stop=None,
            temperature=0.7
        )
        generated_responses = [choice['text'].strip() for choice in response['choices']]

        return {
            'statusCode': 200,
            'body': json.dumps({
                'summary': generated_summary,
                'responses': generated_responses
            }),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }

def preprocess_transcript(transcript):
    cleaned_transcript = re.sub(r'\d{2}:\d{2}:\d{2}:', '. ', transcript)
    sentences = re.split(r'(?<=[.!?])\s+', cleaned_transcript)
    cleaned_sentences = [s.strip() for s in sentences if len(s) > 10]
    return '. '.join(cleaned_sentences)

def generate_summary(text):
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-16k",
            prompt=text,
            max_tokens=4000,
            n=1,
            stop=None,
            temperature=0.7
        )
        summary = response.choices[0].text.strip()
        return summary
    except Exception as e:
        print("Error in generating summary:", str(e))
        return text  # Return original text if summarization fails
