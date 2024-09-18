from flask import Flask, request, send_file, jsonify, render_template
from flask_cors import CORS
import os
import requests
from pydub import AudioSegment
import random
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Retrieve API keys
XI_API_KEY = os.getenv("XI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate API keys
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found in environment variables.")
if not XI_API_KEY:
    raise ValueError("ElevenLabs API key not found in environment variables.")

# Important constants
VOICE_ID = "t7VcunDELSXwqBUqGfc7"
STORY_WORD_COUNT = 700  # Desired length of the horror story
OUTPUT_TTS_PATH = "story_tts.mp3"
CHUNK_SIZE = 1024  # Size of chunks to read/write at a time

BACKGROUND_MUSIC_FOLDER = "background_music/"
FINAL_OUTPUT_AUDIO_PATH = "final_output_audio.mp3"

# Initialize OpenAI API
client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)
CORS(app)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Existing route to generate story
@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    story_name = data.get('story_name', 'Unknown Story')
    
    try:
        # Generate the horror story
        story = generate_horror_story(story_name, word_count=STORY_WORD_COUNT)

        # Convert the story to speech
        text_to_speech(story, OUTPUT_TTS_PATH, VOICE_ID)

        # Mix the audio with background music
        mix_audio(tts_path=OUTPUT_TTS_PATH,
                  music_folder=BACKGROUND_MUSIC_FOLDER,
                  output_path=FINAL_OUTPUT_AUDIO_PATH)

        # Send the final audio file back to the client
        return send_file(FINAL_OUTPUT_AUDIO_PATH, mimetype='audio/mpeg')

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

def generate_horror_story(story_name, word_count=700):
    prompt = (
        f"""Write a first-person, bone-chilling, atmospheric horror story titled "{story_name}" centered around a paranormal activity occurrence in exactly {word_count} words. The story should start with a very relatable scenario, such as a person settling in for the night after a long day, or staying in a remote cabin for a weekend getaway. Then, something paranormal or sinister happens, like hearing footsteps in the attic or seeing a shadowy figure outside the window. Focus on setting the scene in a quiet, isolated home at night, where every creak and shadow feeds into the protagonist's growing fear. Incorporate eerie, sensory details like the sound of footsteps in the dark, the glint of light on unfamiliar objects, or whispers from unseen corners. The intruder's presence should be felt throughout the narrative, creating an overwhelming sense of helplessness and terror. The protagonist eventually confronts the intruder, leading to a chilling climax that leaves the reader with a lingering sense of dread. The protagonist is alive and is able to report to the police. However, the intruder is never caught and is said to be still lingering around for the next victim. The story should be suitable for audio narration, ensuring every word adds to the suspense and ultimate horror of the protagonist's fate."""
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a creative and imaginative writer specializing in horror stories."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,  # Adjusted for 300 words
        temperature=0.9,
    )

    story = response.choices[0].message.content
    return story

def text_to_speech(text, output_path, voice_id, model_id="eleven_multilingual_v2"):
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "xi-api-key": XI_API_KEY
    }

    data = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.98,
            "similarity_boost": 0.95,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }

    response = requests.post(tts_url, headers=headers, json=data, stream=True)

    if response.ok:
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
        print("TTS audio saved successfully.")
    else:
        raise Exception(f"ElevenLabs TTS API Error: {response.text}")

def mix_audio(tts_path, music_folder, output_path):
    tts_audio = AudioSegment.from_file(tts_path)

    music_files = [file for file in os.listdir(music_folder) if file.lower().endswith(('.mp3', '.wav', '.ogg', '.flac', '.m4a'))]
    if not music_files:
        raise Exception("No background music files found.")
    chosen_music_file = os.path.join(music_folder, random.choice(music_files))
    background_music = AudioSegment.from_file(chosen_music_file)

    total_duration = len(tts_audio) + 5000
    background_music = (background_music * ((total_duration // len(background_music)) + 1))[:total_duration]
    background_music += (tts_audio.dBFS - background_music.dBFS - 12)
    mixed_audio = background_music.overlay(tts_audio)
    mixed_audio = mixed_audio.fade_out(6000)
    mixed_audio.export(output_path, format='mp3')
    print("Mixed audio exported successfully.")

if __name__ == "__main__":
    app.run(debug=True)