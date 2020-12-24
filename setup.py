from pathlib import Path
from setuptools import setup

long_description = Path("README.md").read_text()

setup(
    name="yourscript",
    version="1.0.1",
    author="Jani Šumak",
    author_email="jani.sumak@gmail.com",
    description="MacOS custom notifications manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dasdachs/macos-notifier",
    py_modules=["macos_notifier"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Darwin",
    ],
    python_requires=">=3.6",
    install_requires=[
        "Click",
        "Colorama",
        "python-crontab",
    ],
    entry_points="""
        [console_scripts]
        notifier=macos_notifier:cli
    """,
)
