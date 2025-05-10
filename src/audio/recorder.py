import pyaudio
import wave
import numpy as np
import threading
import tempfile
import os
from pathlib import Path

class VoiceRecorder:
    def __init__(self, 
                 rate=16000, 
                 chunk_size=1024, 
                 channels=1, 
                 format=pyaudio.paInt16,
                 silence_threshold=1000,
                 silence_duration=1.5):
        """
        Initialize the voice recorder with audio parameters.
        
        Args:
            rate: Sample rate (Hz)
            chunk_size: Number of frames per buffer
            channels: Number of channels
            format: Audio format
            silence_threshold: Threshold for silence detection
            silence_duration: Duration of silence to stop recording (seconds)
        """
        self.rate = rate
        self.chunk_size = chunk_size
        self.channels = channels
        self.format = format
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.p = pyaudio.PyAudio()
        self.recording = False
        self.frames = []
        
    def _is_silent(self, audio_data):
        """Detect if audio chunk is silent"""
        # Convert audio data to numpy array
        data = np.frombuffer(audio_data, dtype=np.int16)
        # Check if volume is below threshold
        return np.abs(data).mean() < self.silence_threshold
        
    def start_recording(self):
        """Start recording audio until silence is detected"""
        self.recording = True
        self.frames = []
        
        stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        print("Listening... Speak now (will stop after silence)")
        
        silent_chunks = 0
        silent_chunks_threshold = int(self.silence_duration * self.rate / self.chunk_size)
        
        while self.recording:
            data = stream.read(self.chunk_size)
            self.frames.append(data)
            
            # Check for silence to auto-stop
            if self._is_silent(data):
                silent_chunks += 1
                if silent_chunks >= silent_chunks_threshold:
                    break
            else:
                silent_chunks = 0
        
        stream.stop_stream()
        stream.close()
        
        print("Finished recording")
        return self._save_recording()
        
    def stop_recording(self):
        """Manually stop recording"""
        self.recording = False
        
    def _save_recording(self):
        """Save the recorded audio to a temporary WAV file"""
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_path = temp_file.name
        temp_file.close()
        
        # Write the recorded frames to the temporary file
        with wave.open(temp_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
        
        return temp_path
        
    def __del__(self):
        """Clean up PyAudio resources"""
        self.p.terminate()