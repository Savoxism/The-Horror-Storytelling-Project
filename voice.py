from pydub import AudioSegment

import os
import random

def get_random_background_music(music_folder):
    """
    Selects a random music file from the specified folder.
    Supports common audio formats.
    """
    supported_formats = ('.mp3', '.wav', '.ogg', '.flac', '.m4a')
    music_files = [file for file in os.listdir(music_folder) if file.lower().endswith(supported_formats)]
    
    if not music_files:
        raise ValueError("No supported audio files found in the music folder.")
    
    return os.path.join(music_folder, random.choice(music_files))
  
def mix_audio(tts_path, music_folder, output_path, fade_out_duration=6000):
    """
    Mixes the TTS audio with randomly selected background music, applies volume control, and fade-out effects.
    Appends 5 seconds of background music after the narration for a natural fade-out.
    Adjusts the background music to be lower in volume than the TTS audio by a constant margin.
    """
    # Load TTS audio
    tts_audio = AudioSegment.from_file(tts_path)
    
    # Load background music
    music_path = get_random_background_music(music_folder)
    print(f"Selected background music: {music_path}")
    background_music = AudioSegment.from_file(music_path)
    
    # Adding another 5 seconds at the end
    total_duration_ms = len(tts_audio) + 5000  # 5 seconds in milliseconds
    
    # Loop or trim background music to match the total duration
    if len(background_music) < total_duration_ms:
        loops = int(total_duration_ms / len(background_music)) + 1
        background_music = background_music * loops
    background_music = background_music[:total_duration_ms]
    
    # Normalize background music volume to be lower than TTS
    tts_db = tts_audio.dBFS
    background_music_db = background_music.dBFS
    print(f"TTS dB level: {tts_db} dB")
    print(f"Background music dB level before adjustment: {background_music_db} dB")
    
    # Ensure background music is lower in volume than TTS audio by a margin (e.g., 10 dB)
    target_db_difference = 5  # The desired difference between TTS and background music
    volume_adjustment = tts_db - background_music_db - target_db_difference
    
    # Adjust background music volume
    background_music = background_music + volume_adjustment
    print(f"Background music dB level after adjustment: {background_music.dBFS} dB")
    
    # Overlay tts_audio on background_music for tts_audio duration
    mixed = tts_audio.overlay(background_music, position=0)
    
    # Apply fade-out to the last few seconds
    mixed = mixed.fade_out(fade_out_duration)
    
    # Export mixed audio
    mixed.export(output_path, format="mp3")
    print("Final mixed audio saved successfully.")
    

# Example usage

tts_path = "story_tts.mp3"
music_folder = "background_music"
output_path = "mixed_audio.mp3"
mix_audio(tts_path, music_folder, output_path)