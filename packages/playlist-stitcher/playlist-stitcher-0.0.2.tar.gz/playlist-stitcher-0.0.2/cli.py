import click
import os, shutil
import multiprocessing as mp
from pytube import Playlist, YouTube
from moviepy.editor import VideoFileClip, concatenate_videoclips


def download_video(url):
    yt = YouTube(url)
    video = (
        yt.streams.filter(progressive=True, file_extension="mp4")
        .order_by("resolution")
        .desc()
        .first()
    )
    video.download()
    return video.default_filename


def stitch_clips(video_files, playlist_title):
    video_clips = []
    for video_file in video_files:
        clip = VideoFileClip(video_file)
        video_clips.append(clip)

    final_clip = concatenate_videoclips(video_clips, method="compose")
    final_clip.write_videofile(f"{playlist_title}.mp4", fps=25)
    final_clip.close()


@click.group()
def cli():
    pass


@cli.command(help="Download and stitch a YouTube playlist")
@click.argument("url")
def stitch(url):
    click.confirm(
        """This will
        \t1.Download the video files to the current directory
        \t2.Stitch them together in a single video that will be placed in the current directory
        \t3.Then delete the individual video files.
        \nContinue?""",
        abort=True,
    )
    playlist = Playlist(url)
    pool = mp.Pool(processes=10)  # Set the number of processes to use
    video_urls = playlist.video_urls
    video_files = pool.map(download_video, video_urls)
    stitch_clips(video_files, playlist.title)
    for file in video_files:
        # construct the full path of the file
        file_path = os.path.abspath(file)

        # check if file exists and is a regular file
        if os.path.isfile(file_path):
            # delete the file
            os.remove(file_path)
