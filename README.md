# macos-elte-organizer

This is my own personal study folder organizer for macos. 
Currently to my best of knowledge, only 2026 ELTE student future graduates from Group 4 in their first semester can also use this.

Quick Setup:
Example:

[DIRECTORIES]
Destination = /Users/chuluun/Desktop/testing
Downloads = /Users/chuluun/Downloads

[SETTINGS]
Move or Copy = move

[LINKS]
Basic Math = https://canvas.elte.hu/courses/36812 |https://ikelte.sharepoint.com/sites/BasicMathematicsGroup4 |

Each subject can have multiple links and links must be followed by a space and '|'.


To setup the organizer, we need to create a config.ini file with our own data. You may use the config.py program to setup your data, or you can directly type into the config.ini file.

Example data:
/*
[DIRECTORIES]
Destination = /Users/chuluun/Desktop/testing
Downloads = /Users/chuluun/Downloads

[SETTINGS]
Move or Copy = move

[LINKS]
Basic Math = https://canvas.elte.hu/courses/36812 |https://ikelte.sharepoint.com/sites/BasicMathematicsGroup4 |
*/

The data will have 3 sections. The required directory pathways, setting for either moving the files or copying the files, and the links for our data. Make sure to write the data properly! or I can just give a warning if you didn't write properly. 
When inputting the links, make sure each link is followed by a space, and '|'. Each subject can have multiple links.

Each course for teams and canvas has a certain id after the given link above. For example:
My basic math subject link for Canvas is 'https://canvas.elte.hu/courses/36812' and 
for Teams it's 'https://ikelte.sharepoint.com/sites/BasicMathematicsGroup4/'

You can find the link for your subject by: 
Entering this website for TEAMS LINKS https://ikelte.sharepoint.com/_layouts/15/sharepoint.aspx
and for CANVAS LINKS https://canvas.elte.hu/courses
Or: clicking on the downloaded file -> Get Info -> More Info -> Where from: 'LINK'


When setting up configuration file, specify where you want the file
