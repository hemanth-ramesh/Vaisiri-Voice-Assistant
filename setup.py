"""
Setup script for Vaisiri Voice Assistant
"""
from setuptools import setup, find_packages

setup(
    name="vaisiri-voice-assistant",
    version="1.0.0",
    description="A modular voice assistant",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "vaisiri=vaisiri.main:main",
        ],
    },
)
