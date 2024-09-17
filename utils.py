from pydub import AudioSegment
import os

def get_random_background_music(music_folder):
    """
    Selects a random music file from the specified folder.
    Supports common audio formats.
    """
    supported_formats = ('.mp3', '.wav', '.ogg', '.flac', '.m4a')
    music_files = [file for file in os.listdir(music_folder) if file.lower().endswith(supported_formats)]
    
    if not music_files:
        raise ValueError("No supported audio files found in the music folder.")

def mix_audio(tts_path, music_folder, output_path):
    tts_audio = AudioSegment.from_file(tts_path)
    background_music = AudioSegment.from_file(get_random_background_music(music_folder))
    total_duration = len(tts_audio) + 5000
    background_music = (background_music * ((total_duration // len(background_music)) + 1))[:total_duration]
    background_music += (tts_audio.dBFS - background_music.dBFS - 10)
    mixed_audio = background_music.overlay(tts_audio)
    mixed_audio = mixed_audio.fade_out(6000)
    mixed_audio.export(output_path, format='mp3')
    
tts_path = "story_tts.mp3"
music_folder = "background_music"
output_path = "mixed_audio.mp3"
mix_audio(tts_path, music_folder, output_path)