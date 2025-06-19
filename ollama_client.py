import requests
import json
import os
import streamlit as st
from dotenv import load_dotenv

class OllamaClient:
    def __init__(self, base_url=None):
        # Try to get base_url in following order:
        # 1. Passed parameter
        # 2. Environment variable (for local development)
        # 3. Default localhost
        if base_url:
            self.base_url = base_url
        else:
            # Load environment variables from .env file (local development)
            load_dotenv()
            self.base_url = st.secrets.get("OLLAMA_BASE_URL", "http://localhost:11434")
        
        self.models = self.get_available_models()


    def get_available_models(self):
        """Get list of available models from Ollama"""
        try:
            # http://localhost:11434/api/tags
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                return response.json().get("models", [])
            return []
        except Exception as e:
            print(f"Error fetching models: {e}")
            return []


    def generate_response(self, model, prompt, system_prompt=None, temperature=0.5, stream=True):
        """Generate a response from the specified model with streaming support"""
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": stream,
                "temperature": temperature,
                "options": {
                    "num_gpu": 99,  # Use all available GPUs
                    "num_thread": 8  # Fallback to CPU threads if no GPU
                }
            }
            
            if system_prompt:
                payload["system"] = system_prompt

            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                stream=stream
            )
            
            if not stream:
                if response.status_code == 200:
                    return response.json().get("response", "Error: No response generated")
                return f"Error: {response.status_code} - {response.text}"
            
            # Handle streaming response
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        try:
                            json_response = json.loads(line)
                            if "response" in json_response:
                                yield json_response["response"]
                        except json.JSONDecodeError:
                            continue
            else:
                yield f"Error: {response.status_code} - {response.text}"
        
        except Exception as e:
            yield f"Error: {str(e)}" 