import json
import time
from faster_whisper import WhisperModel

def transcribe_video(video_path="input.mp4", output_json="transcript.json"):
    print("🤖 Unbuilt AI: Loading Whisper model...")
    
    model_size = "base"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    print(f"🎙️ Transcribing {video_path}...")
    start_time = time.time()
    
    segments, info = model.transcribe(video_path, word_timestamps=True)
    
    print(f"✅ Detected language: {info.language} (Probability: {info.language_probability:.2f})")
    
    word_level_data = []
    
    for segment in segments:
        for word in segment.words:
            word_level_data.append({
                "word": word.word.strip(),
                "start": word.start,
                "end": word.end
            })
            
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(word_level_data, f, indent=4, ensure_ascii=False)
        
    print(f"🚀 Transcription complete in {time.time() - start_time:.2f} seconds!")
    print(f"📁 Saved {len(word_level_data)} words to {output_json}")

if __name__ == "__main__":
    transcribe_video("input.mp4", "transcript.json")
