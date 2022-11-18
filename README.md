# B-Flat

Flattens a sheet music pdf into one really long png so it can be viewed on a phone.

Example input: [Madeon - Shelter.pdf](Madeon%20-%20Shelter.pdf)
and output: [Madeon - Shelter-flattened.png](Madeon%20-%20Shelter-flattened.png)

Caveat: I wrote all of this code originally in August 2021, and moved it to this repo in 2022.
I did some refactoring in 2022, but it's still not representative of my best work.

## Usage
- Install Python
- python -m venv venv
- activate the venv (depends on your OS)
- pip install -r requirements.txt
- python main.py
- Select your sheet music pdf file
- Crop the left and right sides with the windows that pop up to remove whitespace, clefs, and 
optionally time signature/key signature
The left and right cropping amount chosen here will propogate to the rest of the sheet music.
- A really long image will be output that can be sent to your phone to use with an autoscrolling app.

## Problem statement
As far as I'm aware, there's no app that lets you easily play 
from sheet music on a cell phone.

Most sheet music apps are geared towards having a tablet, but I'm not going to bring my tablet around
all the time, whereas I'll always have my phone on me when I happen upon a piano, and of course, not everyone
has a tablet. 

## Solution (kind of)
Since there are autoscrolling apps on the market (and I made [my own](https://play.google.com/store/apps/details?id=com.kevinlinxc.guitarautoscroll&pli=1)),
I figured that the best way to view sheet music on a phone would be to flatten it into a single staff, and play it on an 
autoscrolling app.

The reason this is only kind of a solution is that scrolling at a set speed isn't perfect for sheet music.

The tempo can change, and the spacing between notes can also change during a piece. Without the ability to change
the scrolling speed during the performance, this makes it pretty hard to read the sheet music at a single speed.

One idea is to encode the scrolling speed as maybe a grayscale 0-255 value at the edge of the sheet music picture,
but I haven't thought of a satisfying way for a user to generate this without a lot of manual work, and of course
the scrolling app would need to interpret this encoding too.
