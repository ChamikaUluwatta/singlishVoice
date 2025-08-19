import streamlit as st
import requests
import os
from dotenv import load_dotenv
from urllib.parse import unquote_to_bytes

# --- Configuration ---
load_dotenv()
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/generate")

def call_tts_api(text, speaker):
    payload = {"text": text, "speaker": speaker}
    headers = {"Content-Type": "application/json", "Accept": "audio/wav"}
    api_timeout_seconds = 90

    try:
        response = requests.post(BACKEND_API_URL, json=payload, headers=headers, timeout=api_timeout_seconds, stream=True)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '')
        content_disposition = response.headers.get('Content-Disposition', '')

        if 'audio/wav' in content_type:
            st.success("Transliteration and TTS completed successfully!")
            audio_data = response.content
            transliterated_text = "Transliteration result"
            if content_disposition:
                if "filename*=" in content_disposition:
                    try:
                        filename_part = content_disposition.split("filename*=")[1]
                        encoding, encoded_filename = filename_part.split("''", 1)
                        decoded_bytes = unquote_to_bytes(encoded_filename)
                        transliterated_text = decoded_bytes.decode('utf-8')
                    except Exception as e:
                        st.error(f"Filename decoding error: {str(e)}")
                        transliterated_text = "Transliteration result"
                elif "filename=" in content_disposition:
                    transliterated_text = content_disposition.split("filename=")[1].strip('"')
            
            return audio_data, transliterated_text
        else:
            st.error("Unexpected response format from server.")
            return None, None

    except requests.exceptions.Timeout:
        st.error(f"API request timed out after {api_timeout_seconds} seconds.")
        return None, None
    except requests.exceptions.HTTPError as http_err:
        st.error(f"API Request Failed with HTTP Status Code: {http_err.response.status_code}")
        try:
            error_detail = http_err.response.json()
            st.error(f"Backend Error Detail: {error_detail.get('detail', 'No specific detail provided.')}")
        except ValueError:
            st.error(f"Backend Response (non-JSON): {http_err.response.text[:500]}")
        return None, None
    except requests.exceptions.RequestException as e:
        st.error(f"API Request Failed: {e}")
        return None, None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None, None

# --- UI Rendering Functions ---

def render_input_view():
    st.markdown("<h1 style='text-align: center;'>SinglishVoice</h1>", unsafe_allow_html=True)

    text_input = st.text_input("Enter Romanized Text:", key="input_text_main", placeholder="e.g., oyata kohomada")

    # Model selection placeholders
    st.selectbox("Select Transliterate Model", ["NLLB (Default)"], key="nllb_model_select", disabled=True)
    st.selectbox("Select TTS Model", ["VITS (Default)"], key="tts_model_select", disabled=True)

    # Speaker selection
    speaker_options = ("Male (Mettananda)","Female (Oshadi)")
    speaker_mapping = {
        "Male (Mettananda)": "mettananda",
        "Female (Oshadi)": "oshadi"
    }
    selected_speaker_display = st.selectbox("Select Speaker", speaker_options, key="speaker_select_main")
    selected_speaker_value = speaker_mapping[selected_speaker_display] 

    # Generate button
    generate_button = st.button("Generate speech", key="generate_button_main", type="primary")

    if generate_button:
        if not text_input:
            st.warning("Please enter some text to generate speech.")
        else:
            with st.spinner("Generating audio... Please wait."):
                audio_bytes, transliterated_text = call_tts_api(text_input, selected_speaker_value)

                if audio_bytes:
                    st.session_state.audio_bytes = audio_bytes
                    st.session_state.transliterated_text = transliterated_text
                    st.session_state.show_results = True
                    st.rerun()
                else:
                    st.session_state.show_results = False

def render_results_view():
    st.markdown("<h1 style='text-align: center;'>Generated Output</h1>", unsafe_allow_html=True)

    # Display Transliteration Result
    if st.session_state.get('transliterated_text'):
        st.subheader("Transliteration Result")
        st.markdown(f"<div style='padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem;'>"
                    f"{st.session_state.transliterated_text}</div>", 
                    unsafe_allow_html=True)

    # Display Audio Player
    if st.session_state.get('audio_bytes'):
        st.subheader("Generated Audio")
        st.audio(st.session_state.audio_bytes, format='audio/wav')
        
        # Download button
        st.download_button(
            label="Download Audio",
            data=st.session_state.audio_bytes,
            file_name=f"{st.session_state.transliterated_text}.wav",
            mime="audio/wav",
            key="download_button"
        )
    else:
        st.warning("No audio data available to display.")

    # Generate New button
    if st.button("Generate New", key="generate_new_button"):
        st.session_state.show_results = False
        st.session_state.audio_bytes = None
        st.session_state.transliterated_text = None
        st.rerun()

# --- Main App Logic ---
def main():
    st.set_page_config(layout="centered", page_title="SinglishVoice")

    # Initialize session state
    session_defaults = {
        'show_results': False,
        'audio_bytes': None,
        'transliterated_text': None
    }
    for key, value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.show_results:
        render_results_view()
    else:
        render_input_view()


if __name__ == "__main__":
    main()