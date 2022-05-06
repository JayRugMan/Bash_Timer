# CLI Time Tracking Tool

## Bash Timer (timer.sh)
_Note I'm no longer developing this one_
Keep track of time using bash.

This script needs a timer.comf file, which is included in the .gitignore file.
The contents should be as follows:

```bash
CAT_HEADING_ARRAY=(
"Some category"
"Project 2"
"Lunch"
"Other"
)
```

It can currently have up to 17 categories


## Python Timer (timer.py)
Keep track of time using python3.

This script needs a categories.json file, which is included in the .gitignore file.
It should contain some lines similar to the following. Note the EOL character
should be \n (Unix style) - Maybe I'll make it work with /r/n or /r for Windows
or Mac later... maybe...

```json
{
  "Admin": [
    "email",
    "break"
  ],
  "project 1": [
    "task 2",
    "task 3"
  ],
  "Lunch": [
    "Lunch"
  ]
}
```

Categories can be added either while the program is running or not. However, if
the program is running, the categories can be added one at a time within the
program. Anything added to the conf file directly while the program is running
will not be available until the program is exited and restarted.

### About "Lunch"
If you add the super category "Lunch" with a sub category of "Lunch" then that
time will be added to the end of day time and subtracted from total time.
