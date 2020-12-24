# MacOS Notifier

Cli application to set and manage custom MacOS notifications using crontab and apple script.


## Usage

```bash
Usage: notifier.py [OPTIONS] COMMAND [ARGS]...

  Create and manage MacOS custom notifications with crontabs.

Options:
  --help  Show this message and exit.

Commands:
  cancel  Cancel, list and deactivate jobs
  create  Create MacOS notifications in crontabs
```

## Installation

Since this is a cli application the recommended installation
is to use [pipx](https://pipxproject.github.io/pipx/)

```bash
pipx install macos-notifier
```

Or use `pip`

```bash
pip install -U macos-notifier
```

If you want to live on the edge you can clone and install it yourself

```bash
git clone https://github.com/dasdachs/macos-notifier .
pip install -e .
```

## Development

The project uses [poetry](https://python-poetry.org/) for dependencies management, so
make sure you have it installed before you start.

The clone the repository

```bash
git clone https://github.com/dasdachs/macos-notifier .
```

And install the dependencies

```bash
poetry install
```

## Misc

If you have any questions or suggestions just reach out to me via mail or
[twitter](https://twitter.com/dasdachs).
