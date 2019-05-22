from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import random
from numpy import array
import numpy as np
import math
from datetime import datetime, timedelta
import os
import argparse
import youtube_dl

ap = argparse.ArgumentParser()
ap.add_argument("-u", help="txt file containing list of urls", required=True)
ap.add_argument(
    "-o", help="what to name the output file (no file extensions", required=True
)
args = ap.parse_args()

total_start_time = datetime.now().replace(microsecond=0)

FRAME_BUFFER = 5
URLS_PATH = args.u
URLS = []
OUTPUT_NAME = args.o

ydl_opts = {
    "format": "mp4",
    "limit-rate": "100M",
    "outtmpl": "temp/youtube/%(id)s.%(ext)s",
}


print("------")
print("WELCOME TO YOUTUBE VIDEO SHORTENER/COMPILER")
print("------")

with open(URLS_PATH, "r") as reader:
    URLS = reader.read().split("\n")
    # print(URLS)

while len(URLS) > 0:
    video_url = URLS[0]
    if video_url == "":
        break
    video_id = video_url.split("/")[-1]

    if os.path.isfile("temp/youtube/" + video_id + "_temp.mp4"):
        print("Video " + video_id + " has already been cached...")
    else:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            playlist_dict = ydl.download([video_url])
            print("Downloaded " + video_id)

            clip = VideoFileClip("temp/youtube/" + video_id + ".mp4")
            # print("loaded - " + file_name)

            print("------")
            print('loading "' + video_id + '" + getting video metadata...')
            print("------")

            length = clip.duration
            frame_rate = clip.fps
            size = clip.size
            rotation = clip.rotation

            new_clip = None

            if (
                length > 1
                and frame_rate == 30.0
                and (size == [1920, 1080] or size == [1280, 720])
                and rotation == 0
            ):
                rand_time = random.randint(0, int(length) - 1)
                if size == [1280, 720]:
                    clip = clip.resize([1920, 1080])
                # print("Resized: " + str(clip.size))
                new_clip = clip.subclip(rand_time, rand_time + 1)
                new_clip.write_videofile(
                    "temp/youtube/" + video_id + "_temp.mp4",
                    # codec="h264_videotoolbox",
                    temp_audiofile="temp/youtube/temp-audio.m4a",
                    # bitrate="500000",
                    remove_temp=True,
                    audio_codec="aac",
                    ffmpeg_params=[
                        "-vcodec",
                        "h264_videotoolbox",
                        "-b:v",
                        "5000K",
                        "-bufsize",
                        "10000K",
                    ],
                    verbose=False,
                    logger=None,
                    threads=8,
                )
            os.remove("temp/youtube/" + video_id + ".mp4")
            URLS = URLS[1:]
            with open(URLS_PATH, "w") as writer:
                writer.write("\n".join(URLS))

            print("------")
            print(str(((1 - (len(URLS) / 137)) * 100)) + "% DONE")
            print("------")

print("------")
print("loading + compiling videos...")
print("------")

TEMP_VIDEOS = [name for name in os.listdir("temp/youtube") if name.endswith(".mp4")]
video_chunks = []

for i in range(0, len(TEMP_VIDEOS), 10):
    video_chunks.append(TEMP_VIDEOS[i : i + 10])

for chunk_index in range(0, len(video_chunks)):
    if os.path.isfile("temp/youtube/chunks/chunk" + str(chunk_index) + ".mp4"):
        print(
            "[cached] chunk "
            + str(chunk_index + 1)
            + " of "
            + str(len(video_chunks))
            + "..."
        )
        continue
    print(
        "[loading] chunk "
        + str(chunk_index + 1)
        + " of "
        + str(len(video_chunks))
        + "..."
    )

    videos = []

    for file_name in video_chunks[chunk_index]:
        video = VideoFileClip("temp/youtube/" + file_name)
        videos.append(video)

    compiled_clip = concatenate_videoclips(videos)
    compiled_clip.write_videofile(
        "temp/youtube/chunks/chunk" + str(chunk_index) + ".mp4",
        temp_audiofile="temp/youtube/temp-audio.m4a",
        remove_temp=True,
        audio_codec="aac",
        ffmpeg_params=[
            "-vcodec",
            "h264_videotoolbox",
            "-b:v",
            "5000K",
            "-bufsize",
            "10000K",
        ],
        verbose=False,
        logger=None,
        threads=8,
    )

    compiled_clip.close()
    video.close()
    for v in videos:
        v.close()

    print(
        "[exported] chunk "
        + str(chunk_index + 1)
        + " of "
        + str(len(video_chunks))
        + "..."
    )

print("------")
print("compiling chunks...")
print("------")

chunks = []

for chunk_index in range(0, len(video_chunks)):
    video = VideoFileClip("temp/youtube/chunks/chunk" + str(chunk_index) + ".mp4")
    chunks.append(video)

compiled_clip = concatenate_videoclips(chunks)
compiled_clip.write_videofile(
    "outputs/youtube/" + OUTPUT_NAME + ".mp4",
    temp_audiofile="temp/youtube/temp-audio.m4a",
    remove_temp=True,
    audio_codec="aac",
    ffmpeg_params=[
        "-vcodec",
        "h264_videotoolbox",
        "-b:v",
        "5000K",
        "-bufsize",
        "10000K",
    ],
    verbose=False,
    logger=None,
    threads=8,
)


print("------")
print("cleaning up...")
print("------")

# for file_name in TEMP_VIDEOS:
#     os.remove("temp/youtube/" + file_name)

compiled_clip.close()
video.close()
for v in chunks:
    v.close()

total_end_time = datetime.now().replace(microsecond=0)

print("------")
print(
    "Thanks to Bradley for making this! Total time to make this video: "
    + str(total_end_time - total_start_time)
)
print("Have a great day! Enjoy the video!")
print("------")

