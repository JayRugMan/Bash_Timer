# CLI Time Tracking Tool

## Bash Timer (timer.sh)

Keep track of time using bash. (_Note I'm no longer developing this one_)

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

### Prerequisits

You will need to install `dill` with `pip`

```bash
pip install dill
## OR
pip3 install dill
## OR
python[3] -m [pip|pip3] dill
```

If you don't have `pip`

#### `WSL` - Windows Subsystem Linux and Linux Mint (& Ubuntu, I guess 😒)

```bash
sudo apt update && sudo apt install python3-pip
```

#### Windows

1) Download the latest version of `get-pip.py` from the [official Python website](https://bootstrap.pypa.io/get-pip.py)
2) Open a Command Prompt or PowerShell and navigate to the directory where you saved `get-pip.py`
3) Run the command python `get-pip.py` to install `pip`

#### Categories and Sub-categories json

This script needs a categories.json file, which is filtered by the .gitignore
 file. It should contain some lines similar to the following.

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
