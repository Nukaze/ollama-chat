import requests
import json

class OllamaClient:
    def __init__(self, base_url=None):
        # Get base_url from Streamlit secrets, fallback to localhost if not set
        self.base_url = base_url or st.secrets.get("OLLAMA_BASE_URL", "http://localhost:11434")
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


    # TODO streaming result
    def generate_response(self, model, prompt, system_prompt=None, temperature=0.5, stream=False):
        """Generate a response from the specified model"""
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": stream,
                "temperature": temperature
            }
            
            if system_prompt:
                payload["system"] = system_prompt

            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            
            if response.status_code == 200:
                # success
                return response.json().get("response", "Error: No response generated")
        
            return f"Error: {response.status_code} - {response.text}"
        
        except Exception as e:
            return f"Error: {str(e)}" 