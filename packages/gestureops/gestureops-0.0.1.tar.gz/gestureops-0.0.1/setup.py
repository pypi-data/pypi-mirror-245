from setuptools import setup, find_packages
import codecs
import os



VERSION = '0.0.1'
DESCRIPTION = 'Basic Package For Hand-Gesture-Driven Computer Operations'
LONG_DESCRIPTION = 'A package that allows to build simple hand gesture based computer commanding system.'

# Setting up
setup(
    name="gestureops",
    version=VERSION,
    author="Charan K",
    author_email="<charankulal0241@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python', 'pyautogui','pycaw', 'mediapipe','numpy'],
    keywords=['python', 'hand tracking', 'hand gestures', 'computer vision'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)