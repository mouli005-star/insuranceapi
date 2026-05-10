# insuranceAPI

This repository contains a FastAPI service that predicts insurance premium using a pre-trained model.

Quick setup (local)

1. Create a GitHub repository (public) on github.com and copy the repo URL.
2. Activate your virtualenv (you already have `app/`):

```powershell
& "app\Scripts\Activate.ps1"
```

3. Install dependencies and pin them:

```bash
pip install -r requirements.txt
pip freeze > requirements.txt
```

4. (Optional) If `model.pkl` is required for the app, add it to the repo or use Git LFS for large files:

- To add normally (small file): place `model.pkl` in the repo root and commit.
- If the file is >50MB, use Git LFS: `git lfs install` then `git lfs track "*.pkl"`.

5. Initialize git, commit, and push:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

Notes
- `.gitignore` excludes the virtual environment and model/data files by default. If you want others to be able to run the app immediately, include `model.pkl` (or provide a download link) and commit it, or use LFS.
- To run the API locally:

```bash
uvicorn app:app --reload
```

Streamlit Cloud deployment

1. In Streamlit Cloud, set Main file path to `frontend.py` (not `app.py`).
2. Keep branch as `main`.
3. Use this repo root as-is (`requirements.txt` and `runtime.txt` are already configured).
4. Click Reboot app after each push.

If you want, I can:

- initialize the git repo locally and create the initial commit, or
- generate a GitHub repo for you (you'll need to provide the repository URL or grant access).
