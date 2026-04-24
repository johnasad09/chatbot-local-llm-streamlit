import streamlit as st  # Streamlit: turns Python scripts into interactive web apps
import ollama  # Ollama: library to run local LLMs (like Llama) on your machine

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

# The local LLM model to use — must be pulled via `ollama pull llama3.1:8b` first
LLM_MODEL = 'llama3.1:8b'

# The default greeting message shown at the start of every conversation.
# Structured as a chat message dict with a "role" (who's speaking) and "content" (what they said)
GREETINGS = {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}

# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

# Configure the browser tab title and icon for the Streamlit app
st.set_page_config(page_title="AI Assistant", page_icon=":material/smart_toy:")

# Split the top of the page into two columns:
# col1 takes up 85% of the width (for the title), col2 takes 15% (for the Reset button)
col1, col2 = st.columns([0.85, 0.15])

with col1:
    st.title("LLM App based on Local LLM ")  # Large title text
    st.header("(Llama 3.1)")  # Slightly smaller subheading below it

with col2:
    # A "Reset" button in the top-right corner.
    # When clicked: clears chat history back to just the greeting, then reruns the app
    if st.button("Reset", type="primary", width="stretch"):
        st.session_state.messages = [GREETINGS]  # Wipe history
        st.rerun()  # Refresh the page to reflect the reset

# --------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------

# st.session_state persists data across Streamlit reruns (e.g. when user types a message).
# On the very first load, 'messages' won't exist yet — so we initialize it with the greeting.
if 'messages' not in st.session_state:
    st.session_state.messages = [GREETINGS]

# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

# Loop through all messages stored in session state and render them in the chat UI.
# Each message is displayed in a chat bubble styled for its role ("user" or "assistant")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  # Creates a chat bubble (user or assistant style)
        st.markdown(message["content"])  # Renders the message text (supports markdown)

# --------------------------------------------------
# CHAT INPUT & RESPONSE
# --------------------------------------------------

# st.chat_input() shows the message input box at the bottom of the page.
# The walrus operator `:=` assigns the typed text to `prompt` AND checks if it's non-empty.
# This block only runs when the user actually submits a message.
if prompt := st.chat_input("Type your message here..."):

    # --- Store and display the user's message ---
    st.session_state.messages.append({"role": "user", "content": prompt})  # Save to history
    with st.chat_message("user"):
        st.markdown(prompt)  # Show the user's message immediately in the chat

    # --- Generate and stream the assistant's response ---
    with st.chat_message("assistant"):  # Open an assistant chat bubble to stream into
        try:
            # Call the local Ollama model with the full conversation history.
            # Sending all past messages gives the model context for a multi-turn conversation.
            # stream=True means the response comes back chunk by chunk (faster perceived response)
            response = ollama.chat(
                model=LLM_MODEL,
                messages=st.session_state.messages,
                stream=True  # Enable streaming output
            )
            # An empty string to accumulate the full response as chunks arrive
            stream_content = ''


            # A generator function that processes the streamed response chunk by chunk
            def catch_stream(response):
                global stream_content  # refer to the outer stream_content variable (not a local copy)

                for chunk in response:  # response is an iterator — each chunk is one piece of the reply
                    content = chunk['message'][
                        'content']  # OUTPUT: e.g. "Hello" ... "!" ... " How" ... " are" ... " you?"
                    stream_content += content  # accumulate: '' -> 'Hello' -> 'Hello!' -> 'Hello! How' -> ...
                    yield content  # send this chunk out immediately (makes this a generator, not a regular function)


            # This line does NOT run the function yet.
            # It just creates a generator object — the function runs lazily, only when iterated
            stream = catch_stream(response)

            # THIS is what actually runs the generator.
            # st.write_stream() pulls chunks one by one from the generator and displays them live in the UI
            # OUTPUT: text appears word by word in the chat bubble, like a typewriter effect
            st.write_stream(stream)

            # By this point, streaming is fully done and stream_content holds the complete response
            # e.g. stream_content = "Hello! How are you?"
            # We now save it to chat history so it can be included in future API calls as context
            st.session_state.messages.append({"role": "assistant", "content": stream_content})
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# ------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------ #


# ------------------------------------------------------------------------------------ #
#  WAIT AND DISPLAY METHOD
# ------------------------------------------------------------------------------------ #
# if "messages" not in st.session_state:
#     # st.session_state["messages"] = []
#     st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    
# for msg in st.session_state.messages:
#     # with st.chat_message(msg['role']):
#     #     st.markdown(msg['content'])
#     st.chat_message(msg["role"]).write(msg["content"])

# := walrus operator - assigns the user inputs and returns the value at the same time
# if prompt := st.chat_input():
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)

#     # Call Ollama instead of OpenAI
#     response = ollama.chat(
#         model=desired_model,
#         messages=st.session_state.messages)
#     msg = response['message']['content']
    
#     st.session_state.messages.append({"role": "assistant", "content": msg})
#     st.chat_message("assistant").write(msg)
                                   
# ------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------ #
 

# ------------------------------------------------------------------------------------ #
# GENERATING RESPONSE USING STREAMLIT FORM
# ------------------------------------------------------------------------------------ #

# def generate_response(prompt):
#     response = ollama.chat(
#         model=desired_model, messages=[
#             {
#                 'role': 'user',
#                 'content': prompt,
#             },
#         ]
#         )
#     st.info(response['message']['content'])
    

# with st.form("my_form"):
#     text = st.text_area(
#         "Enter text:",
#         "Ask a question and press the Submit button. ",
#     )
#     submitted = st.form_submit_button("submit")
#     if submitted:
#         generate_response(text)

# ------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------ #
