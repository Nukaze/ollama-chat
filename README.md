# Ollama Chat

A modern Streamlit-based chat interface for interacting with Ollama LLMs.

## Features

- Clean and modern chat interface
- Support for multiple Ollama models
- Adjustable temperature settings
- Custom system prompts
- Chat history
- Responsive design

## Prerequisites

- Python 3.8 or higher
- Ollama installed and running locally (https://ollama.ai/)

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure Ollama is running on your system (default: http://localhost:11434)

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. In the sidebar:
   - Select your preferred Ollama model
   - Adjust the temperature setting
   - Customize the system prompt if desired

4. Start chatting with the AI!

## Configuration

The application connects to Ollama at `http://localhost:11434` by default. If your Ollama instance is running on a different host or port, you can modify the `base_url` parameter in the `OllamaClient` class initialization.

## License

MIT License 