# B-Flat

Caveat: I wrote all of this code originally in August 2021, and moved it to this repo in 2022.
The code is not the best quality, and its compounded by the fact that sliders in OpenCV 
are very finicky and require global variables. 

## Problem
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

## Usage
