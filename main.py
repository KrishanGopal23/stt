# main.py
import whisper
import tempfile
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Initialize the FastAPI app
app = FastAPI(title="Whisper Transcription API")

# 2. Load the Whisper model on startup
# This is done once to avoid reloading the model for every request
try:
    logger.info("Loading Whisper model...")
    # Using "tiny" as it's the most lightweight. 
    # Change to "base" or "small" for better accuracy, but requires more resources.
    model = whisper.load_model("tiny") 
    logger.info("Whisper model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading Whisper model: {e}")
    model = None

@app.post("/transcribe")
async def transcribe_audio(
    audio_file: UploadFile = File(...),
    language: str = Form("en") # Default language is English
):
    """
    Accepts an audio file and a language code to perform transcription.
    """
    if not model:
        raise HTTPException(status_code=500, detail="Whisper model is not available.")

    # 3. Save the uploaded audio file to a temporary file
    # Whisper's transcribe function works with file paths
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as tmp_file:
            shutil.copyfileobj(audio_file.file, tmp_file)
            tmp_path = tmp_file.name
        
        logger.info(f"Transcribing audio file for language: {language}")

        # 4. Perform the transcription
        result = model.transcribe(tmp_path, language=language, fp16=False)
        
        logger.info("Transcription completed successfully.")
        
        # 5. Return the result as JSON
        return JSONResponse(content={
            "language": result.get("language", language),
            "transcription": result.get("text", "")
        })
    except Exception as e:
        logger.error(f"Error during transcription: {e}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
    finally:
        # Clean up the temporary file
        audio_file.file.close()
        if 'tmp_path' in locals() and tmp_path:
            import os
            os.remove(tmp_path)

@app.get("/")
def read_root():
    return {"message": "Whisper API is running. Post an audio file to /transcribe."}
