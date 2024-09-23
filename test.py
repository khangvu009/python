print("Hello, World!")
#from pytube import YouTube
#YouTube('https://youtu.be/2lAe1cqCOXo').streams.first().download()
#yt = YouTube('http://youtube.com/watch?v=2lAe1cqCOXo')

#yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()

from audio_extract import extract_audio

extract_audio(input_path="./1.mp4", output_path="./3.mp3")

from moviepy.editor import VideoFileClip

# Replace 'your_video.mp4' with the path to your video file
video_path = '1.mp4'
audio_path = '1.mp3'

# Load the video file
video_clip = VideoFileClip(video_path)

# Extract the audio
audio_clip = video_clip.audio

# Write the audio file
audio_clip.write_audiofile(audio_path)

# Close the clips to release resources
video_clip.close()
audio_clip.close()

print(f"Audio extracted and saved to {audio_path}")
