#!/bin/bash
# Helper script to push code to GitHub

echo "=========================================="
echo "🚀 Push Student Study Buddy to GitHub"
echo "=========================================="
echo

# Prompt for the GitHub URL
read -p "Enter your GitHub Repository URL (e.g. https://github.com/username/repo.git): " repo_url

if [ -z "$repo_url" ]; then
    echo "❌ Error: Repository URL cannot be empty."
    exit 1
fi

# Set the remote URL
git remote remove origin 2>/dev/null
git remote add origin "$repo_url"

# Rename branch to main
git branch -M main

# Push the code
echo "Pushing code to $repo_url..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo
    echo "✅ Successfully pushed to GitHub!"
    echo "Now go to https://share.streamlit.io/ to deploy your app."
else
    echo
    echo "❌ Failed to push. Make sure the URL is correct and you have permission to push."
fi
