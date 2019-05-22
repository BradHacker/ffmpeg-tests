import youtube_dl
import os

ydl_opts = {
    "ignoreerrors": True,
    "quiet": True,
    "extract_flat": True,
    "dateafter": "now-6months",
}
# ydl_opts = {
#     "format": "mp4",
#     "limit-rate": "100M",
#     "outtmpl": "%(playlist_id)s/%(title)s.%(ext)s",
# }
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    playlist_dict = ydl.extract_info(
        "https://www.youtube.com/playlist?list=PL7KjeWtXBx-n2f6xq83InBvWJhvTqgQag",
        download=False,
    )

    urls = []

    for video in playlist_dict["entries"]:
        if not video:
            print("NO VIDEO PRESENT")
            continue
        else:
            # print(video.keys())
            urls.append("https://youtu.be/" + video.get("url") + "\n")

    print("Found", len(playlist_dict["entries"]), "videos")
    with open("urls.txt", "w") as writer:
        writer.writelines(urls)
        print("Wrote to urls.txt")

print("done!")
