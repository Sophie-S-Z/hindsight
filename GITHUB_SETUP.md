# 📘 GitHub Repository Setup Guide

Follow these exact steps to create your GitHub repository and upload your Hindsight code.

---

## Step 1: Create a New Repository on GitHub

1. Go to [github.com](https://github.com) and sign in
2. Click the **+** icon in the top right corner
3. Select **"New repository"**
4. Fill in the details:
   - **Repository name:** `hindsight`
   - **Description:** `🔮 Text conversations with your future self - Series Hackathon 2025`
   - **Visibility:** Select **Public** (required for hackathon - must be open source)
   - **DO NOT** check "Add a README file" (we already have one)
   - **DO NOT** add .gitignore (we already have one)
   - **DO NOT** add a license (we already have one)
5. Click **"Create repository"**

---

## Step 2: Upload Your Code

### Option A: Using GitHub Web Interface (Easiest)

1. After creating the repo, you'll see a page with setup instructions
2. Click **"uploading an existing file"** link
3. Drag and drop ALL files from your `hindsight` folder:
   - `main.py`
   - `demo.py`
   - `send_intro.py`
   - `test_connection.py`
   - `requirements.txt`
   - `README.md`
   - `LICENSE`
   - `.gitignore`
   - `.env.example`
   - `src/` folder (with all files inside)
   - `data/` folder
   - `tests/` folder

4. **IMPORTANT:** Do NOT upload `.env` (it contains your secrets!)

5. Add commit message: `Initial commit - Hindsight hackathon project`
6. Click **"Commit changes"**

### Option B: Using Git Command Line

If you have git installed on your computer:

```bash
# Navigate to your hindsight folder
cd /path/to/hindsight

# Initialize git repository
git init

# Add all files (respects .gitignore, so .env won't be added)
git add .

# Create first commit
git commit -m "Initial commit - Hindsight hackathon project"

# Add your GitHub repo as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/hindsight.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Step 3: Verify Your Repository

After uploading, your repository should look like this:

```
hindsight/
├── .gitignore
├── .env.example
├── LICENSE
├── README.md
├── demo.py
├── main.py
├── requirements.txt
├── send_intro.py
├── test_connection.py
├── data/
│   └── memories/
│       └── .gitkeep
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── imessage_client.py
│   ├── kafka_handler.py
│   ├── memory.py
│   └── persona.py
└── tests/
```

**Check that:**
- ✅ README.md is displayed on the main page
- ✅ All Python files are uploaded
- ✅ `.env` is NOT uploaded (it should be in .gitignore)
- ✅ Repository is set to Public

---

## Step 4: Get Your Repository URL

Your repository URL will be:
```
https://github.com/YOUR_USERNAME/hindsight
```

**This is what you'll submit to Shipyard for the hackathon!**

---

## Troubleshooting

### "I accidentally uploaded my .env file!"

1. Go to your repository on GitHub
2. Navigate to the `.env` file
3. Click the trash icon to delete it
4. Commit the deletion
5. **IMPORTANT:** Regenerate your API keys immediately! Once a secret is pushed to GitHub, consider it compromised.

### "My src folder is empty on GitHub"

GitHub doesn't track empty folders. Make sure each folder has at least one file:
- `src/__init__.py` should exist
- `data/memories/.gitkeep` should exist

### "I can't see my README"

Make sure the file is named exactly `README.md` (case sensitive) and is in the root folder.

---

## Quick Checklist Before Submission

- [ ] Repository is PUBLIC
- [ ] README.md displays correctly
- [ ] All source code files are uploaded
- [ ] `.env` is NOT in the repository
- [ ] `.env.example` IS in the repository
- [ ] You have the repository URL ready for Shipyard

---

## Your GitHub URL

Once created, your repository URL will be:

```
https://github.com/YOUR_GITHUB_USERNAME/hindsight
```

Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username.

Good luck! 🔮
