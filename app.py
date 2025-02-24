from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import asyncio
import speech_recognition as sr
from gtts import gTTS
import subprocess

# Initialize FastAPI App
app = FastAPI()

# Enable CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up templates directory for Jinja2
templates = Jinja2Templates(directory="templates")

# Ensure 'temp' folder exists for saving audio files
os.makedirs("temp", exist_ok=True)

# Define Request Model for Translation
class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str

# Serve the HTML Page for the Translator
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API Endpoint: Text Translation (Uses Google Translate)
@app.post("/translate")
async def translate(request: TranslationRequest):
    """
    Translates input text using Google Translate API.
    """
    from deep_translator import GoogleTranslator
    
    try:
        translated_text = GoogleTranslator(source=request.source_language, target=request.target_language).translate(request.text)
        return {"translated_text": translated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

# Function to Convert MP3 to WAV for Speech Recognition
def convert_mp3_to_wav(mp3_path: str, wav_path: str):
    """
    Converts an MP3 file to WAV format using FFmpeg.
    """
    try:
        subprocess.run(["ffmpeg", "-i", mp3_path, "-ar", "16000", "-ac", "1", wav_path], check=True)
        return True
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="FFmpeg not found. Ensure it is installed and added to PATH.")
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="MP3 to WAV conversion failed using FFmpeg.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# API Endpoint: Speech-to-Text (MP3 to Text Conversion)
@app.post("/speech-to-text")
async def speech_to_text(audio_file: UploadFile = File(...)):
    """
    Converts uploaded MP3 file to text.
    """
    try:
        if not audio_file.filename.endswith(".mp3"):
            raise HTTPException(status_code=400, detail="Only MP3 format is allowed.")

        # Save uploaded MP3
        mp3_path = f"temp/{audio_file.filename}"
        wav_path = mp3_path.replace(".mp3", ".wav")
        with open(mp3_path, "wb") as f:
            f.write(await audio_file.read())

        # Convert MP3 to WAV
        if not convert_mp3_to_wav(mp3_path, wav_path):
            raise HTTPException(status_code=500, detail="MP3 to WAV conversion failed. Ensure FFmpeg is installed.")

        # Perform Speech Recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        return {"text": text}

    except sr.UnknownValueError:
        raise HTTPException(status_code=400, detail="Could not understand the audio.")
    except sr.RequestError:
        raise HTTPException(status_code=500, detail="Speech recognition service error.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech-to-text conversion failed: {str(e)}")

# API Endpoint: Text-to-Speech (Generates MP3 from Text)
@app.post("/text-to-speech")
async def text_to_speech(text: str):
    """
    Converts text to speech and returns an MP3 file.
    """
    try:
        if not text.strip():
            raise HTTPException(status_code=400, detail="Text input is required.")

        audio_path = "temp/translated_audio.mp3"
        
        # Remove previous audio file to prevent conflicts
        if os.path.exists(audio_path):
            os.remove(audio_path)

        # Generate and save new speech audio
        tts = gTTS(text)
        tts.save(audio_path)

        return FileResponse(audio_path, media_type="audio/mpeg", filename="translated_audio.mp3")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text-to-speech conversion failed: {str(e)}")
