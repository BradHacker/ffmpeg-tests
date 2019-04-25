from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import random
from numpy import array
import numpy as np
import math
from datetime import datetime, timedelta
import os

total_start_time = datetime.now().replace(microsecond=0)

FRAME_BUFFER = 5
VIDEO_FILES = ["clarke_imf.mp4", "bonding_in_solids.mp4"]
OUTPUT_NAME = "Bonding"

print("------")
print("WELCOME TO CLARKE'S VIDEO SHORTENER/COMPILER")
print("------")


for file_name in VIDEO_FILES:
    if os.path.isfile("temp/" + file_name + "_temp.mp4"):
        print('"' + file_name + '" has already been cached...')
    else:
        video = VideoFileClip("sources/videos/" + file_name)
        # print("loaded - " + file_name)

        print("------")
        print('loading "' + file_name + '" + getting video metadata...')
        print("------")

        # Video
        # video = VideoFileClip("temp/" + OUTPUT_NAME + "_temp.mp4")
        video_fps = int(video.fps)
        video_frame_count = video_fps * video.duration

        # Audio
        audio = video.audio.to_soundarray()
        audio_sample_rate = int(video.audio.fps)
        audio_total_frames = len(audio)
        samples_per_frame = int(audio_sample_rate / video_fps)
        audio_frame_count = int(math.ceil(audio_total_frames / samples_per_frame))

        print("------")
        print("Num video frames: " + str(video.fps * video.duration))
        print("Video fps: " + str(video.fps) + "fps")
        print("Audio sample rate: " + str(video.audio.fps) + "Hz")
        print(
            "Projected "
            + str(audio_sample_rate)
            + "Hz audio frames: "
            + str(audio_sample_rate * video.duration)
        )
        print("Num audio frames: " + str(len(audio)))
        print("Samples per frame: " + str(samples_per_frame))
        print("Audio frame count: " + str(audio_frame_count))
        # print(audio[random.randint(0, len(audio) - 1)][0])
        print("------")

        ten_percent_step = int(audio_frame_count / 10)

        test_vols = [x[0] for x in audio]

        avg_vol = np.average(test_vols)
        min_vol = np.min(test_vols)
        max_vol = np.max(test_vols)

        print("------")
        print("analyzing audio...")
        print("------")

        print("------")
        frame_analysis = np.zeros((audio_frame_count))
        chunk_vols = np.zeros((audio_frame_count))

        for i in range(audio_frame_count):
            start = int(i * samples_per_frame)
            end = min(int((i + 1) * samples_per_frame), audio_total_frames)
            # print("Start: " + str(start) + " | End: " + str(end))
            audio_chunk = test_vols[start:end]

            max_chunk_vol = max(np.max(audio_chunk), -np.min(audio_chunk)) / max_vol
            chunk_vols[i] = max_chunk_vol

            if max_chunk_vol >= 0.1:
                for j in range(
                    max(0, i - FRAME_BUFFER), min(audio_frame_count, i + FRAME_BUFFER)
                ):
                    frame_analysis[j] = 1

            if i % ten_percent_step == 0:
                print(str(int(i / ten_percent_step * 10)) + "% done")

        chunks = []
        start = 0

        while start < audio_frame_count:
            # print("start" + str(start))
            # print("range: " + str(audio_frame_count - start - 1))
            if frame_analysis[start] > 0:
                found = False
                for j in range(audio_frame_count - start):
                    # print("check: " + str(start + j))
                    if frame_analysis[start + j] == 0:
                        # print("found at: " + str(start + j))
                        chunks.append([start / video_fps, (start + j) / video_fps])
                        start += j
                        found = True
                        break
                if found == False:
                    # print("found at: " + str(start + j))
                    chunks.append(
                        [start / video_fps, (audio_frame_count - 1) / video_fps]
                    )
                    start = audio_frame_count
            else:
                start += 1

        talking_frame_count = np.count_nonzero(frame_analysis)

        # print("Talking Points Frames: " + str(len(talking_points)))
        # print("Total Talking time: " + str(talking_frame_count / video_fps))
        # print(
        #     "Total time removed: " + str((video_frame_count - talking_frame_count) / video_fps)
        # )
        # print("max volume: " + str(min(max_vol, -min_vol)))
        # print("chunks: " + str(chunks))
        print("------")

        old_length = video.duration
        new_duration = talking_frame_count / video_fps

        print("------")
        print(
            "Old Video Length: "
            + str(int(video.duration / 60))
            + ":"
            + str(math.ceil(video.duration % 59))
        )
        print(
            "New Video Length: "
            + str(int(new_duration / 60))
            + ":"
            + str(math.ceil(new_duration % 59))
        )
        print("------")

        video_chunks = []

        print("------")
        print("splitting video...")
        print("------")

        for video_range in chunks:
            video_chunks.append(video.subclip(video_range[0], video_range[1]))

        # start_time = datetime.now().replace(microsecond=0)

        # print("------")
        # print("starting encoding at: " + str(start_time))
        # print("------")
        final_clip = concatenate_videoclips(video_chunks)
        final_clip.write_videofile(
            "temp/" + file_name + "_temp.mp4",
            # codec="h264_videotoolbox",
            temp_audiofile="temp/temp-audio.m4a",
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

        # end_time = datetime.now().replace(microsecond=0)

        # print("------")
        # print("done encoding at: " + str(end_time))
        # print("total encoding time: " + str(end_time - start_time))
        # print("------")
        # start_time = datetime.now()

print("------")
print("loading + compiling videos...")
print("------")

videos = []

for file_name in VIDEO_FILES:
    video = VideoFileClip("temp/" + file_name + "_temp.mp4")
    videos.append(video)

compiled_clip = concatenate_videoclips(videos)
compiled_clip.write_videofile(
    "outputs/" + OUTPUT_NAME + ".mp4",
    temp_audiofile="temp/temp-audio.m4a",
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

for file_name in VIDEO_FILES:
    os.remove("temp/" + file_name + "_temp.mp4")

final_clip.close()
video.close()
for v in video_chunks:
    v.close()

total_end_time = datetime.now().replace(microsecond=0)

print("------")
print(
    "Thanks to Bradley for making this! Total time to make this video: "
    + str(total_end_time - total_start_time)
)
print("Have a great day! Enjoy the video!")
print("------")

