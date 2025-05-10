# Voice Assistant

A voice-controlled assistant that can perform tasks based on your spoken commands. This project allows you to record your voice, convert it to text, and execute commands without using a keyboard.

## Features

- Voice recording with automatic silence detection
- Speech-to-text conversion using Whisper models (local, no API costs)
- Execute basic filesystem operations (create/delete files and folders)
- Set up new projects (Next.js, Flask)
- Expandable to integrate with any MCP-compatible LLM for more complex tasks

## Requirements

- Python 3.8+
- PyAudio and related audio libraries
- Whisper speech recognition model
- Various Python packages (see Installation section)
- Node.js & npm (for Next.js project initialization)

## Installation

1. Clone this repository
2. Set up a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pyaudio numpy sounddevice soundfile pydub faster-whisper requests transformers
```

3. For advanced LLM capabilities, set up a local MCP-compatible LLM server. Options include:
   - [Ollama](https://ollama.ai/)
   - [LocalAI](https://github.com/go-skynet/LocalAI)
   - [llama.cpp server](https://github.com/ggerganov/llama.cpp)

## Usage

Run the voice assistant:

```bash
python voice_assistant.py
```

For more options:

```bash
python voice_assistant.py --help
```

### Configuration Options

- `--api-endpoint`: URL for an MCP-compatible LLM API server (optional)
- `--whisper-model`: Whisper model size ("tiny", "base", "small", "medium", "large")
- `--device`: Device to run models on ("cpu" or "cuda")

Example with custom options:

```bash
python voice_assistant.py --whisper-model base --api-endpoint http://localhost:11434/v1/chat/completions
```

### Example Voice Commands

- "Create a new folder called project_data"
- "Delete the file named temp.txt"
- "Clear the folder named cache"
- "Set up a new Next.js project named my-website"
- "Set up a new Flask project called api-server"

## How It Works

1. The assistant records your voice until it detects a pause (silence)
2. The audio is converted to text using the Whisper model
3. The command is processed:
   - For simple file/folder operations, the command is parsed and executed directly
   - For project setup, the assistant identifies project type and name, then uses appropriate tools
   - For complex commands, the assistant can use an MCP-compatible LLM (if configured)

## Project Structure

```
voice-assistant/
├── src/
│   ├── audio/
│   │   ├── recorder.py       # Audio recording functionality
│   │   └── transcriber.py    # Speech-to-text conversion
│   ├── cli/
│   │   └── main.py           # Command-line interface
│   └── llm/
│       ├── executor.py       # Processes commands via direct execution or LLM
│       └── project_initializer.py  # Sets up different project types
└── voice_assistant.py        # Main entry point
```

## Expanding the Assistant

To expand the assistant's capabilities:

1. Add new command patterns in `executor.py`
2. Add new project types in `project_initializer.py`
3. Connect to a more powerful LLM via the MCP protocol

## License

[MIT License](LICENSE)
