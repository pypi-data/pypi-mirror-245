# YouTube Playlist Downloader & Stitcher

<img src="./youtools.jpeg" alt="youtools" style="width:25vw; min-width: 200px; max-width: 400px; display: block; margin-left: auto; margin-right: auto;"/>
</br></br>

### A command-line tool that allows you to download all videos in a YouTube playlist and stitch them together into a single video.

## Dependencies

### FFmpeg

#### MacOS

```bash
brew update
brew upgrade
brew install ffmpeg
```

## Installation

You can install playlist-stitcher directly from PyPI:

```bash
pip install playlist-stitcher
```

## Usage

After installation, you can use the tool directly from your shell:

```bash
playlist-stitcher stitch "PLAYLIST_URL"
```

Replace "PLAYLIST_URL" with the URL of the YouTube playlist you want to download and stitch.

## How does it work

- Downloads all videos in a YouTube playlist
- Stitches downloaded videos into a single video
- Deletes the individual videos

## Features

- Easy to install and use

## Contributing

- Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Making changes

- Feel free to use the makefile + Docker workflow that is provided
- `make container`: builds and runs the docker container
- `make run`: runs an existing built container
- `make build`: builds the cli and installs it
- `playlist-stitcher`: commands to run the CLI after building it with make build

## License

[License](./LICENSE)
