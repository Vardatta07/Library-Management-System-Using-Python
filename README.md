# Library Management System (Python)

This repository contains a small, local Library Management System implemented in Python with a simple GUI (tkinter) and a command-line interface alternative.

Files of interest
- `library_management.py` - core library model and demo usage
- `library_interface.py` - interactive menu-based CLI interface
- `Untitled-3.py` - a modern tkinter GUI app (`LibraryManagementSystem`) for adding/searching/borrowing books
- `Untitled-1-FIXED.py` - fixed billing GUI program (cleaned-up copy)
- `requirements.txt` - Python dependencies (if any)

Quick start (Windows / PowerShell)
1. Create a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

2. Install dependencies (if any):

```powershell
pip install -r requirements.txt
```

3. Run the GUI app (simple example):

```powershell
python "d:\mini project\Untitled-3.py"
```

4. Or run the library demo script:

```powershell
python "d:\mini project\library_management.py"
```

Pushing this project to GitHub
- I initialized the project locally and created an initial commit for you (see commands below).
- To push to a GitHub repository you own, create a new repository on GitHub and then run these commands (replace `<repo-url>`):

```powershell
cd "d:\mini project"
git remote add origin <repo-url>
git branch -M main
git push -u origin main
```

If you'd like, provide the GitHub repo URL (or give me permission to access it) and I can add the remote and push for you.

Notes
- If your GitHub push requires authentication, use GitHub CLI `gh` or configure a PAT and set it in your Git credential helper.
- The project includes some example/untitled files; you may want to rename `Untitled-3.py` to `gui_app.py` (I can do that if you want).

If you want me to add a license file, restructure the project, or push to GitHub for you (you provide the repo URL), tell me and I'll proceed.