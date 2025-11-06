import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import time

# Load environment variables
load_dotenv()

# Rate limiting variables
if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = 0
if "request_count" not in st.session_state:
    st.session_state.request_count = 0

# Rate limiting configuration (30 requests per minute)
RATE_LIMIT = 30
TIME_WINDOW = 60

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "conversation_count" not in st.session_state:
    st.session_state.conversation_count = 0

# Configure the assistant persona
ASSISTANT_PERSONA = """You are a helpful, friendly, and knowledgeable AI assistant.
Primary goals:
- Answer open-domain questions accurately and concisely.
- Handle casual small talk naturally.
- Ask at most one clarifying question only when essential.
- Be safe, polite, and non-judgmental.

Persona & Tone:
- Warm, calm, and upbeat.
- Use plain language.
- Emojis sparingly (max 1 per short reply, 2 for longer replies).
- Match the user's formality and language (English/Hinglish allowed).

Conversation Rules:
- Greet naturally on first contact. If user shares a name, use it later.
- Keep most answers to 3–7 sentences unless the user asks for detail.
- For lists, prefer short bullet points.
- If you don't know, say so and suggest next steps.
- If the question is ambiguous, ask one crisp clarifier.
- If you make an assumption, state it briefly.

Knowledge & Reasoning:
- Use general knowledge. If external "context" is provided (RAG), rely on it first.
- If context conflicts with prior knowledge, prefer the provided context.
- For math/logic, show key steps briefly and the final answer.
- For code, provide runnable, minimal examples with language-tagged fences.
- Cite sources only if provided. Don't fabricate citations.

Safety:
- Avoid harmful instructions, self-harm facilitation, illegal activity, or personal data extraction.
- For medical, legal, or financial topics: provide general information, not professional advice; encourage consulting a professional when appropriate.
- No NSFW content.

Small Talk & Social:
- Handle greetings, feelings, and light banter naturally.
- Be supportive and positive; don't overuse emojis.
- If the user seems upset, be empathetic and concise.

Formatting:
- Default to clean Markdown: short paragraphs, bullets, and tables when helpful.
- Use code blocks for code.
- Keep tables small and readable.

Clarifying Policy:
- Ask one clarifying question only if the user's goal cannot be met without it. Otherwise, proceed with a sensible assumption and note it briefly.

When Unsure:
- Say "I'm not sure" or "I don't have enough info."
- Offer one or two concrete ways to find the answer or move forward.

RAG Context Handling (if provided):
- Summarize the most relevant snippets in your own words.
- Quote minimally (1–2 lines) only if precision matters.
- If no relevant context found, say so and answer from general knowledge or ask for more info."""

def check_rate_limit():
    """Check if we've exceeded the rate limit"""
    current_time = time.time()
    
    # Reset counter if time window has passed
    if current_time - st.session_state.last_request_time > TIME_WINDOW:
        st.session_state.request_count = 0
        st.session_state.last_request_time = current_time
    
    # Check if we've exceeded the rate limit
    if st.session_state.request_count >= RATE_LIMIT:
        time_to_wait = TIME_WINDOW - (current_time - st.session_state.last_request_time)
        if time_to_wait > 0:
            return False, time_to_wait
    
    # Increment request count
    st.session_state.request_count += 1
    st.session_state.last_request_time = current_time
    return True, 0

def get_assistant_response(messages, api_key):
    """Get response from Gemini API with rate limiting"""
    try:
        # Configure Gemini API with the provided key
        genai.configure(api_key=api_key)
        
        # Check rate limit
        allowed, wait_time = check_rate_limit()
        if not allowed:
            return f"Rate limit exceeded. Please wait {int(wait_time)} seconds before making another request."
        
        # Prepare messages for Gemini API
        # Convert messages to Gemini format
        gemini_messages = []
        for message in messages:
            if message["role"] == "system":
                # Add system message as a user message (Gemini doesn't have system messages)
                gemini_messages.append({"role": "user", "parts": [message["content"]]})
                gemini_messages.append({"role": "model", "parts": ["Understood. I will follow these instructions."]})
            else:
                # Convert role names
                role = "model" if message["role"] == "assistant" else message["role"]
                gemini_messages.append({"role": role, "parts": [message["content"]]})
        
        # Initialize the Gemini model (using a model that's available)
        # Try gemini-2.0-flash first, then fall back to gemini-flash-latest
        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
        except Exception:
            try:
                model = genai.GenerativeModel('gemini-flash-latest')
            except Exception:
                # Last resort fallback
                model = genai.GenerativeModel('gemini-pro-latest')
        
        # Start chat with history
        chat = model.start_chat(history=gemini_messages[:-1])  # Exclude the last message (current prompt)
        
        # Send the last message and get response
        response = chat.send_message(messages[-1]["content"])
        
        return response.text
    except Exception as e:
        # Provide more detailed error handling
        error_msg = str(e)
        if "404" in error_msg and "not found" in error_msg:
            return "Sorry, the Gemini model is not available. This might be due to API changes. Please check your API key and try again later."
        elif "API_KEY_INVALID" in error_msg:
            return "Sorry, your Gemini API key appears to be invalid. Please check your API key."
        else:
            return f"Sorry, I encountered an error: {error_msg}. Please check your Gemini API key and connection."

def log_feedback(message, feedback):
    """Log user feedback to a JSON file"""
    feedback_entry = {
        "timestamp": datetime.now().isoformat(),
        "message": str(message),
        "feedback": feedback
    }
    
    try:
        if os.path.exists("feedback_log.json"):
            with open("feedback_log.json", "r") as f:
                feedback_data = json.load(f)
        else:
            feedback_data = []
            
        feedback_data.append(feedback_entry)
        
        with open("feedback_log.json", "w") as f:
            json.dump(feedback_data, f, indent=2)
    except Exception as e:
        st.warning(f"Could not save feedback: {e}")

# Streamlit UI
st.title("🤖 NLP Chatbot")
st.markdown("Your friendly AI assistant powered by Google Gemini")

# API Key Input
with st.sidebar:
    st.header("API Configuration")
    api_key = st.text_input("Enter your Gemini API Key:", type="password", 
                           value=os.getenv("GEMINI_API_KEY", ""))
    
    if not api_key:
        st.warning("Please enter your Gemini API key to use the chatbot.")
        st.info("Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)")
        st.stop()

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    This chatbot can:
    - Answer questions
    - Help with explanations
    - Assist with coding
    - Engage in casual conversation
    """)
    
    st.header("Settings")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.conversation_count = 0
        st.session_state.last_request_time = 0
        st.session_state.request_count = 0
        st.rerun()
        
    st.header("Feedback")
    st.markdown("How was your experience?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👍 Good"):
            if st.session_state.messages:
                last_message = st.session_state.messages[-1]
                log_feedback(last_message, "good")
                st.success("Thanks for your feedback!")
    with col2:
        if st.button("👎 Needs Improvement"):
            if st.session_state.messages:
                last_message = st.session_state.messages[-1]
                log_feedback(last_message, "needs_improvement")
                st.success("Thanks for your feedback!")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What's on your mind?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.conversation_count += 1
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Get and display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = get_assistant_response(st.session_state.messages, api_key)
        message_placeholder.markdown(full_response)
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# First time greeting
if st.session_state.conversation_count == 0:
    with st.chat_message("assistant"):
        greeting = "hey! 👋 I can help with questions, explain concepts, chat casually, or write/run small code snippets. what are you working on today?"
        st.markdown(greeting)
    st.session_state.messages.append({"role": "assistant", "content": greeting})