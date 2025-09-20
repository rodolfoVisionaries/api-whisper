from fastapi import FastAPI, UploadFile, File
from services.whisper_service import transcribe_file

app = FastAPI()

# Transcribe Endpoint
@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    transcript = transcribe_file(file)
    return {"transcript": transcript}