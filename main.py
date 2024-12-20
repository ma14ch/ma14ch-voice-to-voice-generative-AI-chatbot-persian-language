from flask import Flask, render_template, request, jsonify, send_file
import tempfile
from openai import OpenAI
from hezar.models import Model
import os
import requests

# Load Whisper model
model = Model.load("hezarai/whisper-small-fa")

# Initialize OpenAI client
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Initialize Flask app
app = Flask(__name__)

# Function to convert voice to text
def convert_voice_to_text(audio_data: bytes) -> str:
    # Save the recorded audio to a temporary MP3 file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
        temp_audio_file.write(audio_data)
        audio_path = temp_audio_file.name

    transcripts = model.predict(audio_path)
    transcription = transcripts.get('text', 'Error: Transcription failed') if isinstance(transcripts, dict) else str(transcripts)

    # Remove the temporary file
    os.remove(audio_path)

    return transcription

# Function to generate text using OpenAI model
def generate_text(messages, model="aya-23-8b"):
    try:
        response = client.chat.completions.create(model=model, messages=messages)
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# Define the home route
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle audio upload and processing
@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audio_data' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio_data']
    audio_data = audio_file.read()

    # Convert voice to text
    transcription = convert_voice_to_text(audio_data)

    # Generate a response from the model
    chat_history = [
        {"role": "user", "content": transcription}
    ]
    response_text = generate_text(chat_history)

    # Call the FastAPI TTS service to convert response text to speech
    tts_api_url = "http://localhost:8000/synthesize/"
    tts_response = requests.post(tts_api_url, json={"text": response_text})

    if tts_response.status_code == 200:
        # Save the output audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_file.write(tts_response.content)
            audio_path = temp_audio_file.name

        return send_file(audio_path, mimetype="audio/wav", as_attachment=True, download_name="response_audio.wav")
    else:
        return jsonify({'error': 'Failed to generate speech'}), 500

if __name__ == '__main__':
    app.run(debug=True)
