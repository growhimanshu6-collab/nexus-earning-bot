import os
import time
import random
import asyncio
from google import genai
import edge_tts
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ColorClip, TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

# --- 1. DAILY FRESH EARNING IDEAS ---
CATEGORIES = [
    "Passive income apps like Honeygain and Pawns.app to earn money sharing bandwidth",
    "Best micro-task apps to earn daily cash by completing simple online surveys",
    "High-paying freelancing skills you can learn in 2026 with zero investment",
    "AI tools that can help students make $10 a day online",
    "Best websites to earn money by testing mobile games and apps",
    "Student side-hustles with no startup money required in 2026",
    "How to monetize short-form videos on YouTube Shorts and Instagram Reels"
]

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
MODELS_TO_TRY = ['gemini-2.0-flash-lite', 'gemini-1.5-flash-8b', 'gemini-2.0-flash']

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

# --- 3. PRO VIDEO ASSEMBLY ---
def create_video(category_name, audio_path="voice.mp3", output_path="final_short.mp4"):
    audio = AudioFileClip(audio_path)
    duration = audio.duration

    # Dark Premium Canvas (1080x1920 Shorts Format)
    bg = ColorClip(size=(1080, 1920), color=(15, 20, 32), duration=duration)
    
    # Header Tag
    header_clip = TextClip(
        text="🔥 NEXUS EARNING | DAILY SIDE-HUSTLE",
        font_size=42,
        color='cyan',
        font='Arial-Bold',
        method='caption',
        size=(950, None)
    ).with_position(('center', 250)).with_duration(duration)

    # Clean Highlight Card Title
    title_text = f"TODAY'S IDEA:\n\n{category_name.upper()}"
    title_clip = TextClip(
        text=title_text,
        font_size=52,
        color='yellow',
        font='Arial-Bold',
        method='caption',
        size=(900, None)
    ).with_position(('center', 500)).with_duration(duration)

    # Bottom Call to Action
    sub_clip = TextClip(
        text="👇 SUBSCRIBE FOR DAILY EARNING TIPS 👇",
        font_size=38,
        color='white',
        font='Arial-Bold',
        method='caption',
        size=(950, None)
    ).with_position(('center', 1500)).with_duration(duration)

    # Combine All Elements
    final_video = CompositeVideoClip([bg, header_clip, title_clip, sub_clip]).with_audio(audio)
    final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("[1/3] Selecting Fresh Idea & Generating Script...")
    script, category_name = generate_script()
    print(f"Selected Topic: {category_name}")
    print(f"Script: {script}\n")
    
    print("[2/3] Generating Voiceover...")
    asyncio.run(generate_audio(script))
    
    print("[3/3] Rendering Video...")
    create_video(category_name)
    
    print("✅ Pro Short Video Successfully Generated: final_short.mp4")
