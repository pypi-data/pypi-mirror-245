import click
import random
import os, shutil
import multiprocessing as mp
from pytube import Playlist, YouTube
from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips


def download_video(url):
    yt = YouTube(url)
    video_file = (
        yt.streams.filter(progressive=True, file_extension="mp4").first().download()
    )
    video = VideoFileClip(video_file)
    audio_file = yt.streams.filter(only_audio=True).last().download()
    audio = AudioFileClip(audio_file)

    dir, file_name = os.path.split(video_file)
    final_file = f"{dir}/final_{file_name}"
    final_clip = video.set_audio(audio)
    final_clip.write_videofile(final_file, fps=60)

    audio.close()
    video.close()
    final_clip.close()

    os.remove(video_file)
    os.remove(audio_file)

    return final_file


def stitch_clips(video_files, playlist_title):
    video_clips = []
    for video_file in video_files:
        clip = VideoFileClip(video_file)
        audio = AudioFileClip(video_file)
        clip = clip.set_audio(audio)
        video_clips.append(clip)
        audio.close()

    final_clip = concatenate_videoclips(video_clips, method="compose")
    final_clip.write_videofile(f"{playlist_title}.mp4", fps=60)

    for clip in video_clips:
        clip.close()
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
    video_urls = playlist.video_urls
    video_files = [download_video(url) for url in video_urls]
    stitch_clips(video_files, playlist.title)
    for file in video_files:
        # construct the full path of the file
        file_path = os.path.abspath(file)

        # check if file exists and is a regular file
        if os.path.isfile(file_path):
            # delete the file
            os.remove(file_path)
