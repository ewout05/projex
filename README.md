
---

# Projex Generator

**A lightweight CLI tool to download GitHub templates directly into your current folder and run associated scripts.**

Projex Generator lets you quickly pull project templates from GitHub, run scripts, or do both in one command — all **without creating extra folders**.

---

## Features

* Download GitHub repositories directly into your **current working directory** (`pull`)
* Execute scripts from templates (`exec`)
* Download and run in one command (`init`)
* Supports `.py`, `.bat`, and `.sh` scripts
* Works on Windows (tested) and can be extended to Linux/macOS

---

## Installation

1. Clone or download this repository to a folder, e.g.:

```bash
git clone https://github.com/yourusername/projex.git
```

2. Make sure **Python 3** is installed:

```bash
python --version
```

3. Install dependencies:

```bash
python -m pip install --user GitPython
```

4. Make sure **Git** is installed and in your PATH:

```bash
git --version
```

---

## Setting up PATH (Windows)

To use `projex` from **any folder** in your terminal:

1. Locate the folder where `projex.bat` is placed (e.g., `C:\codespace\python\projex`)
2. Open **Environment Variables** → Edit **Path** → Add this folder
3. Open a **new terminal** to apply changes

Now you can run `projex` from any folder:

```bash
projex pull ewout05/ClipCalc
```

---

## Usage

```
projex pull <user>/<repo>           Download template into current folder
projex exec <user>/<repo>/<script> Run a script from template
projex init <user>/<repo>/<script> Download template and run script
```

### Examples

* **Pull template only**:

```bash
projex pull ewout05/ClipCalc
```

* **Run a script from a template**:

```bash
projex exec ewout05/ClipCalc/setup.bat
```

* **Download and run a script in one command**:

```bash
projex init ewout05/ClipCalc/setup.bat
```

---

## Notes

* Templates are copied **directly into the current folder**, not into a subfolder.
* Existing files with the same name will be skipped.
* Supports `.py`, `.bat`, and `.sh` scripts.

---

## Contributing

Feel free to fork, create templates, or add commands. You can host templates anywhere on GitHub, and users can pull them with Projex.

---

## License

MIT License – feel free to use and modify.

---