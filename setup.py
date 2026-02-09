from setuptools import setup, find_packages

setup(
    name="Transcription & Translation Service",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "moviepy>=2.2.1",
        "openai>=2.16.0",
        "pydub>=0.25.1",
        "python-dotenv>=1.2.1",
        "setuptools>=82.0.0"
    ],
    entry_points={
        'console_scripts': [
            'app=main:main',
        ],
    },
)