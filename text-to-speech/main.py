from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from TTS.utils.synthesizer import Synthesizer
from pydantic import BaseModel
import uvicorn
from pydub import AudioSegment
import os
# Initialize the FastAPI app
app = FastAPI()

# Model configuration
model_path = "checkpoint_48000.pth"  # Absolute path to the model checkpoint.pth
config_path = "config-2.json"  # Absolute path to the model config.json
download_url = "https://huggingface.co/Kamtera/persian-tts-female-vits/blob/main/checkpoint_48000.pth"

# Check if the file exists
if not os.path.exists(model_path):
    print(f"{model_path} not found. Downloading from {download_url}...")
    try:
        # Download the file
        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            with open(model_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Downloaded and saved as {model_path}.")
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred during the download: {e}")
else:
    print(f"{model_path} already exists. No download needed.")
# Initialize the TTS synthesizer
try:
    synthesizer = Synthesizer(model_path, config_path, use_cuda=True)
except Exception as e:
    print(f"Error loading model: {e}")
    synthesizer = None

# Pydantic model for text input
class TextToSpeechRequest(BaseModel):
    text: str

@app.on_event("startup")
async def load_model():
    global synthesizer
    if synthesizer is None:
        synthesizer = Synthesizer(model_path, config_path, use_cuda=True)
        print("Model loaded successfully!")

@app.post("/synthesize/")
async def synthesize(request: TextToSpeechRequest):
    """
    Synthesizes text into speech and returns the audio file in MP3 format.
    """
    try:
        text = request.text
        if not text:
            raise HTTPException(status_code=400, detail="Text cannot be empty.")
        
        # Synthesize speech
        wavs = synthesizer.tts(text)
        
        # Save the output audio as WAV
        output_wav_file = "output_audio.wav"
        synthesizer.save_wav(wavs, output_wav_file)
        
        # Convert WAV to MP3 using pydub
        output_mp3_file = "output_audio.mp3"
        audio = AudioSegment.from_wav(output_wav_file)
        audio.export(output_mp3_file, format="mp3")
        
        # Return the MP3 file
        return FileResponse(output_mp3_file, media_type="audio/mpeg", filename="output_audio.mp3")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during synthesis: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Welcome to the TTS API! Use /synthesize/ endpoint to convert text to speech."}

# Run the app using uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
