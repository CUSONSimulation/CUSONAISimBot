import streamlit as st
import os
from openai import OpenAI
from io import BytesIO
import base64
from st_audiorec import st_audiorec
import re
from openai.types.beta.assistant_stream_event import ThreadMessageDelta
from openai.types.beta.threads.text_delta_block import TextDeltaBlock
from docx import Document
import tomllib
import hmac
import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning)


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    with st.form("Credentials"):
        st.text_input("Access Code", type="password", key="password")
        st.form_submit_button("Start Chat", on_click=password_entered)
    if "password_correct" in st.session_state:
        st.error("😕 Invalid Code")
    return False


def load_settings():
    return tomllib.load(open("settings.toml", "rb"))


def get_assistant(client):
    name = st.session_state.settings["title"]
    print("Getting assistant:", name)
    has_more = True
    after = None
    while has_more == True:
        assistants = client.beta.assistants.list(after=after)
        for assistant in assistants.data:
            if assistant.name == name:
                return assistant.id
        has_more = assistants.has_more
        after = assistants.last_id

        # Can't find, create a new one
    assistant = client.beta.assistants.create(name=name, model="gpt-4o")
    return assistant.id


@st.cache_data
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def speech_to_text(client, audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", response_format="text", file=audio_file
        )
    return transcript


def text_to_speech(client, input_text):
    response = client.audio.speech.create(model="tts-1", voice="nova", input=input_text)
    webm_file_path = "temp_audio_play.mp3"
    with open(webm_file_path, "wb") as f:
        response.stream_to_file(webm_file_path)
    return webm_file_path


def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)


# Function to generate Word document from the transcript
def create_transcript_word():
    doc = Document()
    doc.add_heading("Conversation Transcript\n", level=1)

    for message in st.session_state.messages:
        if message["role"] == "user":
            p = doc.add_paragraph()
            p.add_run(st.session_state.settings["user_name"] + ": ").bold = True
            p.add_run(message["content"])
        else:
            p = doc.add_paragraph()
            p.add_run(st.session_state.settings["assistant_name"] + ": ").bold = True
            p.add_run(message["content"])

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


def main():
    # Inject CSS for custom styles
    local_css("style.css")

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    if "settings" not in st.session_state:
        st.session_state.settings = load_settings()
    if "assistant_id" not in st.session_state:
        st.session_state.assistant_id = get_assistant(client)
    if "assistant_instruction" not in st.session_state:
        st.session_state.assistant_instruction = st.session_state.settings[
            "instruction"
        ]
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "manual_input" not in st.session_state:
        st.session_state.manual_input = None  # Add this line to initialize manual input
    if "end_session_button_clicked" not in st.session_state:
        st.session_state.end_session_button_clicked = (
            False  # Initialize the state to track the button click
        )
    if "processed_audio" not in st.session_state:
        st.session_state.processed_audio = None  # Initialize the processed audio state

    st.title(st.session_state.settings["title"])

    st.sidebar.header("Chat with " + st.session_state.settings["assistant_name"])
    container1 = st.sidebar.container(border=True)
    with container1:
        for key, val in st.session_state.settings["sidebar"].items():
            if re.search(r"(jpg|png|webp)$", val):
                st.image(val, caption=key.replace("_", " "))
            else:
                st.subheader(f"{key.replace("_", " ")}: {val}")

    # Button Login
    col1, col2, col3 = st.sidebar.columns([1, 1, 1])
    with col2:
        if check_password():
            st.session_state["chat_active"] = True
            st.session_state.show_text = (
                False  # Hide the text when Start Chat is pressed
            )

    # Display text before Start Chat is pressed
    if "show_text" not in st.session_state:
        st.session_state.show_text = True

    if st.session_state.show_text:
        container2 = st.container(border=True)
        with container2:
            st.markdown(st.session_state.settings["intro"])

    # Check if chat is active
    if st.session_state.get("chat_active"):
        st.sidebar.header("Speech Input")

        for message in st.session_state.messages:
            if message["role"] == "user":
                print(message["content"])
                with st.chat_message(
                    st.session_state.settings["user_name"],
                    avatar=st.session_state.settings["user_avatar"],
                ):
                    st.markdown(message["content"])
            else:
                with st.chat_message(
                    st.session_state.settings["assistant_name"],
                    avatar=st.session_state.settings["assistant_avatar"],
                ):
                    st.markdown(message["content"])

        # Check if there's a manual input and process it
        if st.session_state.manual_input:
            user_query = st.session_state.manual_input
            st.session_state.manual_input = None  # Clear manual input after use
        else:
            if st.session_state.end_session_button_clicked:
                user_query = None  # Prevent any input after the end session
            else:
                user_query = st.chat_input(
                    "Click 'End Session' Button to Receive Feedback and Download Transcript."
                )

        # Create footer container for the microphone
        footer_container = st.sidebar.container(border=True)

        with footer_container:
            # audio_bytes = audio_recorder(text="Click to Record", icon_size="2x", neutral_color="#30475E")
            audio_bytes = st_audiorec()
            # st.write(audio_bytes)

            # Check if there is a new audio recording and it has not been processed yet
            if (
                audio_bytes
                and audio_bytes != st.session_state.processed_audio
                and audio_bytes
                != b"RIFF,\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x02\x00\x80\xbb\x00\x00\x00\xee\x02\x00\x04\x00\x10\x00data\x00\x00\x00\x00"
            ):
                webm_file_path = "temp_audio.mp3"
                with open(webm_file_path, "wb") as f:
                    f.write(audio_bytes)
                transcript = speech_to_text(client, webm_file_path)
                if transcript:
                    os.remove(webm_file_path)
                    user_query = transcript  # Ensure you extract the text from the transcript object correctly
                    st.session_state.processed_audio = (
                        audio_bytes  # Update the processed audio state
                    )

            if (
                audio_bytes
                == b"RIFF,\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x02\x00\x80\xbb\x00\x00\x00\xee\x02\x00\x04\x00\x10\x00data\x00\x00\x00\x00"
            ):
                st.error("Something went wrong. Kindly refresh the page and try again.")
                st.stop()

        if user_query:
            if user_query.lower() == "exit":
                st.session_state["chat_active"] = False
                st.stop()

            # Create a new thread if it does not exist
            if "thread_id" not in st.session_state:
                thread = client.beta.threads.create()
                st.session_state.thread_id = thread.id

            # Display the user's query
            with st.chat_message(
                st.session_state.settings["user_name"],
                avatar=st.session_state.settings["user_avatar"],
            ):
                st.markdown(user_query)

            # Store the user's query into the history
            st.session_state.messages.append({"role": "user", "content": user_query})

            # Add user query to the thread
            client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id, role="user", content=user_query
            )

            # Stream the assistant's reply
            with st.chat_message(
                st.session_state.settings["assistant_name"],
                avatar=st.session_state.settings["assistant_avatar"],
            ):
                stream = client.beta.threads.runs.create(
                    thread_id=st.session_state.thread_id,
                    assistant_id=st.session_state.assistant_id,
                    instructions=st.session_state.assistant_instruction,
                    stream=True,
                )

                # Empty container to display the assistant's reply
                assistant_reply_box = st.empty()

                # A blank string to store the assistant's reply
                assistant_reply = ""

                # Iterate through the stream
                for event in stream:
                    if isinstance(event, ThreadMessageDelta):
                        if isinstance(event.data.delta.content[0], TextDeltaBlock):
                            # empty the container
                            assistant_reply_box.empty()
                            # add the new text
                            assistant_reply += event.data.delta.content[0].text.value
                            # display the new text
                            assistant_reply_box.markdown(assistant_reply)
                    if event.data.object == "thread.message.delta":
                        for content in event.data.delta.content:
                            if content.type == "image_file":
                                file_id = content.image_file.file_id
                                image_data = client.files.content(file_id)
                                image_data_bytes = image_data.read()
                                with open("my-image.png", "wb") as file:
                                    file.write(image_data_bytes)
                                st.image("my-image.png")

                # Once the stream is over, update chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": assistant_reply}
                )
                if not st.session_state.end_session_button_clicked:
                    audio_file = text_to_speech(client, assistant_reply)
                    autoplay_audio(audio_file)

    st.sidebar.warning(st.session_state.settings["warning"])

    # Button to show the download button
    if st.session_state.get("chat_active"):
        if st.session_state.end_session_button_clicked:
            st.button("End Session", disabled=True)
        else:
            if st.session_state.get("messages"):
                if st.button("End Session"):
                    st.session_state.end_session_button_clicked = True
                    st.session_state["end_session_button"] = True
                    st.session_state.manual_input = (
                        "Goodbye. Thank you for coming."  # Set manual input
                    )
                    # Trigger the manual input immediately
                    st.rerun()

    # Check if there's a transcript to download
    if st.session_state.get("end_session_button"):
        word_buffer = create_transcript_word()

        col1, col2 = st.columns([1, 1])
        # Button to download the full conversation transcript
        with col1:
            st.download_button(
                label="Download Transcript",
                data=word_buffer,
                file_name="Transcript.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )


if __name__ == "__main__":
    main()
