from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.all import resize
from os import listdir
from os.path import isfile, join
import random

source_dir_files = listdir("sources")
# video_files = [name for name in source_dir_files if name.endswith(".mp4")]
video_files = [
    "Properties of Solutions #1_edited.mp4",
    "Properties of Solutions #2_edited.mp4",
    "Properties of Solutions #3_edited.mp4",
]

videos = []

for file_name in video_files:
    clip = VideoFileClip("outputs/" + file_name)
    videos.append(clip)
    print(clip.size)
    # clip = VideoFileClip("sources/videos/" + file_name)
    # length = clip.duration
    # frame_rate = clip.fps
    # size = clip.size
    # rotation = clip.rotation
    # if (
    #     length > 1
    #     and frame_rate == 30.0
    #     and (size == [1920, 1080] or size == [1280, 720])
    #     and rotation == 0
    # ):
    #     rand_time = random.randint(0, int(length) - 1)
    #     print(
    #         "Filename: "
    #         + file_name
    #         + "\t| Length: "
    #         + str(length)
    #         + "\t| Time Range: "
    #         + str(rand_time)
    #         + "-"
    #         + str(rand_time + 1)
    #         + "\t| Rotation: "
    #         + str(rotation)
    #         + "\t| Size: "
    #         + str(size)
    #     )
    #     if size == [1280, 720]:
    #         clip = clip.resize([1920, 1080])
    #     # print("Resized: " + str(clip.size))
    #     videos.append(clip.subclip(rand_time, rand_time + 1))
    # else:
    #     clip.close()

if len(videos) > 0:
    final_clip = concatenate_videoclips(videos)
    print(final_clip.size)
    final_clip.write_videofile(
        "outputs/Properties of Solutions Combined_output 2.mp4",
        codec="h264_videotoolbox",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
        audio_codec="aac",
        ffmpeg_params=["-vcodec", "h264_videotoolbox"],
        verbose=False,
        threads=6,
    )
else:
    print("No videos found with parameters")

