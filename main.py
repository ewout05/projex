#!/usr/bin/env python3
import sys
import os
import subprocess
from pathlib import Path
from git import Repo  # pip install GitPython
import shutil
import tempfile

# -------- CONFIG -----------
# Templates worden opgeslagen in de huidige werkdirectory
TEMPLATE_DIR = Path.cwd()

# -------- HELP FUNCTION --------
def show_help():
    print("""
Projex Generator CLI
Usage:
  projex pull <user>/<repo>           Download template into current folder
  projex exec <user>/<repo>/<script> Run a script from the template
  projex init <user>/<repo>/<script> Download template and run script
""")

# -------- PULL FUNCTION --------

def pull_template(repo):
    user, repo_name = repo.split("/")
    url = f"https://github.com/{user}/{repo_name}.git"

    print(f"[+] Downloading {url} into current folder...")
    
    # Maak een tijdelijke folder
    with tempfile.TemporaryDirectory() as tmpdirname:
        Repo.clone_from(url, tmpdirname)

        # Kopieer alles uit tmpdirname naar TEMPLATE_DIR (cwd)
        for item in os.listdir(tmpdirname):
            s = os.path.join(tmpdirname, item)
            d = os.path.join(TEMPLATE_DIR, item)
            if os.path.exists(d):
                print(f"[!] Bestand/map {item} bestaat al, overslaan")
            else:
                if os.path.isdir(s):
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)

    print("[+] Download complete")


# -------- EXEC FUNCTION --------
def exec_script(repo_script):
    parts = repo_script.split("/")
    if len(parts) < 3:
        print("[!] Usage: projex exec <user>/<repo>/<script>")
        return
    user, repo_name, script = parts
    template_path = TEMPLATE_DIR / repo_name
    if not template_path.exists():
        print(f"[!] Template not found locally. Pulling first...")
        pull_template(f"{user}/{repo_name}")
    script_path = template_path / script
    if not script_path.exists():
        print(f"[!] Script {script} not found in template.")
        return
    print(f"[+] Running script: {script_path}")
    if script_path.suffix == ".py":
        subprocess.run(["python", str(script_path)])
    elif script_path.suffix == ".bat":
        subprocess.run([str(script_path)], shell=True)
    elif script_path.suffix == ".sh":
        subprocess.run(["bash", str(script_path)])
    else:
        print("[!] Unknown script type. Use .py, .bat, or .sh")

# -------- INIT FUNCTION --------
def init_template(repo_script):
    parts = repo_script.split("/")
    if len(parts) < 3:
        print("[!] Usage: projex init <user>/<repo>/<script>")
        return
    pull_template("/".join(parts[:2]))
    exec_script(repo_script)

# -------- MAIN CLI HANDLER --------
def main():
    if len(sys.argv) < 3:
        show_help()
        return
    cmd = sys.argv[1]
    arg = sys.argv[2]

    if cmd == "pull":
        pull_template(arg)
    elif cmd == "exec":
        exec_script(arg)
    elif cmd == "init":
        init_template(arg)
    else:
        print(f"[!] Unknown command: {cmd}")
        show_help()

if __name__ == "__main__":
    main()
