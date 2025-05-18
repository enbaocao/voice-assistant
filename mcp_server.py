#!/usr/bin/env python3
"""
Simple MCP server for file operations using FastMCP.

Run this in a separate terminal to provide an MCP endpoint for the voice assistant.
"""

from fastmcp import FastMCP
import os
import subprocess
import sys

# Directory where file operations are allowed
WORKSPACE_DIR = os.getcwd()

app = FastMCP(name="file-operations")

@app.tool("list_files")
def list_files(path="."):
    """List files in the specified directory."""
    target_path = os.path.abspath(os.path.join(WORKSPACE_DIR, path))
    
    # Security check - ensure we're not escaping the workspace
    if not target_path.startswith(WORKSPACE_DIR):
        return {"error": "Cannot access directories outside the workspace"}
    
    try:
        files = os.listdir(target_path)
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}

@app.tool("read_file")
def read_file(path):
    """Read the contents of a file."""
    target_path = os.path.abspath(os.path.join(WORKSPACE_DIR, path))
    
    # Security check
    if not target_path.startswith(WORKSPACE_DIR):
        return {"error": "Cannot access files outside the workspace"}
    
    try:
        with open(target_path, 'r') as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}

@app.tool("write_file")
def write_file(path, content):
    """Create or update a file with the specified content."""
    target_path = os.path.abspath(os.path.join(WORKSPACE_DIR, path))
    
    # Security check
    if not target_path.startswith(WORKSPACE_DIR):
        return {"error": "Cannot access files outside the workspace"}
    
    try:
        with open(target_path, 'w') as f:
            f.write(content)
        return {"status": "success", "message": f"File '{path}' written successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.tool("delete_file")
def delete_file(path):
    """Delete a file."""
    target_path = os.path.abspath(os.path.join(WORKSPACE_DIR, path))
    
    # Security check
    if not target_path.startswith(WORKSPACE_DIR):
        return {"error": "Cannot access files outside the workspace"}
    
    try:
        os.remove(target_path)
        return {"status": "success", "message": f"File '{path}' deleted successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.tool("run_command")
def run_command(command):
    """Run a shell command (limited to safe operations)."""
    # List of allowed command prefixes for safety
    allowed_prefixes = ["echo", "ls", "cat", "mkdir", "pwd"]
    
    # Simple security check - only allow specific commands
    command_parts = command.split()
    if not command_parts or command_parts[0] not in allowed_prefixes:
        return {
            "error": f"Command not allowed. Allowed commands start with: {', '.join(allowed_prefixes)}"
        }
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=WORKSPACE_DIR
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print(f"Starting MCP server for file operations in {WORKSPACE_DIR}")
    # Run with default transport (STDIO)
    app.run()