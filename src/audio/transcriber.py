import os
from faster_whisper import WhisperModel
from pathlib import Path

class SpeechToText:
    def __init__(self, model_size="tiny", device="cpu", compute_type="int8"):
        """
        Initialize the speech-to-text transcriber with Whisper.
        
        Args:
            model_size: Size of Whisper model ("tiny", "base", "small", "medium", "large")
            device: Device to run the model on ("cpu" or "cuda")
            compute_type: Computation type for efficiency
        """
        # Load model
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        print(f"Loaded Whisper model: {model_size}")
        
    def transcribe(self, audio_path):
        """
        Transcribe audio file to text.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Transcribed text
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
        # Transcribe audio
        segments, info = self.model.transcribe(audio_path, beam_size=5)
        
        # Extract text from segments
        transcript = " ".join([segment.text for segment in segments])
        
        return transcript.strip()