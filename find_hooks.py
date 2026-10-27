import json
import re
import ast
from openai import OpenAI

def find_viral_hooks(transcript_file="transcript.json", output_file="clips.json"):
    print("🤖 Unbuilt AI: Analyzing transcript for viral moments...")
    
    with open(transcript_file, 'r', encoding='utf-8') as f:
        words = json.load(f)
        
    if len(words) == 0:
        print("❌ Error: Transcript is empty.")
        return

    text_with_times = ""
    for w in words:
        text_with_times += f"[{w['start']:.1f}s] {w['word']} "
        
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    
    # We added a strict "Example Format" to force the AI to behave
    prompt = f"""
    You are an expert short-form video editor. 
    Read the following transcript and find the single most viral, engaging 15-to-60-second segment.
    
    You MUST output valid JSON. Do not include markdown formatting.
    
    Example Output Format:
    [
      {{
        "start_time": 1.5,
        "end_time": 25.2,
        "title": "The Crazy Twist",
        "viral_score": 95,
        "explanation": "This part has a high-energy hook and a satisfying conclusion."
      }}
    ]
    
    Transcript: 
    {text_with_times}
    """
    
    try:
        print("🧠 Asking Local Llama 3.2 to find the best hook...")
        response = client.chat.completions.create(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        raw_output = response.choices[0].message.content.strip()
        match = re.search(r'\[.*\]', raw_output, re.DOTALL)
        
        if match:
            clean_json = match.group(0)
            
            try:
                # First try strict JSON parsing
                clips = json.loads(clean_json)
            except json.JSONDecodeError:
                # If it used single quotes, use Python's AST module to rescue it!
                print("⚠️ AI used invalid quotes. Engaging Python safety net...")
                clips = ast.literal_eval(clean_json)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(clips, f, indent=4)
                
            print(f"✅ Success! Found viral clip and saved to {output_file}")
            print(json.dumps(clips, indent=2))
        else:
            print("❌ Error: The AI did not output a valid JSON array.")
            print("Raw AI Output:\n", raw_output)
            
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        print("Raw AI Output:\n", raw_output if 'raw_output' in locals() else "None")

if __name__ == "__main__":
    find_viral_hooks()
