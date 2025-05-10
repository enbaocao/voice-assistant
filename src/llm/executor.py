import os
import json
import subprocess
from pathlib import Path
import tempfile
import requests

class LLMExecutor:
    def __init__(self, model_name=None, api_endpoint=None):
        """
        Initialize the LLM executor that will process commands via MCP.
        
        Args:
            model_name: Name of the local model to use, if directly loading a model
            api_endpoint: API endpoint if using a remote/local MCP server
        """
        self.model_name = model_name
        self.api_endpoint = api_endpoint
        
    def process_command(self, command_text):
        """
        Process the command text using a local LLM through MCP.
        
        Args:
            command_text: The text of the command to process
            
        Returns:
            Response from the model and/or executed command result
        """
        # Determine if this is a system command that we should execute directly
        if self._is_system_command(command_text):
            return self._execute_system_command(command_text)
        
        # Otherwise, use an LLM to process the command
        return self._query_llm(command_text)
    
    def _is_system_command(self, command_text):
        """Check if the command text appears to be a direct system command"""
        system_command_prefixes = [
            "create folder", "make folder", "create directory", 
            "delete folder", "remove folder", "clear folder",
            "create file", "make file", "delete file", "remove file",
        ]
        
        return any(command_text.lower().startswith(prefix) for prefix in system_command_prefixes)
    
    def _execute_system_command(self, command_text):
        """Execute a system command based on the command text"""
        cmd = command_text.lower()
        response = "Command executed."
        
        try:
            # Handle folder creation
            if "create folder" in cmd or "make folder" in cmd or "create directory" in cmd:
                # Extract folder name - simple parsing
                parts = cmd.split("called" if "called" in cmd else "named")
                if len(parts) > 1:
                    folder_name = parts[1].strip().strip('"\'')
                    os.makedirs(folder_name, exist_ok=True)
                    response = f"Created folder: {folder_name}"
                else:
                    return "Could not understand folder name"
            
            # Handle folder deletion
            elif "delete folder" in cmd or "remove folder" in cmd:
                parts = cmd.split("called" if "called" in cmd else "named")
                if len(parts) > 1:
                    folder_name = parts[1].strip().strip('"\'')
                    os.rmdir(folder_name)  # This will only work if the folder is empty
                    response = f"Deleted folder: {folder_name}"
                else:
                    return "Could not understand folder name"
            
            # Handle clearing a folder
            elif "clear folder" in cmd:
                parts = cmd.split("called" if "called" in cmd else "named")
                if len(parts) > 1:
                    folder_name = parts[1].strip().strip('"\'')
                    for item in os.listdir(folder_name):
                        item_path = os.path.join(folder_name, item)
                        if os.path.isfile(item_path):
                            os.remove(item_path)
                    response = f"Cleared all files in folder: {folder_name}"
                else:
                    return "Could not understand folder name"
            
            # Handle file creation
            elif "create file" in cmd or "make file" in cmd:
                # This is a simplistic approach - a real implementation would be more robust
                parts = cmd.split("called" if "called" in cmd else "named")
                if len(parts) > 1:
                    file_name = parts[1].strip().strip('"\'')
                    with open(file_name, 'w') as f:
                        # If user specifies content, include it
                        if "with content" in cmd:
                            content_parts = cmd.split("with content")
                            if len(content_parts) > 1:
                                content = content_parts[1].strip().strip('"\'')
                                f.write(content)
                    response = f"Created file: {file_name}"
                else:
                    return "Could not understand file name"
            
            # Handle file deletion
            elif "delete file" in cmd or "remove file" in cmd:
                parts = cmd.split("called" if "called" in cmd else "named")
                if len(parts) > 1:
                    file_name = parts[1].strip().strip('"\'')
                    os.remove(file_name)
                    response = f"Deleted file: {file_name}"
                else:
                    return "Could not understand file name"
                    
        except Exception as e:
            response = f"Error executing command: {str(e)}"
            
        return response
    
    def _query_llm(self, command_text):
        """
        Query the LLM with the given command text through MCP.
        
        In a production system, this would connect to a running MCP server,
        but for demonstration we'll use a simplified implementation.
        """
        # For real implementation, this would use MCP protocol to communicate with the LLM
        if self.api_endpoint:
            try:
                # Sample API call to an MCP-compatible server
                payload = {
                    "messages": [
                        {"role": "system", "content": "You are a helpful voice assistant that executes user commands. Convert voice commands into actions."},
                        {"role": "user", "content": command_text}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 500
                }
                
                headers = {"Content-Type": "application/json"}
                response = requests.post(self.api_endpoint, headers=headers, json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("choices", [{}])[0].get("message", {}).get("content", "No response")
                else:
                    return f"Error: API returned status code {response.status_code}"
            
            except Exception as e:
                return f"Error querying LLM: {str(e)}"
        
        # If no API endpoint is provided, give instructions on how to set up
        else:
            return (
                "To use LLM processing, please set up a local MCP-compatible server and provide the API endpoint. "
                "For project setup actions like creating Next.js or Flask projects, you need to configure an LLM. "
                f"Command received: {command_text}"
            )