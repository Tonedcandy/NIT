import openai
import speech_recognition as sr
import requests
import time
from pydub import AudioSegment
from pydub.playback import play
import os


# Set up OpenAI API credentials
openai.api_key = "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"

# Set up ElevenLabs.io API credentials
elevenlabs_token = "10b8dfa2f6e243c2cb5d19b6d57d15b2"

# Configure the OpenAI completion
def complete_prompt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """Assume the role of a helpful assistant
       
         """},
            {"role": "user", "content": prompt},
        ],
        max_tokens=100,
    )
    return response.choices[0].message.content

# Convert text to audio using ElevenLabs.io TTS API
def text_to_audio(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM/stream"
    headers = {
        "Content-Type": "application/json",
        "xi-api-key": elevenlabs_token,
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers, stream=True)
    print(response)
    with open('output.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

# Record audio and convert it to text
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Recording for 4 seconds...")
        recorded_audio = recognizer.listen(source, timeout=4)
        print("Done recording.")

    try:
        print("Recognizing the text...")
        text = recognizer.recognize_google(recorded_audio, language="en-US")
        return text

    except Exception as ex:
        print(ex)
        return None

# Main function
def main():
    # Record audio and convert to text
    text = recognize_speech()
    if text:
        print("Decoded Text: {}".format(text))
        # Generate response using GPT-3.5 Turbo
        response = complete_prompt(text)
        print("GPT Response: {}".format(response))
        # Convert response text to audio
        text_to_audio(response)
        # Play the audio
        print(os.getcwd())
        audio_segment = AudioSegment.from_file(os.getcwd()+"/output.mp3", format="mp3")
        play(audio_segment)
    else:
        print("Speech recognition failed.")

if __name__ == "__main__":
    while True:
        main()