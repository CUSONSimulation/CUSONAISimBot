import streamlit as st
import os
from openai import OpenAI
from io import BytesIO
import base64
from streamlit_mic_recorder import mic_recorder
import re
from docx import Document
import tomllib
import hmac
import warnings
import io

warnings.filterwarnings("ignore", category=DeprecationWarning)


def password_entered():
    """Checks whether a password entered by the user is correct."""
    if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
        st.session_state["password_correct"] = True
        del st.session_state["password"]  # Don't store the password.
    else:
        st.session_state["password_correct"] = False


def load_settings():
    return tomllib.load(open("settings.toml", "rb"))


@st.cache_data
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def speech_to_text(client, audio):
    try:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", response_format="text", file=audio
        )
        return transcript
    except Exception as e:
        print("speech_to_text:", e)


def text_to_speech(client, input_text):
    try:
        response = client.audio.speech.create(
            model="tts-1", voice="nova", input=input_text
        )
        autoplay_audio(response.content)
    except Exception as e:
        print("text_to_speech:", e)


def autoplay_audio(audio_data):
    b64 = base64.b64encode(audio_data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)


# Send prompt and get response
def stream_response(client, messages):
    try:
        stream = client.chat.completions.create(
            model=st.session_state.settings["parameters"]["model"],
            messages=messages,
            temperature=st.session_state.settings["parameters"]["temperature"],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    except Exception as e:
        print("Stream_response:", e)
        return


# Function to generate Word document from the transcript
def create_transcript_word():
    doc = Document()
    doc.add_heading("Conversation Transcript\n", level=1)

    for message in st.session_state.messages[1:]:
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
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": st.session_state.settings["instruction"]}
        ]
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
                st.image(val)
            else:
                st.subheader(f"{key.replace("_", " ")}: {val}")

    # Button Login
    if (
        st.session_state.get("password_correct", False)
        and st.session_state.password_correct
    ):
        st.session_state["chat_active"] = True
        st.session_state.show_text = False  # Hide the text when Start Chat is pressed
    else:
        st.sidebar.header("Access Code")
        with st.sidebar.container(border=True):
            with st.form("Credentials"):
                st.text_input("Access Code", type="password", key="password")
                st.form_submit_button("Start Chat", on_click=password_entered)
            if "password_correct" in st.session_state:
                st.error("😕 Invalid Code")

    # Display text before Start Chat is pressed
    if "show_text" not in st.session_state:
        st.session_state.show_text = True

    if st.session_state.show_text:
        with st.container(border=True):
            st.markdown(st.session_state.settings["intro"])

    # Check if chat is active
    if st.session_state.get("chat_active"):
        for message in st.session_state.messages[1:]:
            if message["role"] == "user":
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

        # Create container for the microphone
        with st.sidebar.container(border=True):
            audio = mic_recorder(
                start_prompt="🎙 Record",
                stop_prompt="📤 Stop",
                just_once=False,
                use_container_width=True,
                format="wav",
                key="recorder",
            )

        # Check if there is a new audio recording and it has not been processed yet
        if audio and audio["id"] != st.session_state.processed_audio:
            audio_bio = io.BytesIO(audio["bytes"])
            audio_bio.name = "audio.webm"
            transcript = speech_to_text(client, audio_bio)

            if transcript:
                user_query = transcript  # Ensure you extract the text from the transcript object correctly
                st.session_state.processed_audio = audio["id"]

        if user_query:
            # Display the user's query
            with st.chat_message(
                st.session_state.settings["user_name"],
                avatar=st.session_state.settings["user_avatar"],
            ):
                st.markdown(user_query)

            # Store the user's query into the history
            st.session_state.messages.append(
                {"role": "user", "content": user_query.strip()}
            )

            # Stream the assistant's reply
            with st.chat_message(
                st.session_state.settings["assistant_name"],
                avatar=st.session_state.settings["assistant_avatar"],
            ):
                # Empty container to display the assistant's reply
                assistant_reply_box = st.empty()

                # A blank string to store the assistant's reply
                assistant_reply = ""

                # Iterate through the stream
                for chunk in stream_response(client, st.session_state.messages):
                    assistant_reply += chunk
                    assistant_reply_box.markdown(assistant_reply)

                # Once the stream is over, update chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": assistant_reply.strip()}
                )
                if not st.session_state.end_session_button_clicked:
                    text_to_speech(client, assistant_reply)

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
                label="📥 Download Transcript",
                data=word_buffer,
                file_name="Transcript.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )


if __name__ == "__main__":
    main()
