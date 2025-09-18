import os, re, sys, tkinter as tk
from tkinter import filedialog, scrolledtext
from datetime import datetime

def load_list(fp, patterns=False):
    try:
        with open(fp, "r", encoding="utf-8-sig") as f:
            lines = [l.strip() for l in f if l.strip() and not l.lstrip().startswith("#")]
            return [re.compile(l, re.I) for l in lines] if patterns else lines
    except FileNotFoundError:
        print(f"[ERROR] File not found: {fp}")
    except Exception as e:
        print(f"[ERROR] Could not load {fp}: {e}")
    return []

def log_message(widget, log_file, msg):
    widget.insert(tk.END, msg + "\n"); widget.see(tk.END)
    with open(log_file, "a", encoding="utf-8") as lf: lf.write(msg + "\n")

def run_cleanup(mod_dir, paths_file, patterns_file, log_widget):
    base_dir = os.path.dirname(sys.executable if (getattr(sys, 'frozen', False) or (
        os.path.splitext(sys.executable)[1].lower() in ('.exe', '') and not sys.executable.endswith('python.exe')
    )) else os.path.abspath(__file__))
    log_file = os.path.join(base_dir, "cleanup.log")

    rel_paths, patterns = load_list(paths_file), load_list(patterns_file, True)
    if not rel_paths: return log_message(log_widget, log_file, f"[ERROR] No paths loaded from {paths_file}")
    if not patterns:  return log_message(log_widget, log_file, f"[ERROR] No patterns loaded from {patterns_file}")

    log_message(log_widget, log_file, f"\n=== Run started {datetime.now():%Y-%m-%d %H:%M:%S} ===\n")
    engines = ("Nemesis_Engine", "Pandora_Engine")
    found, deleted_total = False, []
    print(patterns[0])

    for engine in engines:
        mods_dir = os.path.join(mod_dir, engine, "mod")
        if not os.path.isdir(mods_dir):
            continue
        found = True
        for modname in os.listdir(mods_dir):
            mod_path = os.path.join(mods_dir, modname)
            if not os.path.isdir(mod_path):
                continue
            for rel_path in rel_paths:
                fp = os.path.join(mod_path, rel_path)
                if not os.path.isfile(fp):
                    continue
                try:
                    
                    with open(fp, "r", encoding="utf-8-sig", errors="ignore") as f:
                        content = f.read()
                    if any(p.search(content) for p in patterns):
                        os.remove(fp)
                        deleted_total.append(fp)
                        log_message(log_widget, log_file, f"[DELETED] {fp}")
                    else:
                        log_message(log_widget, log_file, f"[SKIPPED] {fp} — no dirty edit found")

                except Exception as e:
                    log_message(log_widget, log_file, f"[ERROR] Could not process {fp}: {e}")

    if not found:
        log_message(log_widget, log_file, f"[ERROR] No supported engine folder found in {mod_dir}")
    else:
        log_message(log_widget, log_file, f"\n=== SUMMARY ===\nDeleted {len(deleted_total)} files")
        for f in deleted_total:
            log_message(log_widget, log_file, f" - {f}")


def launch_ui():
    root = tk.Tk(); root.title("Behavior Dirty Edit Cleaner")
    def browse(entry, dir_mode=False):
        path = filedialog.askdirectory() if dir_mode else filedialog.askopenfilename()
        if path: entry.delete(0, tk.END); entry.insert(0, os.path.relpath(path) if not dir_mode else path)

    tk.Label(root, text="Mod Root Folder:").grid(row=0, column=0, sticky="w")
    mod_dir_entry = tk.Entry(root, width=50); mod_dir_entry.grid(row=0, column=1)
    tk.Button(root, text="Browse", command=lambda: browse(mod_dir_entry, True)).grid(row=0, column=2)

    tk.Label(root, text="File List (filelist.txt):").grid(row=1, column=0, sticky="w")
    paths_entry = tk.Entry(root, width=50); paths_entry.insert(0, "filelist.txt"); paths_entry.grid(row=1, column=1)
    tk.Button(root, text="Browse", command=lambda: browse(paths_entry)).grid(row=1, column=2)

    tk.Label(root, text="Pattern Config (patterns.txt):").grid(row=2, column=0, sticky="w")
    pattern_entry = tk.Entry(root, width=50); pattern_entry.insert(0, "patterns.txt"); pattern_entry.grid(row=2, column=1)
    tk.Button(root, text="Browse", command=lambda: browse(pattern_entry)).grid(row=2, column=2)

    log_widget = scrolledtext.ScrolledText(root, width=80, height=20); log_widget.grid(row=3, column=0, columnspan=3, pady=10)
    tk.Button(root, text="Run Cleanup", command=lambda: run_cleanup(mod_dir_entry.get(), paths_entry.get(), pattern_entry.get(), log_widget)).grid(row=4, column=1)
    root.mainloop()

if __name__ == "__main__":
    launch_ui()
