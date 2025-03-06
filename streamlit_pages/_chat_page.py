import streamlit as st
import time
import google.generativeai as genai

def setup_page():
    
    # Add custom CSS for better appearance
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #4527A0;
            text-align: center;
            margin-bottom: 1rem;
        }
        .subheader {
            font-size: 1.2rem;
            color: #666;
            text-align: center;
            margin-bottom: 2rem;
        }
        .disclaimer {
            background-color: #FFF8E1;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 2rem;
            font-size: 0.9rem;
        }
        .chat-container {
            border-radius: 10px;
            border: 1px solid #444;
            padding: 20px;
            margin-bottom: 20px;
            background-color: #000000;
            color: #ffffff;
        }
        /* Style for messages within the chat container */
        .chat-container .st-emotion-cache-ue6h4q {
            background-color: #000000 !important;
        }
        .chat-container .st-emotion-cache-1cypcdb {
            background-color: #1E1E1E !important; 
            color: #ffffff !important;
        }
        /* Override the default message styling */
        .st-chat-message {
            background-color: #000000 !important;
        }
        .st-chat-message .message-container {
            background-color: #1E1E1E !important;
            color: #ffffff !important;
        }
        /* User message bubbles */
        .st-emotion-cache-5j5imc {
            background-color: #333333 !important;
            color: #ffffff !important;
        }
        /* Assistant message bubbles */
        .st-emotion-cache-l9bjmx {
            background-color: #202020 !important;
            color: #ffffff !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Header section
    st.markdown("<h1 class='main-header'>Alzheimer's Awareness Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subheader'>Ask questions about memory concerns, cognitive changes, or dementia symptoms</p>", unsafe_allow_html=True)

    # Medical disclaimer
    with st.expander("⚕️ Important Medical Disclaimer", expanded=True):
        st.markdown("""
        This tool is for informational purposes only and not a substitute for professional medical advice. 
        If you're experiencing cognitive symptoms or are concerned about Alzheimer's disease, please consult a healthcare provider.
        This AI assistant cannot diagnose medical conditions.
        """)

def setup_sidebar():
    """Configure sidebar with information"""
    with st.sidebar:
        st.header("About This Tool")
        st.write("""
        This assistant provides information about:
        - Early signs of Alzheimer's disease
        - Differences between normal aging and dementia
        - When to seek medical attention
        - Support resources for patients and caregivers
        - Latest research in Alzheimer's treatment
        """)
        
        st.header("Common Warning Signs")
        st.write("""
        • Memory loss disrupting daily life
        • Challenges in planning or problem solving
        • Difficulty completing familiar tasks
        • Confusion with time or place
        • Trouble understanding visual images
        • New problems with words or speaking
        • Misplacing things and losing the ability to retrace steps
        • Decreased or poor judgment
        • Withdrawal from work or social activities
        • Changes in mood and personality
        """)

def configure_ai():
    """Configure Gemini API and return model and configuration status"""
    try:
        # Get API key from environment variable
        api_key = st.secrets["GEMINI_API_KEY"]
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            is_configured = True
        else:
            # Fallback message - this will only be visible to developers, not end users
            st.sidebar.info("Note to developer: Set the GEMINI_API_KEY environment variable")
            is_configured = False
            model = None
    except Exception as e:
        st.sidebar.error(f"Error initializing AI assistant: {str(e)}")
        is_configured = False
        model = None
    
    return model, is_configured

def display_chat_history():
    """Display the chat history"""
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    st.markdown("</div>", unsafe_allow_html=True)

def display_quick_questions():
    """Display buttons for common questions"""
    st.subheader("Common Questions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("What are early signs of Alzheimer's?"):
            st.session_state.messages.append({"role": "user", "content": "What are the early signs of Alzheimer's disease?"})
            st.rerun()
        if st.button("Is forgetfulness normal aging?"):
            st.session_state.messages.append({"role": "user", "content": "Is occasional forgetfulness a normal part of aging or a sign of Alzheimer's?"})
            st.rerun()

    with col2:
        if st.button("When should I see a doctor?"):
            st.session_state.messages.append({"role": "user", "content": "When should someone with memory problems see a doctor?"})
            st.rerun()
        if st.button("How is Alzheimer's diagnosed?"):
            st.session_state.messages.append({"role": "user", "content": "How is Alzheimer's disease diagnosed?"})
            st.rerun()

def chat_bot():
    """Main chatbot functionality"""
    # Initialize chat history if not exists
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello, I'm your Alzheimer's awareness assistant. I can provide information about memory concerns, cognitive changes, and dementia. How can I help you today?"}
        ]
    
    # Set up the page and sidebar
    setup_page()
    setup_sidebar()
    
    # Configure AI model
    model, is_configured = configure_ai()
    
    # Display existing chat history
    display_chat_history()
    
    # Alzheimer's and dementia context for the model
    MEDICAL_CONTEXT = """
    You are an Alzheimer's disease awareness assistant designed to provide helpful information about memory concerns, 
    cognitive changes, and dementia symptoms. Follow these guidelines:
    1. IMPORTANT: You are NOT a diagnostic tool. Always clarify that only qualified healthcare professionals can 
       diagnose Alzheimer's disease or other forms of dementia. Include this disclaimer when appropriate.
    2. Provide accurate, evidence-based information about:
       - Early warning signs of Alzheimer's disease and other dementias
       - Differences between normal aging and concerning cognitive changes
       - When someone should seek medical attention
       - The diagnostic process for Alzheimer's disease
       - Current treatment approaches and research
       - Resources for patients and caregivers
    3. For questions about specific symptoms:
       - Be empathetic and informative
       - Explain which symptoms warrant medical attention
       - Never attempt to diagnose or rule out medical conditions
       - When in doubt, recommend consulting a healthcare provider
    4. Use clear, empathetic language appropriate for the general public
       - Avoid excessive medical jargon
       - Be sensitive to the emotional nature of memory concerns
    5. If asked about a medical emergency or severe symptoms, always advise seeking immediate medical attention
    6. Focus your responses on information related to Alzheimer's disease, dementia, memory concerns, and brain health.
       If asked questions outside this scope, gently redirect to your area of focus.
    Respond in a helpful, accurate, and compassionate manner.
    """
    
    # Chat input
    if prompt := st.chat_input("Ask about memory concerns, Alzheimer's disease, or dementia..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        if is_configured:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                try:
                    # Show a spinner while generating response
                    with st.spinner("Thinking..."):
                        response = model.generate_content(MEDICAL_CONTEXT + "\n\nUser question: " + prompt)
                    
                    # Simulate typewriter effect
                    if hasattr(response, 'text'):
                        response_text = response.text
                        for chunk in response_text.split():
                            full_response += chunk + " "
                            time.sleep(0.02)  # Adjust speed as needed
                            message_placeholder.markdown(full_response + "▌")
                        
                        message_placeholder.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    else:
                        message_placeholder.markdown("I apologize, but I couldn't generate a response. Please try rephrasing your question.")
                except Exception as e:
                    message_placeholder.markdown(f"I'm sorry, I encountered an error while processing your request. Please try again later. Error details: {str(e)}")
        else:
            with st.chat_message("assistant"):
                st.markdown("I apologize, but the AI assistant is currently unavailable. Please try again later.")
    
    # Footer
    st.markdown("---")
    st.markdown("© 2025 Alzheimer's Awareness Assistant | This is not a diagnostic tool | Always consult a healthcare professional")
    
    # Display quick question buttons
    display_quick_questions()

# Main execution
if __name__ == "__main__":
    chat_bot()
