# Voice Assistant with MCP

A simple macOS application that:
1. Records audio from your microphone
2. Converts it to text using OpenAI's Whisper
3. Sends the text to an MCP server to execute file operations

## Prerequisites

- macOS
- [Homebrew](https://brew.sh/)
- Python 3.11+ 
- ffmpeg

## Setup

1. Install required system dependencies:

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and ffmpeg
brew install python@3.11 ffmpeg
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:

```bash
pip install sounddevice soundfile openai-whisper "mcp[cli]" fastmcp
```

4. Install an MCP server (choose ONE):

```bash
# Option 1: Mac Shell - full shell + file operations
npx @michaellatman/mcp-get@latest install cfdude-mac-shell

# Option 2: Text Editor - line-oriented editor
pip install mcp-text-editor
```

## Usage

1. In one terminal, start the MCP server (use the appropriate command for your chosen server)

2. In another terminal, run the voice assistant:

```bash
python record_and_edit.py
```

3. Speak your command (example: "create a file named hello.txt with the contents Hello World")

## Security Considerations

- The application is configured to operate within the current directory only
- Review the transcribed text before sending to MCP
- Configure your MCP server's security policy to restrict dangerous operations