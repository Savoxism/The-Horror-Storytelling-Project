from pydub import AudioSegment

# Load an audio file
audio = AudioSegment.from_file("final_output.mp3")

# Increase volume by 10 dB
louder_audio = audio + 10

# Decrease volume by 5 dB
quieter_audio = audio - 15

# # Export the adjusted volume audio files
# louder_audio.export("louder_audio.mp3", format="mp3")
quieter_audio.export("quieter_audio.mp3", format="mp3")

print("Volume adjusted and files saved.")