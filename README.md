# 🧹 Behavior Dirty Edit Cleaner



A Python/Tkinter tool for scanning and removing **dirty edits** from Skyrim mod behavior files.  

Supports both **Nemesis_Engine** and **Pandora_Engine** mod folders, using a configurable list of file paths and regex patterns.



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

- Select your Mod Root Folder

- Select your filelist.txt

- Select your patterns.txt

- Click Run Cleanup

4. Deletions are logged to cleanup.log.



## Building to EXE (Optional)
```bash
python -m nuitka behavior_dirty_edit_cleaner.py --onefile --windows-disable-console --enable-plugin=tk-inter --lto=yes --remove-output --nofollow-imports --clang --output-dir=build
```
