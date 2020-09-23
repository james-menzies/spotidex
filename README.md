# Spotidex
### A Classical Companion for Spotify

>Please note that this application is currently under development, and that 
>v1.0 of the program is due on the 2nd October 2020 as part of my assessment
>for the Coder Academy 2020 CCC course. For ease of editing, this document will 
>be written in the present tense for features not yet implemented.

This terminal application is designed to run alongside an active Spotify 
session, passively using the Spotify API to gather information about a track
which the user is currently listening to. The app then queries classical music 
APIs in order to deliver a robust context that track. This is not unlike a 
device in the video game Pokemon (known as a Pokedex) which the protagonist Ash
uses to gain information about creatures he spots in the wild.

Hence... Spotidex. 

## How To Install This Program

(Coming Soon)

## Benchmarks and Criteria

This project is being assessed as part of my assessment for the 2020 Coder 
Academy CCC course. The brief is to design a terminal application that 
handles two-way communication with an API of my choice. This assessment contains
four main criteria that are equally weighted:

1. How well I describe what the app is trying to achieve, how to interact with
it, and how the program achieves it on a high level. In other words, how
thorough this **README** file is.
2. How well I utilize OOP to create the structures needed to deliver the 
solutions for my program, i.e. how well written my model classes are.
3.  How well I utilize OOP to handle input and output of my program, i.e. how 
well written my views and view-models are.
4. How well my programs handles errors and edge cases. My assessors will try to
break my program and it needs to be able to resist those attempts.

In addition, I've taken some time to consider what I wrote in the [previous 
terminal assessment](https://github.com/redbrickhut/StringSectionRosteringUtility), 
and in doing so have come up with some extra benchmarks for myself in order
to demonstrate that I am improving as a developer:

* **Testing**: This project contains rigorous and specific automated tests that 
provide widespread coverage throughout the code base. Given I'm using a lot of
3rd party APIs and modules, there's a need to utilize some considered
strategies in order to accurately expose the code I have written.
* **Project Structure**: This project has a directory structure that attempts
to reflect a real-world distribution as much as possible. It uses the outline
discussed in [this article](https://docs.python-guide.org/writing/structure/)
which outlines an example by Kenneth Reitz.
* **Packages**: As this project is well-structured, this project in turn 
demonstrates an understanding of how package imports are used in Python, and
through that implicitly demonstrates a program that adheres to the MVVM 
(Model / View / View-Model ) structure. This will allow for me to implement a
different interface (such as a GUI) in the future with minimal refactoring. 
* **CI/CD**: This project makes use of Github actions to provide a useful 
automated CI/CD process which as a minimum will be used to ensure the code
pushed to the master branch passes all the required tests. If there is time,
this pipeline will be extended by either deploying the application on Pypi, 
or by creating executable binaries for the major platforms.

## Development Process

For this initial version, I am using this 
[Github project board](https://github.com/redbrickhut/spotidex/projects/1) to 
manage my actionable tasks. Any issues or pull requests that are made will 
automatically feed into this board. 