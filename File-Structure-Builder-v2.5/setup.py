from setuptools import setup, find_packages
import sys

# Application metadata
APP_NAME = "File Structure Builder"
VERSION = "3.0"
DESCRIPTION = "AI-Powered Project Structure Generator"
AUTHOR = "Your Name"

# Dependencies
REQUIREMENTS = [
    'tkinter',
    'pyinstaller>=5.0',
    'setuptools>=60.0'
]

setup(
    name=APP_NAME.replace(" ", "-").lower(),
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'file-structure-builder=optimized_main:main',
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)