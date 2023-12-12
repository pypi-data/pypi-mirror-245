from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="arpit",
    version="0.1.2.6",
    author="Masti Khor (arpy8)",
    author_email="arpitsengar99@gmail.com",
    description="Hi stranger! ssup?",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arpy8/arpit",
    packages=find_packages(),
    install_requires=["pygame", "termcolor", "pyautogui", "keyboard", "opencv-python"],
    entry_points={
        "console_scripts": [
            "arpit=arpit.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'arpit': ['assets/*.mp3', 'assets/*.mp4', 'assets/*.json']},
    include_package_data=True,
    license="MIT"
)