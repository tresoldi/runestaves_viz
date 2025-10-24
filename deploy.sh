#!/bin/bash
# Deploy runestaves visualization to GitHub Pages
#
# This script builds the site locally with the correct base path
# and pushes it to the gh-pages branch.

set -e  # Exit on error

echo "🚀 Deploying Runestaves Visualization to GitHub Pages"
echo "======================================================"

# Clean previous build
echo "Cleaning previous build..."
make clean

# Build site with GitHub Pages base path
echo "Building site with /runestaves_viz base path..."
BASE_PATH=/runestaves_viz make site-release

# Verify build succeeded
if [ ! -f "site/index.html" ]; then
    echo "❌ Build failed - site/index.html not found"
    exit 1
fi

echo "✓ Build complete"

# Deploy to gh-pages
echo "Deploying to gh-pages branch..."
cd site
git init
git add -A
git commit -m "Deploy site - $(date -I)"
git push -f origin master:gh-pages
cd ..

# Clean up
rm -rf site/.git

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Your site will be live in 1-2 minutes at:"
echo "https://tresoldi.github.io/runestaves_viz/"
