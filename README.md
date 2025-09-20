# 🧹 Behavior Dirty Edit Cleaner



A Python/Tkinter tool for scanning and removing **dirty edits** from Skyrim mod behavior files.  

Supports both **Nemesis_Engine** and **Pandora_Engine** mod folders, using a configurable list of file paths and regex patterns.



## How it works



Reads the files listed in file list, checks for dirty edit patterns in patterns then deletes if it matches a pattern.



## Prerequisites

- Python **3.8+**

- Tkinter

- `filelist.txt` — list of relative file paths to check  

- `patterns.txt` — regex patterns to match dirty edits



## Usage

1. Place `behavior_dirty_edit_cleaner.py`, `filelist.txt`, and `patterns.txt` in the same folder.

2. Run:

```bash

python behavior_dirty_edit_cleaner.py

```

3. In the GUI:

- Select your mod folder that you want to clean

- Edit and select your filelist.txt and patterns.txt or use the one included (written based on article)

- Click Run Cleanup

4. Deletions are logged to cleanup.log.



## Building to EXE (Optional)
```bash
python -m nuitka behavior_dirty_edit_cleaner.py --onefile --windows-console-mode=disable --enable-plugin=tk-inter --lto=yes --remove-output --clang --output-dir=build
```
