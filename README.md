# Spotidex
### A Classical Companion for Spotify

>Please note that this application is currently under development, and that 
>v1.0 of the program is due on the 2nd October 2020 as part of my assessment
>for the Coder Academy 2020 CCC course. For ease of editing, this document will 
>be written in the present tense for features not yet implemented.

This terminal application is designed to run alongside an active Spotify 
session, using the Spotify API to gather information about a track that the user 
is currently listening. The app will then query various classical music APIs in
order to deliver a bunch of interesting information about the current track. 

## Installation

(Coming Soon)

## Benchmarks and Criteria

This project is being assessed as part of my assessment for the 2020 Coder 
Academy CCC course. The brief is to design a terminal application that 
handles two-way communication with an API of my choice. This assessment contains
four main criteria:

1. How well I describe what the app is trying to achieve, how to interact with
it, and how the program achieves it on a high level. In other words, how
thorough this **README** file is.
2. 

* **Testing**: This project contains rigorous and specific automated tests that 
provide widespread coverage throughout the code base. 
* **Project Structure**: This project has a directory structure that attempts
to reflect a real-world distribution as much as possible. It uses the outline
discussed in [this article](https://docs.python-guide.org/writing/structure/)
which outlines an example by Kenneth Reitz.
* **Packages**: As this project is well-structured, this project in turn 
demonstrates an understanding of how package imports are used in Python, and
through that implicitly demonstrates a program that adheres to the MVVM 
(Model / View / ViewModel ) structure. This will allow for me to implement a
different interface (such as a GUI) in the future with minimal refactoring. 
* **CI/CD**: This project makes use of Github actions to provide a useful 
automated CI/CD process which as a minimum will be used to ensure the code
pushed to the master branch passes all the required tests. If there is time,
this pipeline will be extended by either deploying the application on Pypi, 
or by creating executable binaries for the major platforms.
