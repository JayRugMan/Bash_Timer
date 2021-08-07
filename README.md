== Bash_Timer (timer.sh) ==
keep track of time using bash
This script needs a timer.comf file, which is included in the .gitignore file. 
The contents should be as follows:

CAT_HEADING_ARRAY=(
"Some category"
"Project 2"
"Lunch"
"Other"
)

It can currently have up to 17 categories


== Python_Timer (timer.py) ==
keep track of time using python3
This script needs a timerpy.conf file, which is included in the .gitignore file.
It should contain some lines similar to the following. Note that any line with #
will be ignored, spaces are fine, quotes are not necessary, and the EOL character
should be \n (Unix style) - Maybe I'll make it work with /r/n or /r for Windows 
or Mac later... maybe... 

# Categories
Some category
Project 2
Lunch
Other


Categories can be added either while the program is running or not. However, if
the program is running, the categories can be added one at a time within the 
program. Anything added to the conf file directly while the program is running
will not be available until the program is exited and restarted. 

Also note, the code is written to show eod considering "Lunch," so that category 
is necessary in the current version

