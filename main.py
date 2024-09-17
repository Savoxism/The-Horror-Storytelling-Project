import os
from openai import OpenAI
from dotenv import load_dotenv
import requests
from pydub import AudioSegment
import random
from moviepy.editor import (
    AudioFileClip,
    ImageClip,
    concatenate_videoclips,
)

load_dotenv()

# Retreive API keys
XI_API_KEY = os.getenv("XI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate API keys
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found in environment variables.")
if not XI_API_KEY:
    raise ValueError("ElevenLabs API key not found in environment variables.")

# Important constants
VOICE_ID = "t7VcunDELSXwqBUqGfc7"
OPEN_AI_MODEL = "o1-preview"

STORY_WORD_COUNT = 300  # Desired length of the horror story
OUTPUT_TTS_PATH = "story_tts.mp3"
CHUNK_SIZE = 1024  # Size of chunks to read/write at a time

BACKGROUND_MUSIC_FOLDER = "background_music/"
FINAL_OUTPUT_AUDIO_PATH = "final_output_audio.mp3"

IMAGE_DISPLAY_DURATION_RANGE = (30, 45)  # Duration each image is displayed (seconds)
TRANSITION_DURATION = 2  # Duration of fade in/out transitions (seconds)
VIDEO_SIZE = (1280, 720)  # Video resolution (width, height)
FINAL_VIDEO_PATH = "final_output_video.mp4"
IMAGES_FOLDER = "images/"

# Initialize OpenAI API
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_horror_story(word_count=800):
    
    exemplary_story = """
        I’m not going to call myself an expert hiker, but I’ve been avidly enjoying the activity for a few decades now. I’ve traversed all the major trails in America, and I’ve been to over 75% of this beautiful country’s national parks. As such, I’ve had to find new ways to excite myself. I recently picked up a new hobby: scouring Google Maps for vast unnamed forests and just exploring them. It’s a little unconventional, but I think the added excitement is worth the risk of getting lost. Or at least I did. I carry a pack of homemade route-marking stickers that I periodically slap onto trees so I don’t forget my way back. As I pass each one, I pull them off the trees so as not to leave any litter behind. I’m surprised more people haven’t picked up on this trick. It makes getting lost in a forest nearly impossible.

        Anyway, there was a slightly more daunting task ahead of me this time around. I had decided to explore Dudley Town Forest in Connecticut, which I’m sure would give any normal person pause. If you don’t know, the whole town has been abandoned since the 1800s, and there are all sorts of creepy accounts about strange things and stuff like that. You should do some research on the place if you’re interested in that sort of thing. I’m not, though. I’m not superstitious, and I don’t believe in ghost stories. Technically, this forest is off-limits to the public, but that hasn’t stopped me before. As I saw it, I was basically guaranteed to not encounter anyone in those woods, which is usually what I go for. I’m also from New England, so the drive actually wasn’t so bad.

        I entered the woods around noon to ensure that the sun didn’t go down before I finished hiking. My first impression of the woods was honestly pretty freaky. I had heard that it was dead silent in there, and I was surprised to discover that it actually was. You don’t really notice or appreciate all the sounds in the forest until they aren’t there anymore. Imagine closing your eyes in a silent room and only being able to hear your breathing. That’s what it was like. To be completely honest, this silent phenomenon wasn’t something foreign to me. I’d been in forests void of animals before. I kept walking, placing my stickers as I went, trying to shake the eerie feeling the forest was inducing. I kept thinking I would eventually stumble upon an animal or at least some indication that there was life in there, but I had no such luck.

        After a while, I was honestly hoping to encounter a person even. That’s how unsettled I was. Pretty soon, though, the silence of the forest stopped bothering me so much. For the first time since I’d stepped foot in those woods, I was calm. The feeling didn’t last long, though. Out of nowhere, I picked up on a sound that sent the uneasiness rushing back in. It was like a wailing, moaning sound. The kind of sound you might imagine a wounded animal making. That’s the best way I can put it. I still have trouble describing it even to this day. It was especially creepy since it was the only sound in the whole damn woods. I paused and listened, trying to figure out what it could be. I had never heard anything like it. There was a chance it could have been a whistling made by the wind, but there wasn’t any wind to begin with, so that didn’t make sense. I concluded that it was most likely a wounded animal, even though I knew it probably wasn’t.

        I walked away from it until the sound faded away. You are probably wondering why I didn’t just turn around and leave right there. I wish I had an answer to that question. I told myself that if one more creepy thing happened, that would be it for me. As I walked, I started thinking to myself, how would an animal even get wounded in a forest like this? Like, was there someone hunting in here? There’s no way I could have missed a gunshot. Maybe the hunter had taken the shot before I was in earshot. Maybe he neglected to put the thing out of its misery. Would someone really do that, though? It was hard to imagine. All these thoughts and more were bouncing around in my head when I stumbled upon something on the tree directly in front of me.

        There were honest-to-God carvings. I know it sounds cliche, but I’m being dead serious. The carvings were in symbols, and they didn’t look like letters either—just random slashes and bits of missing tree bark. I started looking around and saw that several of the neighboring trees were covered in the same marks. That was it for me. I turned around without another thought and began walking back, unsticking my trail markers as I passed them. I’m a curious person by nature, and even I was thinking, screw this. I followed my trail markers for a while before seeing something in the distance I hadn’t seen before. There was what looked like a bear’s den up ahead or at least a cave of some sort.

        I stopped walking, confused. I know myself; there was a 0% chance I would have overlooked something like a bear’s den. And that’s when it hit me: my trail markers should have been shoulder-high, not waist-high. My blood ran cold. I turned around and began sprinting back the way I had come, constantly looking over my shoulder. How could I have been so absent-minded? Someone had moved my stickers in an attempt to lure me into that cave. But how? Was it really possible that someone had been tracking me this entire time? I didn’t have time to think all of it through. I was busy focusing on getting the hell out of that forest. The issue with that, though, was that I literally had no idea where I was going. Without those trail markers, I was as good as lost.

        I kept running, not even trying to be quiet. It would have been pointless anyway. The forest was dead silent apart from the sounds I was making. I stopped to catch my breath and pulled out my phone, praying for a signal. By some miracle, I did have a bar. I found my parked car’s location on the map and figured out which direction I needed to go. I wasn’t far, and just like that, the signal dropped. It didn’t matter, though. I knew where I was going now. And that’s when the wailing started up again, only this time it was twice as loud. I ran faster than I had ever run before, even though my most fit years were behind me. The sound seemed like it was coming from right behind me, but every time I turned to look, I couldn’t see anything.

        After the worst 10 minutes of my life, I finally reached the edge of the forest, and the wailing stopped abruptly. I jumped in my car and sped off before whatever had been chasing me had a chance to catch up. That day ruined hiking for me. Here’s my rational explanation for what happened: some hermit or woods freak lives in those woods and noticed me before I noticed him. He then, for whatever reason, tracked me and messed with my trail markers, hoping to lure me toward that cave. I’m assuming he had a whistle or something that made that wailing noise, which is why it stopped so abruptly once he realized he wasn’t going to catch me.

        I know there are holes in this explanation, like how could someone blow through a whistle for that long while simultaneously running at full speed? I’m open to anybody suggesting explanations. Maybe there’s a reason that forest is off-limits to civilians.
     """
     
    prompt = (
        f"""Write a first-person, bone-chilling, atmospheric horror story centered around a paranormal activity occurrence in exactly {word_count} words. The story should start with a very relatable scenario, such as a person settling in for the night after a long day, or staying in a remote cabin for a weekend getaway. Then, something paranormal or sinister happens, like hearing footsteps in the attic or seeing a shadowy figure outside the window. Focus on setting the scene in a quiet, isolated home at night, where every creak and shadow feeds into the protagonist's growing fear. Incorporate eerie, sensory details like the sound of footsteps in the dark, the glint of light on unfamiliar objects, or whispers from unseen corners. The intruder's presence should be felt throughout the narrative, creating an overwhelming sense of helplessness and terror. The protangonist eventually confronts the intruder, leading to a chilling climax that leaves the reader with a lingering sense of dread. The protagonist is alive, and is able to report to the police. However, the intruder is never caught and said to be still lingering around for the next victim. The story should be suitable for audio narration, ensuring every word adds to the suspense and ultimate horror of the protagonist's fate.
        
        Consult this story for example: {exemplary_story}
        """
    )
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a creative and imaginative writer specializing in horror stories."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=word_count,  # Approximate token count for the desired word count
        temperature=0.8,
    )
    
    story = response.choices[0].message.content
    return story

def text_to_speech(text, output_path, voice_id, model_id="eleven_multilingual_v2"):
    """
    Converts text to speech using ElevenLabs API and saves the audio to the specified path.
    """
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
            "stability": 0.95,
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

#####

def mix_audio(tts_path, music_folder, output_path):
    tts_audio = AudioSegment.from_file(tts_path)
    
    music_files = [file for file in os.listdir(music_folder) if file.lower().endswith(('.mp3', '.wav', '.ogg', '.flac', '.m4a'))]
    chosen_music_file = os.path.join(music_folder, random.choice(music_files))
    background_music = AudioSegment.from_file(chosen_music_file)
    
    total_duration = len(tts_audio) + 5000
    background_music = (background_music * ((total_duration // len(background_music)) + 1))[:total_duration]
    print(f"The background music db is {background_music.dBFS}")
    print(f"The tts_music db is: {tts_audio.dBFS}")
    background_music += (tts_audio.dBFS - background_music.dBFS - 12) # Ensure a 12 unit dB difference
    print(f"after change {background_music.dBFS}")
    mixed_audio = background_music.overlay(tts_audio)
    mixed_audio = mixed_audio.fade_out(6000)
    mixed_audio.export(output_path, format='mp3')
    print(f"Mixed audio exported successfully ")

def create_video_with_images(audio_path, images_folder, output_video_path, display_duration_range=(30, 45), transition_duration=2, video_size=(1280, 720)):
    """
    Creates a video by combining a slideshow of images with the provided audio.
    Each image is displayed for a random duration within the specified range, with fade transitions.
    Ensures the video resolution is set to 1280x720.
    """
    # Load the audio file
    audio_clip = AudioFileClip(audio_path)
    audio_duration = audio_clip.duration
    print(f"Audio duration: {audio_duration} seconds")
    
    # Get list of images
    image_files = [os.path.join(images_folder, file) for file in os.listdir(images_folder)
                   if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    if not image_files:
        raise ValueError("No image files found in the specified images folder.")
    
    # Calculate total number of images needed based on audio duration and display duration range
    avg_display_duration = sum(display_duration_range) / 2
    num_images = max(1, int(audio_duration / avg_display_duration))
    print(f"Number of images to display: {num_images}")
    
    # Randomly select images
    selected_images = random.choices(image_files, k=num_images)
    
    # Create ImageClips with random display durations
    clips = []
    for img_path in selected_images:
        display_duration = random.uniform(*display_duration_range)
        img_clip = ImageClip(img_path).set_duration(display_duration)
        
        # Resize the image, maintaining aspect ratio, and fit within 1280x720
        img_clip = img_clip.resize(height=video_size[1])
        if img_clip.w > video_size[0]:
            img_clip = img_clip.resize(width=video_size[0])
        
        # Pad the image to fit exactly 1280x720 if necessary
        img_clip = img_clip.on_color(size=video_size, color=(0, 0, 0), pos='center')

        # Apply fade-in and fade-out
        img_clip = img_clip.fadein(transition_duration).fadeout(transition_duration)
        
        clips.append(img_clip)
    
    # Concatenate ImageClips with crossfade transitions
    video = concatenate_videoclips(clips, method="compose", padding=-transition_duration)
    
    # Ensure the video duration matches the audio duration
    if video.duration < audio_duration:
        # Calculate how much more time is needed
        additional_duration = audio_duration - video.duration
        additional_images = random.choices(image_files, k=int(additional_duration / avg_display_duration) + 1)
        for img_path in additional_images:
            display_duration = random.uniform(*display_duration_range)
            img_clip = ImageClip(img_path).set_duration(display_duration)
            
            # Resize and pad the image to fit 1280x720
            img_clip = img_clip.resize(height=video_size[1])
            if img_clip.w > video_size[0]:
                img_clip = img_clip.resize(width=video_size[0])
            img_clip = img_clip.on_color(size=video_size, color=(0, 0, 0), pos='center')
            
            # Apply fade-in and fade-out
            img_clip = img_clip.fadein(transition_duration).fadeout(transition_duration)
            
            clips.append(img_clip)
            video = concatenate_videoclips([video, img_clip], method="compose", padding=-transition_duration)
            if video.duration >= audio_duration:
                break
    
    video = video.subclip(0, audio_duration)
    
    # Add audio to the video
    final_video = video.set_audio(audio_clip)
    
    # Write the final video to a file
    final_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac", fps=24)
    print(f"Final video saved successfully as {output_video_path}.")
    

def main():
    try:
        print("Generating horror story...")
        story = generate_horror_story(word_count=STORY_WORD_COUNT)
        print("Horror story generated successfully.\n")
        print("Story Content:\n")
        print(story)
        
        print("\nConverting story to speech...")
        text_to_speech(story, OUTPUT_TTS_PATH, VOICE_ID)
        
        print("\nMixing TTS audio with background music...")
        mix_audio(tts_path=OUTPUT_TTS_PATH,
                  music_folder=BACKGROUND_MUSIC_FOLDER,
                  output_path=FINAL_OUTPUT_AUDIO_PATH,
                  )
        
        print("\nCreating video with image slideshow and mixed audio...")
        # create_video_with_images(
        #     audio_path=FINAL_OUTPUT_AUDIO_PATH,
        #     images_folder=IMAGES_FOLDER,
        #     output_video_path=FINAL_VIDEO_PATH,
        #     display_duration_range=IMAGE_DISPLAY_DURATION_RANGE,
        #     transition_duration=TRANSITION_DURATION,
        #     video_size=VIDEO_SIZE
        # )
        
        print("\nProcess completed successfully!")
        print(f"Final audio file saved as: {FINAL_OUTPUT_AUDIO_PATH}")
        print(f"Final video file saved as: {FINAL_VIDEO_PATH}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()












