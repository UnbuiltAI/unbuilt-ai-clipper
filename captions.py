import json
import pysubs2
import subprocess
import imageio_ffmpeg

def create_captions():
    print("📝 Unbuilt AI: Generating dynamic captions...")
    
    # 1. Load the clip timestamps
    try:
        with open('clips.json', 'r') as f:
            clip_data = json.load(f)[0]
            clip_start = clip_data['start_time']
            clip_end = clip_data['end_time']
    except Exception as e:
        print("❌ Error loading clips.json.")
        return
        
    # 2. Load the full transcript
    with open('transcript.json', 'r', encoding='utf-8') as f:
        all_words = json.load(f)
        
    # 3. Filter words that belong ONLY to this clip
    clip_words = []
    for w in all_words:
        if w['start'] >= clip_start - 0.5 and w['end'] <= clip_end + 0.5:
            clip_words.append(w)
            
    if not clip_words:
        print("❌ No words found in this timeframe! Try generating a different clip.")
        return
        
    # 4. Create the OpusClip Style Subtitles
    subs = pysubs2.SSAFile()
    style = pysubs2.SSAStyle()
    style.fontname = "Arial Black"
    style.fontsize = 130  # Huge TikTok style text
    style.primarycolor = pysubs2.Color(0, 255, 255) # Yellow Text
    style.outlinecolor = pysubs2.Color(0, 0, 0) # Black outline
    style.outline = 6
    style.shadow = 4
    style.alignment = 2 # Bottom center
    style.marginv = 300 # Push it up from the very bottom
    
    subs.styles["OpusStyle"] = style
    
    # 5. Flash 1-2 words on the screen at a time
    for w in clip_words:
        start_ms = int((w['start'] - clip_start) * 1000)
        end_ms = int((w['end'] - clip_start) * 1000)
        
        if start_ms < 0: start_ms = 0
        if end_ms < 0: end_ms = 100
            
        event = pysubs2.SSAEvent(start=start_ms, end=end_ms, text=w['word'].upper(), style="OpusStyle")
        subs.events.append(event)
        
    subs.save("subtitles.ass")
    print("✅ Subtitles file generated as subtitles.ass")
    
    # 6. Burn subtitles using our hidden Python FFmpeg!
    print("🔥 Burning subtitles onto video using Hacker FFmpeg...")
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    
    try:
        subprocess.run([
            ffmpeg_path, "-y", "-i", "temp_clip.mp4", 
            "-vf", "ass=subtitles.ass", 
            "-c:a", "copy", "final_short.mp4"
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("🎉 SUCCESS! Your final AI-generated Short is saved as final_short.mp4!")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ FFmpeg crashed while rendering. Error code: {e.returncode}")

if __name__ == "__main__":
    create_captions()
