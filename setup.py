from setuptools import setup


setup(
    name="yourscript",
    version="1.0",
    py_modules=["notifier"],
    install_requires=[
        "Click",
        "Colorama",
        "python-crontab",
    ],
    entry_points="""
        [console_scripts]
        notifier=notifier:cli
    """,
)
