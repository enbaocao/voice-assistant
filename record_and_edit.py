#!/usr/bin/env python3
"""
Voice Assistant with MCP

Records audio, transcribes it using Whisper, and sends it to an MCP server 
to execute file operations.
"""

import os
import tempfile
import sounddevice as sd
import soundfile as sf
import whisper
from mcp import Client

# Configuration
FS = 16_000  # 16-kHz mono is enough for Whisper tiny/base
RECORD_SECONDS = 5  # Duration of recording in seconds
MODEL_NAME = "base.en"  # Fast but accurate for English
SERVER_URL = "http://localhost:5000"  # Mac-Shell default; change if needed

def record_wav(path, seconds=RECORD_SECONDS):
    """Record audio from microphone to a WAV file."""
    print(f"Recording for {seconds} seconds... (speak now)")
    data = sd.rec(int(seconds * FS), samplerate=FS, channels=1, dtype='int16')
    sd.wait()
    sf.write(path, data, FS)
    print("Recording finished.")

def main():
    # Load Whisper model
    print(f"Loading Whisper {MODEL_NAME} model...")
    model = whisper.load_model(MODEL_NAME)
    
    # Connect to MCP server
    print(f"Connecting to MCP server at {SERVER_URL}...")
    server = Client(SERVER_URL)
    
    # Create temporary WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        # Record audio
        record_wav(tmp.name)
        
        # Transcribe audio to text
        print("Transcribing audio...")
        result = model.transcribe(tmp.name)
        prompt = result["text"]
        os.unlink(tmp.name)
        
        # Display transcribed text
        print("\n► Transcribed prompt:", prompt)
        
        # Ask for confirmation before sending to MCP
        confirm = input("Send this prompt to MCP? (y/N): ").strip().lower()
        
        if confirm == "y":
            print("Sending to MCP server...")
            
            # Change this depending on which MCP server you're using:
            # For Mac Shell:
            reply = server.tool("run_command", command=prompt)
            # For MCP Text Editor:
            # reply = server.tool("edit_file", command=prompt)
            
            print("\nMCP Response:")
            print(reply)
        else:
            print("Operation cancelled.")

if __name__ == "__main__":
    main()