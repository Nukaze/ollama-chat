import os
import subprocess
from dotenv import load_dotenv
import argparse

# Load environment variables from .env file if present
load_dotenv()

# Update the policy file with the credentials
def update_policy_file(username, password, policy_path):
    policy_content = f"""
on_http_request:
  - actions:
      - type: basic-auth
        config:
          realm: \"Ollama Access\"
          credentials:
            - {username}:{password}
"""
    with open(policy_path, 'w') as f:
        f.write(policy_content)


def main():
    parser = argparse.ArgumentParser(description="Launch Ollama, ngrok, and optionally Streamlit with basic auth.")
    parser.add_argument("--run-streamlit", default=False, help="Start running Streamlit")
    
    args = parser.parse_args()
    
    
    CREATE_NEW_CONSOLE = subprocess.CREATE_NEW_CONSOLE
    
    TARGET_PORT = 11434
    POLICY_FILE = 'policy_basic_auth.yaml'

    USERNAME = os.getenv('NGROK_BASIC_AUTH_USERNAME')
    PASSWORD = os.getenv('NGROK_BASIC_AUTH_PASSWORD')

    if not USERNAME or not PASSWORD:
        raise ValueError("USERNAME and PASSWORD environment variables must be set.")

    update_policy_file(USERNAME, PASSWORD, POLICY_FILE)
    
    
    try:
      # start Ollama on port 11434
      ollama_cmd = ["ollama", "serve"]
      print("Starting Ollama server")
      subprocess.Popen(
        ollama_cmd, 
        creationflags=CREATE_NEW_CONSOLE
      )
    except Exception as e:
      print(f"Error ollama, {e}")
    


    try:
      # Start ngrok as a subprocess
      # ngrok http 11434 --host-header="localhost:11434" --traffic-policy-file=policy_basic_auth.yaml
      ngrok_cmd = [
          'ngrok', 'http', str(TARGET_PORT),
          f'--host-header=localhost:{TARGET_PORT}',
          f'--traffic-policy-file={POLICY_FILE}'
      ]
      print(f"Starting NGRok service with command: {' '.join(ngrok_cmd)}")
      subprocess.Popen(
        ngrok_cmd,
        creationflags=CREATE_NEW_CONSOLE
      )
    except Exception as e:
      print(f"Error NGRok, {e}")
      
      
    try:
      # Start streamlit run process on local demo not cloud (default --run-streamlit=false)
      if args.run_streamlit:
        streamlit_cmd = [
          "streamlit", "run", "app.py"
        ]
        
        print("Starting Streamlit service with command")
        subprocess.Popen(
          streamlit_cmd,
          creationflags=CREATE_NEW_CONSOLE
        )
      
    except Exception as e:
      print(f"Error Streamlit, {e}")




if __name__ == "__main__":
    main()