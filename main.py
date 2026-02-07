#!/usr/bin/env python3
import sys
import os
import subprocess
from pathlib import Path
from git import Repo
import shutil
import tempfile
import requests

# -------- CONFIG -----------
TEMPLATE_DIR = Path.cwd()

# -------- HELP FUNCTION --------
def show_help():
    print("""
Projex Generator CLI
Usage:
  projex pull <user>/<repo>
  projex exec <user>/<repo>/<script> [key=value ...]
  projex init <user>/<repo>/<script> [key=value ...]
""")

# -------- PULL FUNCTION --------
def pull_template(repo):
    user, repo_name = repo.split("/")
    url = f"https://github.com/{user}/{repo_name}.git"

    print(f"[+] Downloading {url} into current folder...")

    with tempfile.TemporaryDirectory() as tmpdirname:
        Repo.clone_from(url, tmpdirname)

        for item in os.listdir(tmpdirname):
            s = os.path.join(tmpdirname, item)
            d = os.path.join(TEMPLATE_DIR, item)
            if os.path.exists(d):
                print(f"[!] {item} already exists, skipping")
            else:
                if os.path.isdir(s):
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)

    print("[+] Download complete")

# -------- EXEC FUNCTION (REMOTE SCRIPT + VARIABLES) --------
def exec_script(repo_script, variables):
    parts = repo_script.split("/")
    if len(parts) < 3:
        print("[!] Usage: projex exec <user>/<repo>/<script> [key=value]")
        return

    user, repo_name, *script_path = parts
    script_file = "/".join(script_path)

    url = f"https://raw.githubusercontent.com/{user}/{repo_name}/main/{script_file}"
    print(f"[+] Downloading script from {url} ...")

    resp = requests.get(url)
    if resp.status_code != 200:
        print("[!] Failed to download script.")
        return

    content = resp.text

    # Replace placeholders {{key}}
    for var in variables:
        if "=" in var:
            key, value = var.split("=", 1)
            content = content.replace(f"{{{{{key}}}}}", value)

    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(script_file).suffix, mode="w", encoding="utf-8") as tmp_file:
        tmp_file.write(content)
        tmp_file_path = tmp_file.name

    print("[+] Running script...")
    subprocess.run(tmp_file_path, shell=True, cwd=Path.cwd())

    Path(tmp_file_path).unlink()

# -------- INIT FUNCTION --------
def init_template(repo_script, variables):
    parts = repo_script.split("/")
    if len(parts) < 3:
        print("[!] Usage: projex init <user>/<repo>/<script>")
        return

    pull_template("/".join(parts[:2]))
    exec_local_script(repo_script, variables)

# -------- LOCAL EXEC FUNCTION --------
def exec_local_script(repo_script, variables):
    parts = repo_script.split("/")
    user, repo_name, *script_path = parts
    script_file = script_path[-1]

    script_path_local = TEMPLATE_DIR / script_file
    if not script_path_local.exists():
        print(f"[!] Script {script_file} not found in current folder")
        return

    # Read and replace variables
    content = script_path_local.read_text(encoding="utf-8")

    for var in variables:
        if "=" in var:
            key, value = var.split("=", 1)
            content = content.replace(f"{{{{{key}}}}}", value)

    with tempfile.NamedTemporaryFile(delete=False, suffix=script_path_local.suffix, mode="w", encoding="utf-8") as tmp_file:
        tmp_file.write(content)
        tmp_file_path = tmp_file.name

    print("[+] Running local script...")
    subprocess.run(tmp_file_path, shell=True, cwd=Path.cwd())

    Path(tmp_file_path).unlink()

# -------- MAIN CLI HANDLER --------
def main():
    if len(sys.argv) < 3:
        show_help()
        return

    cmd = sys.argv[1]
    arg = sys.argv[2]
    variables = sys.argv[3:]

    if cmd == "pull":
        pull_template(arg)
    elif cmd == "exec":
        exec_script(arg, variables)
    elif cmd == "init":
        init_template(arg, variables)
    else:
        print(f"[!] Unknown command: {cmd}")
        show_help()

if __name__ == "__main__":
    main()
