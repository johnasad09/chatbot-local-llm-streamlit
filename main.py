# Download LLM from via Ollama, this code uses Llama 3.1:8b

import streamlit as st
import ollama

# set the model
LLM_MODEL = 'llama3.1:8b'

GREETINGS = {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}

st.set_page_config(page_title="AI Assistant", page_icon=":material/smart_toy:")

col1, col2 = st.columns([0.85, 0.15])
with col1: 
    st.title("LLM App based on Local LLM ")
    st.header("(Llama 3.1)")

# RESET BUTTON
with col2: 
    if st.button("Reset", type="primary", width="stretch"):
        st.session_state.messages = [GREETINGS]
        st.rerun()
            
# ------------------------------------------------------------------------------------ #
# REAL TIME STREAMING (TYPING EFFECT) METHOD
# ------------------------------------------------------------------------------------ #
# Initialization
if 'messages' not in st.session_state:
    st.session_state.messages = [GREETINGS]

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Type your message here..."):

    # Append and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Model Response with Streaming 
    with st.chat_message("assistant"):      
        try:
            response = ollama.chat(
                model=LLM_MODEL,
                messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True)
            
            stream_content = ''
            def catch_stream(response):
                global stream_content
                for chunk in response:
                    content = chunk['message']['content']
                    stream_content += content
                    yield content

            stream = catch_stream(response)
            st.write_stream(stream)

            st.session_state.messages.append({"role": "assistant", "content": stream_content})
        except Exception as e:
            st.error(f"An error occured: {str(e)}")

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
