import os
import time
import random
import asyncio
import requests
from google import genai
import edge_tts
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ColorClip, TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

# --- 1. DAILY FRESH EARNING IDEAS ---
CATEGORIES = [
    "Passive income apps like Honeygain to earn money sharing internet",
    "Best micro-task apps to earn daily cash completing online surveys",
    "High-paying freelancing skills you can learn with zero investment",
    "AI tools that can help students make side income online",
    "Best websites to earn money by testing mobile games and apps",
    "Student side-hustles with no startup money required",
    "How to monetize short-form videos on YouTube Shorts and Instagram Reels"
]

# Direct HD Stock Video URLs (Working CDN Links)
STOCK_BG_VIDEOS = [
    "https://cdn.pixabay.com/video/2021/04/12/70886-536968724_large.mp4",
    "https://cdn.pixabay.com/video/2019/04/20/22906-331575797_large.mp4",
    "https://cdn.pixabay.com/video/2020/05/25/40149-425211993_large.mp4"
]

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
MODELS_TO_TRY = ['gemini-2.0-flash-lite', 'gemini-1.5-flash', 'gemini-2.0-flash']

def generate_script():
    category = random.choice(CATEGORIES)
    prompt = f"""
    You are an expert creator for YouTube Shorts channel 'Nexus Earning'.
    Write an energetic, fast-paced 20-second Hinglish script about '{category}'.
    Rules:
    - Start with a strong hook phrase in Hindi/Hinglish.
    - Keep it crisp, exciting, and realistic.
    - Plain spoken text ONLY. No brackets, no emojis, no stage directions.
    """
    
    if client:
        for model_name in MODELS_TO_TRY:
            try:
                print(f"Generating script using model: {model_name}...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                return response.text.strip(), category
            except Exception as e:
                print(f"⚠️ {model_name} quota/error: {e}")
                time.sleep(1)
                
    # Direct smart fallback script if API limit hits
    print("⚠️ Using built-in smart fallback template for script...")
    fallback_script = f"Kya aapko pata hai ki {category} se aap daily ghar baithe achhi earning kar sakte hain? Bas sahi platforms aur smart tools ka setup chahiye. Nexus Earning ko abhi subscribe karein aur daily direct side-hustles seekhein!"
    return fallback_script, category

# --- 2. VOICEOVER GENERATION ---
async def generate_audio(text, output_file="voice.mp3"):
    communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural")
    await communicate.save(output_file)

# --- 3. DOWNLOAD BACKGROUND VIDEO (FIXED 403 ERROR) ---
def download_bg_video(output_path="bg_clip.mp4"):
    video_url = random.choice(STOCK_BG_VIDEOS)
    print(f"Downloading background stock video from: {video_url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(video_url, headers=headers, stream=True)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("✅ Background Video Downloaded Successfully!")
    except Exception as e:
        print(f"⚠️ Download failed ({e}), creating fallback canvas...")
        # Fallback empty video file marker

# --- 4. PRO VIDEO ASSEMBLY WITH VIDEO BACKGROUND ---
def create_video(category_name, audio_path="voice.mp3", bg_video_path="bg_clip.mp4", output_path="final_short.mp4"):
    audio = AudioFileClip(audio_path)
    duration = audio.duration

    # Load Background Stock Video Clip
    if os.path.exists(bg_video_path) and os.path.getsize(bg_video_path) > 1000:
        try:
            bg_clip = VideoFileClip(bg_video_path).without_audio()
            if bg_clip.duration < duration:
                bg_clip = bg_clip.loop(duration=duration)
            else:
                bg_clip = bg_clip.subclip(0, duration)
            
            bg_clip = bg_clip.resized(height=1920)
            bg_clip = bg_clip.cropped(x_center=bg_clip.w/2, width=1080)
        except Exception as e:
            print(f"⚠️ Video processing error: {e}, fallback canvas used")
            bg_clip = ColorClip(size=(1080, 1920), color=(15, 23, 42), duration=duration)
    else:
        bg_clip = ColorClip(size=(1080, 1920), color=(15, 23, 42), duration=duration)

    # Top Header Tag
    header_clip = TextClip(
        text="NEXUS EARNING | DAILY SIDE-HUSTLE",
        font_size=36,
        color='cyan',
        method='caption',
        size=(850, None)
    ).with_position(('center', 250)).with_duration(duration)

    # Main Idea Title Card
    formatted_category = category_name.upper().replace(" ON ", "\nON ").replace(" AND ", "\nAND ")
    title_text = f"TODAY'S IDEA:\n\n{formatted_category}"
    
    title_clip = TextClip(
        text=title_text,
        font_size=42,
        color='yellow',
        method='caption',
        size=(820, None)
    ).with_position(('center', 550)).with_duration(duration)

    # Bottom Call to Action
    sub_clip = TextClip(
        text="SUBSCRIBE FOR DAILY EARNING TIPS",
        font_size=34,
        color='white',
        method='caption',
        size=(850, None)
    ).with_position(('center', 1500)).with_duration(duration)

    # Merge Video Clip, Text & Voice Audio
    final_video = CompositeVideoClip([bg_clip, header_clip, title_clip, sub_clip]).with_audio(audio)
    final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("[1/4] Selecting Fresh Idea & Generating Script...")
    script, category_name = generate_script()
    print(f"Selected Topic: {category_name}")
    print(f"Script: {script}\n")
    
    print("[2/4] Generating Voiceover...")
    asyncio.run(generate_audio(script))
    
    print("[3/4] Downloading Royalty-Free Stock Video...")
    download_bg_video()
    
    print("[4/4] Rendering Final Video with Video Background...")
    create_video(category_name)
    
    print("✅ Pro Short Video Successfully Generated: final_short.mp4")
