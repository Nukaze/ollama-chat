import streamlit as st

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="Ollama Chat",
    page_icon="🤖",
    layout="wide"
)

from ollama_client import OllamaClient
import time

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "ollama_client" not in st.session_state:
    # Try to get Ollama URL from Streamlit secrets (for cloud deployment)
    ollama_url = None
    try:
        ollama_url = st.secrets["OLLAMA_BASE_URL"]
        print("ollama url", ollama_url)
        st.session_state.ollama_client = OllamaClient(base_url=ollama_url)
    except:
        # If no secret is set, will fallback to environment variable or localhost
        pass
    

# Custom CSS
st.markdown("""
<style>
    .stTextInput>div>div>input {
        background-color: #f0f2f6;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2b313e;
        color: white;
    }
    .chat-message.assistant {
        background-color: #f0f2f6;
    }
    .chat-message .avatar {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🤖 Ollama Chat Settings")
    
    # Model selection
    models = st.session_state.ollama_client.get_available_models()
    # TODO: suggest url https://ollama.com/library
    selected_model = st.selectbox(
        "Select Model",
        options=[model["name"] for model in models] if models else ["gemma3:latest"],
        index=0
    )
    
    # Temperature slider
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.1
    )
    
    # System prompt
    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful AI assistant.",
        height=100
    )
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.title("💬 Ollama Chat")

# Display chat messages
for message in st.session_state.messages:
    with st.container():
        st.markdown(f"""
        <div class="chat-message {message['role']}">
            <div style="display: flex; align-items: center;">
                <span style="font-weight: bold;">{'🤖' if message['role'] == 'assistant' else '👤'}</span>
                <span style="margin-left: 0.5rem;">{message['role'].title()}</span>
            </div>
            <div style="margin-top: 0.5rem;">{message['content']}</div>
        </div>
        """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("What's on your mind?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.container():
        st.markdown(f"""
        <div class="chat-message user">
            <div style="display: flex; align-items: center;">
                <span style="font-weight: bold;">👤</span>
                <span style="margin-left: 0.5rem;">User</span>
            </div>
            <div style="margin-top: 0.5rem;">{prompt}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Generate response
    with st.spinner("Thinking..."):
        # Create an empty placeholder for the streaming response
        response_placeholder = st.empty()
        full_response = ""
        
        # Get streaming response
        for response_chunk in st.session_state.ollama_client.generate_response(
            model=selected_model,
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature
        ):
            full_response += response_chunk
            # Update the response in real-time
            response_placeholder.markdown(f"""
            <div class="chat-message assistant">
                <div style="display: flex; align-items: center;">
                    <span style="font-weight: bold;">🤖</span>
                    <span style="margin-left: 0.5rem;">Assistant</span>
                </div>
                <div style="margin-top: 0.5rem;">{full_response}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Add the complete response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response}) 