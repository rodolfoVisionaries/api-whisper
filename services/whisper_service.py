import os
import subprocess
import shutil

TEMP_DIR = "temp_audios"
OUTPUT_DIR = "transcripts"

ffmpeg_dir = r"C:\ffmpeg-8.0-essentials_build\bin"
os.environ["PATH"] += os.pathsep + ffmpeg_dir

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def transcribe_file(file) -> str:
    temp_path = os.path.join(TEMP_DIR, file.filename)
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Whisper CLI
    command = [
        "whisper",
        temp_path,
        "--task", "transcribe",
        "--model", "medium",
        "--verbose", "False",
        "--output_dir", OUTPUT_DIR
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Whisper failed: {e}")

    transcript_file = os.path.join(
        OUTPUT_DIR,
        os.path.splitext(os.path.basename(temp_path))[0] + ".txt"
    )

    if not os.path.exists(transcript_file):
        raise FileNotFoundError(f"Transcription not generated for {file.filename}")
    with open(transcript_file, "r", encoding="utf-8") as f:
        transcript = f.read()

    os.remove(temp_path)
    return transcript
