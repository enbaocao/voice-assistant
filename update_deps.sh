#!/bin/bash

# Update pip
pip install --upgrade pip

# Install or update FastMCP with all extras
pip install "fastmcp[all]" --upgrade

# Alternative approach with specific dependencies if needed
# pip install fastmcp uvicorn httpx --upgrade
