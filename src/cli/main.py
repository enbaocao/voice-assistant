import os
import sys
import argparse
from pathlib import Path

# Add the parent directory to the system path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules
from src.audio.recorder import VoiceRecorder
from src.audio.transcriber import SpeechToText
from src.llm.executor import LLMExecutor
from src.llm.project_initializer import ProjectInitializer

def main():
    parser = argparse.ArgumentParser(description="Voice assistant for executing commands")
    parser.add_argument("--api-endpoint", type=str, help="API endpoint for the MCP-compatible LLM server")
    parser.add_argument("--whisper-model", type=str, default="tiny", 
                        choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper model size to use for speech recognition")
    parser.add_argument("--device", type=str, default="cpu", choices=["cpu", "cuda"],
                        help="Device to run Whisper model on")
    parser.add_argument("--manual-stop", action="store_true", 
                        help="Use manual stop mode (press Enter to stop recording) instead of automatic silence detection")
    
    args = parser.parse_args()
    
    print("Initializing voice assistant...")
    
    # Initialize the components
    recorder = VoiceRecorder()
    transcriber = SpeechToText(model_size=args.whisper_model, device=args.device)
    executor = LLMExecutor(api_endpoint=args.api_endpoint)
    project_initializer = ProjectInitializer()
    
    print("\nVoice Assistant is ready!")
    print("You can say commands like:")
    print("- 'Create a new folder called project_data'")
    print("- 'Set up a new Next.js project named my-app'")
    print("- 'Clear the folder named temp'")
    
    if args.manual_stop:
        print("\nUsing MANUAL STOP mode: Press Enter AGAIN when you're done speaking")
    else:
        print("\nUsing automatic silence detection: Recording will stop after a brief pause")
        
    print("\nPress Ctrl+C to quit at any time.\n")
    
    try:
        while True:
            print("\nPress Enter to start recording a command...")
            input()
            
            # Record audio (using manual or automatic mode)
            if args.manual_stop:
                # Start recording in a non-blocking way
                recorder.start_recording(auto_detect_silence=False)
                
                # Wait for user to press Enter to stop recording
                input("Recording... Press Enter when you're done speaking\n")
                
                # Manually stop the recording
                audio_path = recorder.stop_recording()
            else:
                # Use automatic silence detection
                audio_path = recorder.start_recording(auto_detect_silence=True)
            
            # Transcribe audio to text
            print("Transcribing...")
            command_text = transcriber.transcribe(audio_path)
            print(f"You said: {command_text}")
            
            # Process special project initialization commands
            if "set up" in command_text.lower() and ("next.js" in command_text.lower() or "flask" in command_text.lower()):
                project_type = "nextjs" if "next.js" in command_text.lower() else "flask"
                
                # Extract project name - simple parsing
                project_name = "myapp"  # Default name
                if "named" in command_text.lower():
                    parts = command_text.lower().split("named")
                    if len(parts) > 1:
                        project_name = parts[1].strip().strip('"\'')
                elif "called" in command_text.lower():
                    parts = command_text.lower().split("called")
                    if len(parts) > 1:
                        project_name = parts[1].strip().strip('"\'')
                
                print(f"Initializing {project_type} project: {project_name}")
                result = project_initializer.initialize_project(project_type, project_name)
                print(result)
            else:
                # Process the command with the LLM
                print("Processing command...")
                result = executor.process_command(command_text)
                print(f"Result: {result}")
            
            # Clean up the temporary audio file
            try:
                os.remove(audio_path)
            except:
                pass
                
    except KeyboardInterrupt:
        print("\nExiting voice assistant. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()