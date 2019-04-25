from moviepy.audio.io.AudioFileClip import AudioFileClip

audio = AudioFileClip("sources/music/test.mp3")

print(audio.to_soundarray())
