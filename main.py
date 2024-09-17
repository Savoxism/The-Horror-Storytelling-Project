import os
from openai import OpenAI
from dotenv import load_dotenv
import requests
from pydub import AudioSegment
from pydub.effects import normalize
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

OUTPUT_TTS_PATH = "story_tts.mp3"
BACKGROUND_MUSIC_FOLDER = "background_music/"
FINAL_OUTPUT_AUDIO_PATH = "final_output_audio.mp3"
FINAL_VIDEO_PATH = "final_output_video.mp4"
IMAGES_FOLDER = "images/"

FADE_OUT_DURATION = 6000  # milliseconds
CHUNK_SIZE = 1024  # Size of chunks to read/write at a time
MUSIC_VOLUME_DB = -20  # Adjust the background music volume in dBFS (-20 is a reasonable starting point)
STORY_WORD_COUNT = 50  # Desired length of the horror story

IMAGE_DISPLAY_DURATION_RANGE = (30, 45)  # Duration each image is displayed (seconds)
TRANSITION_DURATION = 2  # Duration of fade in/out transitions (seconds)
VIDEO_SIZE = (1280, 720)  # Video resolution (width, height)

# Initialize OpenAI API
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_horror_story(word_count=800):
    
    exemplary_story = """
     I'm a big hiker. I was doing some hiking in Utah during a cross-country trip I was taking after breaking up with who I thought was going to be my fiance. Long story short, I caught her messing around with one of my closest friends. Total betrayal on both sides. I was 31. Utah was actually one of the states I was most excited about passing through. There are some great forests out there that I think every hiker would dream of exploring. I had picked Wasatch National Forest as my Utah destination because I had heard a lot of great things about it. One of its biggest upsides for me was that it had a lot of secluded areas that I could easily access. I prefer hiking alone, so bustling hiking trails swarming with people aren't really my thing. I picked an unnamed area of the forest and drove my car as far down this narrow access road as I could. I parked, stepped out of my car, and took in my surroundings. I geared up and checked my phone. No service, just the way I like it. I made a mental note of my starting point and began the trek. I know hiking alone in uncharted territory is dangerous, but I don’t think I have as much fun following a designated route. I always download the digital map of whatever location I’m planning to explore. A lot of people don’t realize that your phone’s GPS still functions without service. I know what you're probably thinking, but no, I didn’t get lost. I wish I could tell you that’s what the story is about. The reality of what happened to me is something I’m still trying to wrap my head around. My destination was a lookout point at the summit of the mountain, which was maybe 3 or 4 miles away. The terrain was pretty difficult, so I was only clearing about 1 and 1/2 miles an hour. About an hour into my hike, it began raining. Although it was light, I refused to continue hiking in the rain as a massive pet peeve of mine. Annoyed, I turned around and began retracing my steps. Eventually, I spotted my car in the distance, and I was relieved that this failed outing would soon be over. I reached my vehicle and was met with a horrifying sight. All four tires were slashed. I felt the fear start to set in. There wasn’t a chance in the world that all four tires had been coincidentally punctured. This had been deliberate. I whipped my head around, scanning the forest in every direction. Nothing. I listened as carefully as I could, but anything I might have picked up on was drowned out by the patter of raindrops on leaves and brush. I weighed my options. Without service, I was basically screwed. I’d need to get service so I could call for assistance, but as far as I remembered, I had lost service over 20 miles down the access road. Walking back to civilization seemed like a grueling option. I needed to find high ground. Luckily, the destination I had originally sought out was just that. I had to chance it. I didn’t feel safe walking 20 miles down the road where I’d basically be out in the open. Without another thought, I turned back towards the woods and began my route once again. I was about halfway to the summit when I picked up on a faint rustling coming from behind me, maybe 40 or so yards away. It would start and stop in tandem with my movements. I didn’t want to turn and look; I just picked up the pace, knowing I was probably a faster hiker than whoever or whatever was stalking me. The sun was starting to go down, casting an eerie shadow over the forest. The rain was still falling, and I was starting to get nervous. After putting some distance between myself and whatever was stalking me, I cast an inconspicuous glance over my shoulder. I didn’t see anything, but someone could have easily been hiding behind any of the countless trees in the forest. Finally, I reached the peak. By some miracle, there actually was service up there. I didn’t waste a second, not even pausing to admire the view. I told the police exactly where my car was and explained what happened, including my suspicion that I was being stalked. I also told the operator that I had AAA. I hung up, relieved that someone knew where I was. There was still a glaring problem, though. I’d have to navigate back through the forest before it was fully dark while somehow avoiding whoever was stalking me. I couldn’t just march in a straight line back through the forest; that was asking for trouble. I thought for a second before concluding that I’d have to try to walk in a semicircle back to my car, hopefully avoiding any kind of trap someone had set. I walked parallel to the cliff for a while before entering the woods from a different angle. I hadn’t bothered to analyze this area of the forest, though, so I pulled up the map on my phone and prayed my navigation skills wouldn’t let me down. Things were going well for a while. I hadn’t heard a single unusual sound behind me or in front of me. I might have spoken too soon, though, because not 30 seconds after having that thought, I heard a twig snap from my left. I turned to look but didn’t see anything, and a few minutes later, I heard another sound, this time from directly behind me. My blood ran cold as it dawned on me there were multiple people out there. I picked up the pace again, settling into a light jog. As if things weren’t terrifying enough already, I stumbled upon something that brought my panic levels from a five to a ten. There was a makeshift campsite literally tucked away in the woods. There were 12 or so logs sitting in a circle around a campfire. Someone had been here recently. I jogged around it and continued on, casting glances behind me every so often. A few minutes later, I heard something from my right this time. I turned quickly enough just to barely see someone’s foot jump behind a tree. That was it for me. My light jog instantly turned into a full-on sprint through the woods. I didn’t care how loud I was being. I needed to get out of that forest. As I ran, the sounds around me continued getting louder. It was clear that I was being chased. They weren’t even trying to hide it anymore. I continued running, afraid to look behind me. At one point, I couldn’t resist the urge anymore and shot a glance over my shoulder. I counted at least six people, all of whom were wearing white and charging toward me. I kept running, knowing my car wasn’t far. The next few minutes were the most terrifying moments I’ve ever experienced in my life. Imagine being overwhelmed with exhaustion while the threat of death looms over you. I couldn’t slow down; my life literally depended on it. Finally, I saw my car in the distance, and right behind it was a police officer. I reached his car and keeled over, almost throwing up before he even had a chance to speak. I turned around, and those people that had been chasing me were nowhere in sight. The cop told me that he had gone ahead and called AAA, which I was beyond thankful for. I gave him a full police report, and what he told me was chilling. Apparently, Utah houses the largest population of Mormons in the country, and it is not uncommon to encounter woods folk in unmarked forests. The specific forest I was exploring actually had a very rich history, especially as it pertains to woods cults and religious groups. The cop told me that I had probably stumbled upon one such group and that I was stupid to explore a random part of the woods. In all honesty, what that cop told me all those years ago was probably true. I still can’t wrap my head around this, though. If they were mad that I was infringing on their land, why not just tell me that? I don’t see why they’d feel the need to stalk and chase me through the woods, especially after slashing my tires. This experience is still something I think about all the time.
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
    # print(f"TTS dB level: {tts_db} dB")
    # print(f"Background music dB level before adjustment: {background_music_db} dB")
    
    # Ensure background music is lower in volume than TTS audio by a margin (e.g., 10 dB)
    target_db_difference = 5  # The desired difference between TTS and background music
    volume_adjustment = tts_db - background_music_db - target_db_difference
    
    # Adjust background music volume
    background_music = background_music + volume_adjustment
    # print(f"Background music dB level after adjustment: {background_music.dBFS} dB")
    
    # Overlay tts_audio on background_music for tts_audio duration
    mixed = tts_audio.overlay(background_music, position=0)
    
    # Apply fade-out to the last few seconds
    mixed = mixed.fade_out(fade_out_duration)
    
    # Export mixed audio
    mixed.export(output_path, format="mp3")
    print("Final mixed audio saved successfully.")

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
        mix_audio(OUTPUT_TTS_PATH, BACKGROUND_MUSIC_FOLDER,output_path=FINAL_OUTPUT_AUDIO_PATH, fade_out_duration=FADE_OUT_DURATION)
        
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












