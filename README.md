# POPCRN (in development)

## Description

Popcrn is a project being developed for the final project of CS1951A - Data Science at Brown University. While a further flushed-out description will replace this one at the end of development, Popcrn intends to perform sentiment analysis for the purpose of compiling a mapping between the general sentiment of an individual's Twitter presence (as determined by the content of their tweets) and a set of songs, which is supposed to embody that general sentiment.

## Progress

Currently, Popcrn has the majority of the ingestion capabilities, but lacks the sentiment analysis algorithms that will ultimately be used to generate the sentiment mapping.

## Setup

1. Clone this repository with a simple:
<code>git clone https://github.com/sahilprasad/popcrn.git</code>

2. Set up a virtual environment for this project, and activate it.

3. Navigate to the `popcrn` directory, and run `python setup.py develop`. This will take a while, as all of the dependencies of the application are being downloaded and installed into the virtual environment.

4. Run the application server with `pserve development.ini` and navigate to the localhost URL for the web interface.

5. Enjoy!

## Live version

This project will eventually go live, so stay tuned!
