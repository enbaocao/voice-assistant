import os
import subprocess
import json
from pathlib import Path

class ProjectInitializer:
    """
    Handles project initialization for different types of projects.
    """
    
    def __init__(self):
        """Initialize the project initializer."""
        pass
        
    def initialize_project(self, project_type, project_name, target_dir=None):
        """
        Initialize a new project of the specified type.
        
        Args:
            project_type: Type of project to initialize (e.g., 'nextjs', 'flask')
            project_name: Name of the project
            target_dir: Target directory for the project (default: current directory)
            
        Returns:
            Result message
        """
        if target_dir is None:
            target_dir = os.getcwd()
            
        project_path = os.path.join(target_dir, project_name)
        
        # Select appropriate initialization method based on project type
        if project_type.lower() == 'nextjs':
            return self._init_nextjs(project_name, project_path)
        elif project_type.lower() == 'flask':
            return self._init_flask(project_name, project_path)
        else:
            return f"Unsupported project type: {project_type}"
    
    def _init_nextjs(self, project_name, project_path):
        """Initialize a Next.js project."""
        try:
            # Check if npx is available
            try:
                subprocess.run(['which', 'npx'], check=True, capture_output=True)
            except subprocess.CalledProcessError:
                return "npx not found. Please install Node.js and npm first."
            
            # Create the project using create-next-app
            subprocess.run(
                ['npx', 'create-next-app@latest', project_name, '--use-npm'],
                check=True
            )
            
            return f"Successfully initialized Next.js project: {project_name}"
        except subprocess.CalledProcessError as e:
            return f"Error initializing Next.js project: {str(e)}"
    
    def _init_flask(self, project_name, project_path):
        """Initialize a Flask project with a basic structure."""
        try:
            # Create project directory
            os.makedirs(project_path, exist_ok=True)
            
            # Create basic Flask project structure
            # app.py
            with open(os.path.join(project_path, 'app.py'), 'w') as f:
                f.write("""from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
""")
            
            # requirements.txt
            with open(os.path.join(project_path, 'requirements.txt'), 'w') as f:
                f.write("Flask==2.3.3\n")
            
            # Create templates directory
            templates_dir = os.path.join(project_path, 'templates')
            os.makedirs(templates_dir, exist_ok=True)
            
            # Create static directory
            static_dir = os.path.join(project_path, 'static')
            os.makedirs(static_dir, exist_ok=True)
            os.makedirs(os.path.join(static_dir, 'css'), exist_ok=True)
            os.makedirs(os.path.join(static_dir, 'js'), exist_ok=True)
            
            # Create a basic index.html template
            with open(os.path.join(templates_dir, 'index.html'), 'w') as f:
                f.write("""<!DOCTYPE html>
<html>
<head>
    <title>{{ title|default('Flask App') }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <h1>Welcome to Flask!</h1>
    <p>This is a basic Flask application.</p>
    
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
""")
            
            # Create basic CSS file
            with open(os.path.join(static_dir, 'css', 'style.css'), 'w') as f:
                f.write("""body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    line-height: 1.6;
}

h1 {
    color: #333;
}
""")
            
            # Create basic JS file
            with open(os.path.join(static_dir, 'js', 'main.js'), 'w') as f:
                f.write("""// Main JavaScript file
console.log('Flask app loaded');
""")
            
            # Create a basic README
            with open(os.path.join(project_path, 'README.md'), 'w') as f:
                f.write(f"""# {project_name}

A Flask web application.

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows: `venv\\Scripts\\activate`
   - On macOS/Linux: `source venv/bin/activate`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open http://127.0.0.1:5000/ in your browser.
""")
            
            return f"Successfully initialized Flask project: {project_name}"
        except Exception as e:
            return f"Error initializing Flask project: {str(e)}"