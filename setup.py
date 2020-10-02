import setuptools

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name="spotidex-redbrickhut",
    version="1.0",
    author="James Menzies",
    author_email="james.r.menzies@gmail.com",
    description="A classical companion for Spotify",
    long_description="A companion app for Spotify "
                     "so that the listener can get a greater "
                     "appreciation and context for what they're listening to.",
    url="https://github.com/redbrickhut/spotidex",
    packages=setuptools.find_packages(),
    install_requires=[
        'google',
        'beautifulsoup4',
        'requests',
        'spotipy',
        'urwid',
    ],
    entry_points={
      "console_scripts": [
          "spotidex = spotidex.__main__:main"
      ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Unix",
    ],
    python_requires='>=3.6'
)