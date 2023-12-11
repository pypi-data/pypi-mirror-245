from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name="playlist-stitcher",
    version="0.0.7",
    author="Chen Stanilovsky",
    author_email="chen.stanilovsky@gmail.com",
    license="GNU GPLv3",
    description="A tool to download and stitch YouTube playlists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/you-tools/playlist-stitcher",
    py_modules=["cli"],
    packages=find_packages(),
    install_requires=[requirements],
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "playlist-stitcher=cli:cli",
        ]
    },
)
