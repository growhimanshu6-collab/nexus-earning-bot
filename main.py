import os
import time
import random
import asyncio
from google import genai
import edge_tts
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ColorClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

# --- 1. SCRIPT GENERATION ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

CATEGORIES = [
    "Mobile apps that pay real cash for micro-tasks",
    "High-paying freelancing skills for beginners in 2026",
    "Best passive income tools & websites",
    "Student side-hustles with zero investment",
    "AI tools to make money online"
]

# Alternate models to try if quota hits
MODELS_TO_TRY = ['gemini-2.0-flash-lite', 'gemini-1.5-flash-8b', 'gemini-2.0-flash']

def generate_script():
    category = random.choice(CATEGORIES)
    prompt = f"""
    You are an expert content creator for YouTube channel 'Nexus Earning'.
    Write a fast-paced, highly engaging 25-second YouTube Short script in Hinglish about '{category}'.
    Rules:
    - Language: Energetic Hinglish (Hindi + English).
    - Output: Plain spoken text ONLY. No brackets, no captions, no metadata.
    """
    
    for model_name in MODELS_TO_TRY:
        try:
            print(f"Trying model: {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            print(f"⚠️ {model_name} failed: {e}")
            time.sleep(2)
            
    # Backup script if API quotas fail completely
    print("⚠️ API Quotas completely exhausted, using smart template script...")
    return f"Kya aapko pata hai ki {category} se aap daily achhi earning kar sakte hain? Bas sahi AI tools aur platforms ka use karna hai. Aaj hi Nexus Earning par bio link check karein aur start karein!"

# --- 2. VOICEOVER GENERATION ---
async def generate_audio(text, output_file="voice.mp3"):
    communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural")
    await communicate.save(output_file)

# --- 3. VIDEO CREATION ---
def create_video(audio_path="voice.mp3", output_path="final_short.mp4"):
    audio = AudioFileClip(audio_path)
    
    # 1080x1920 Vertical Canvas (Shorts Format)
    bg = ColorClip(size=(1080, 1920), color=(15, 23, 42), duration=audio.duration)
    
    # Merge Video & Audio
    final_video = CompositeVideoClip([bg]).with_audio(audio)
    final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("[1/3] Generating AI Script...")
    script = generate_script()
    print(f"Script: {script}\n")
    
    print("[2/3] Generating Voiceover...")
    asyncio.run(generate_audio(script))
    
    print("[3/3] Assembling Video...")
    create_video()
    
    print("✅ Video Successfully Generated: final_short.mp4")
