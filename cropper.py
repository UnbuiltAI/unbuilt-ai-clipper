import json
import cv2
import numpy as np
from moviepy import VideoFileClip

def crop_to_vertical():
    print("🎬 Unbuilt AI: Starting the Video Editor...")
    
    try:
        with open('clips.json', 'r') as f:
            clips = json.load(f)
            clip_data = clips[0]
            start_time = clip_data['start_time']
            end_time = clip_data['end_time']
    except Exception as e:
        print("❌ Error loading clips.json.")
        return
        
    print(f"✂️ Cutting video from {start_time}s to {end_time}s...")
    
    # Load video
    video = VideoFileClip("input.mp4").subclipped(start_time, end_time)
    
    # THE PIVOT: Use OpenCV's built-in Face Tracking AI instead of MediaPipe
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    width = video.w
    height = video.h
    target_width = int(height * 9 / 16)
    
    def process_frame(frame):
        # Convert frame to grayscale for the AI brain to process faster
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        # Scan for faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
        
        # Default to center of screen
        center_x = width // 2
        
        if len(faces) > 0:
            # If multiple faces/objects found, grab the largest one (the speaker)
            faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)
            x, y, w, h = faces[0]
            center_x = x + (w // 2)
            
        # Keep the crop window inside the video boundaries
        x1 = max(0, center_x - target_width // 2)
        x2 = x1 + target_width
        
        if x2 > width:
            x2 = width
            x1 = width - target_width
        elif x1 < 0:
            x1 = 0
            x2 = target_width
            
        # Cut the video and resize to TikTok/Shorts format (1080x1920)
        cropped_frame = frame[:, x1:x2]
        return cv2.resize(cropped_frame, (1080, 1920))

    print("🤖 Tracking face using OpenCV and cropping to 9:16...")
    
    # Apply our face-tracking AI to every single frame of the video
    vertical_video = video.image_transform(process_frame)
    
    # Export the final video
    output_filename = "temp_clip.mp4"
    vertical_video.write_videofile(
        output_filename, 
        codec="libx264", 
        audio_codec="aac", 
        preset="ultrafast", 
        threads=4,
        logger=None
    )
    print(f"✅ Success! Vertical video saved as {output_filename}")

if __name__ == "__main__":
    crop_to_vertical()
