import streamlit as st
import google.generativeai as genai
from config import BASE_PROMPT

# Configure Google Gemini API using Streamlit secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Initialize flag for first interaction
if "first_interaction" not in st.session_state:
    st.session_state.first_interaction = True

def chat_bot():
    # Set page title and header
    st.title("Alzheimer's and Memory Health Assistant")
    st.subheader("Ask me questions about Alzheimer's disease, memory issues, and mental health")
    
    # Store LLM generated responses
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm your Alzheimer's and memory health assistant. I can answer questions about Alzheimer's disease, dementia, memory issues, and related mental health topics. How may I help you today?"}]
    
    # Initialize Gemini model
    if "model" not in st.session_state:
        st.session_state.model = genai.GenerativeModel('gemini-pro')
    
    # Initialize Gemini chat
    if "chat" not in st.session_state:
        st.session_state.chat = st.session_state.model.start_chat(history=[])

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Function for generating LLM response
    def generate_response(prompt_input):
        # Create a system prompt that focuses responses on Alzheimer's and related topics
        if st.session_state.first_interaction:
            # For the first interaction, include the base prompt to set context
            system_prompt = f"{BASE_PROMPT} You are an assistant specialized in Alzheimer's disease, dementia, memory loss, cognitive decline, and related mental health issues. Only answer questions related to these topics. If asked about unrelated topics, politely redirect the conversation back to Alzheimer's disease, memory health, cognitive issues, or mental health."
            st.session_state.first_interaction = False
            
            # Add the system prompt to the chat history
            st.session_state.chat = st.session_state.model.start_chat(history=[
                {"role": "user", "parts": [system_prompt]},
                {"role": "model", "parts": ["I understand. I'll focus on providing helpful information about Alzheimer's disease, memory issues, cognitive health, and related mental health topics."]}
            ])
        
        # Evaluate if the question is on topic
        topic_check = st.session_state.model.generate_content(
            f"Determine if this question is related to Alzheimer's disease, dementia, memory issues, cognitive health, or mental health: '{prompt_input}'. Answer only with 'yes' or 'no'."
        )
        
        is_on_topic = "yes" in topic_check.text.lower()
        
        if is_on_topic:
            # Send the prompt to Gemini and get response
            response = st.session_state.chat.send_message(prompt_input)
            return response.text
        else:
            return "I'm specialized in answering questions about Alzheimer's disease, dementia, memory issues, cognitive health, and related mental health topics. Could you please ask me something related to these areas instead?"

    # User-provided prompt
    if prompt := st.chat_input("Ask about Alzheimer's, memory issues, or mental health..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
    
    # Generate a new response if last message is not from assistant
    if st.session_state.messages and st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt) 
                st.write(response) 
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)

# Main app
def main():
    st.set_page_config(
        page_title="Alzheimer's Health Assistant",
        page_icon="🧠",
    )
    
    # Sidebar with info
    with st.sidebar:
        st.markdown("## About")
        st.markdown("This assistant provides information about Alzheimer's disease, dementia, memory issues, and related mental health topics.")
        st.markdown("### Topics You Can Ask About:")
        st.markdown("- Alzheimer's disease symptoms and progression")
        st.markdown("- Memory loss and forgetfulness")
        st.markdown("- Dementia types and differences")
        st.markdown("- Caregiving tips and resources")
        st.markdown("- Latest research and treatments")
        st.markdown("- Cognitive health and prevention")
    
    # Run the chatbot
    chat_bot()

if __name__ == "__main__":
    main()
