import subprocess
from datetime import datetime, timezone
from pathlib import Path

from setuptools import find_packages, setup


def shell(*args):
    out = subprocess.check_output(args)
    return out.decode("ascii").strip()


def write_version(version_core, dev=True):
    if dev:
        last_commit_time = shell("git", "log", "-1", "--format=%cd", "--date=iso-strict")
        last_commit_time = datetime.strptime(last_commit_time, "%Y-%m-%dT%H:%M:%S%z")
        last_commit_time = last_commit_time.astimezone(timezone.utc)
        last_commit_time = last_commit_time.strftime("%y%m%d%H%M%S")
        version = f"{version_core}-dev{last_commit_time}"
    else:
        version = version_core

    with open(Path("resemble_enhance", "version.py"), "w") as f:
        f.write('__version__ = "{}"\n'.format(version))

    return version


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="resemble-enhance",
    python_requires=">=3.10",
    version=write_version("0.0.1"),
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "celluloid==0.2.0",
        "deepspeed==0.12.4",
        "librosa==0.10.1",
        "matplotlib==3.8.1",
        "numpy==1.26.2",
        "omegaconf==2.3.0",
        "pandas==2.1.3",
        "ptflops==0.7.1.2",
        "rich==13.7.0",
        "scipy==1.11.4",
        "soundfile==0.12.1",
        "torch==2.1.1",
        "torchaudio==2.1.1",
        "torchvision==0.16.1",
        "tqdm==4.66.1",
        "resampy==0.4.2",
        "tabulate==0.8.10",
        "gradio==4.8.0",
    ],
    url="https://github.com/resemble-ai/resemble-enhance",
    author="Resemble AI",
    author_email="team@resemble.ai",
    entry_points={
        "console_scripts": [
            "resemble-enhance=resemble_enhance.enhancer.__main__:main",
        ]
    },
)
