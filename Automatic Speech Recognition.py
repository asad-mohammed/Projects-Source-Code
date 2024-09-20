import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import io

# Initialize recognizer class (for recognizing the speech)
recognizer = sr.Recognizer()

def recognize_speech_from_mic():
    with sr.Microphone() as source:
        st.info("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source)
        st.info("Listening...")
        audio = recognizer.listen(source)
        try:
            st.info("Recognizing...")
            text = recognizer.recognize_google(audio)
            st.success("You said: " + text)
        except sr.UnknownValueError:
            st.error("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            st.error("Could not request results from Google Speech Recognition service; {0}".format(e))

def recognize_speech_from_audio_file(audio_file):
    try:
        st.info("Processing the uploaded audio file...")

        # Read the audio file into a BytesIO object
        audio_bytes = audio_file.read()
        audio_io = io.BytesIO(audio_bytes)

        # Determine the format of the audio file
        file_extension = audio_file.name.split('.')[-1].lower()
        if file_extension not in ['wav', 'mp3', 'ogg', 'm4a']:
            st.error("Unsupported file format")
            return

        # Convert the audio file to WAV format using pydub
        audio = AudioSegment.from_file(audio_io, format=file_extension)
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)
        st.info("Converted audio to WAV format")

        # Use the in-memory WAV file for speech recognition
        with sr.AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)
            st.info("Recognizing...")
            text = recognizer.recognize_google(audio_data)
            st.success("Transcription: " + text)
    except sr.UnknownValueError:
        st.error("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        st.error(f"Error processing the audio file: {e}")

def main():
    st.title("Automatic Speech Recognition")
    st.write("This application takes input as audio in English from the user and displays the text. You can either speak in real-time or upload an audio file.")

    st.header("Real-time Speech Recognition")
    if st.button("Start"):
        recognize_speech_from_mic()

    st.header("Upload an Audio File")
    audio_file = st.file_uploader("Choose an audio file...", type=["wav", "mp3", "ogg", "m4a"])
    if audio_file is not None:
        st.info(f"Uploaded file: {audio_file.name}")
        recognize_speech_from_audio_file(audio_file)

if __name__ == "__main__":
    main()
