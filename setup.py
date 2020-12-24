from pathlib import Path
from setuptools import setup, find_packages

long_description = Path("README.md").read_text()

setup(
    name="macos-notifier",
    author="Jani Šumak",
    version="1.0.3",
    author_email="jani.sumak@gmail.com",
    description="MacOS custom notifications manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dasdachs/macos-notifier",
    py_modules=["macos_notifier"],
    packages=find_packages(),
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Environment :: MacOS X",
    ],
    python_requires=">=3.7",
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
