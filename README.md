# Stockholm street cleaning map

## Publish (one time, c.10 min)
1. Create a free GitHub account, then a new public repository, e.g. `street-cleaning`
2. Upload all files in this folder (Add file > Upload files), commit
3. Settings > Pages > Source: "Deploy from a branch", branch `main`, folder `/ (root)`, Save
4. After c.1 min the app is live at `https://<username>.github.io/street-cleaning/`

## Install on iPhone
1. Open the link in Safari
2. Share > Add to Home Screen
3. Open from the home screen icon, tap the location button, allow location

## Refresh data
- Run the Shortcut again to download `servicedagar.json`
- Rename it to `data.json` and upload it to the repo, replacing the old file (the app reads both the raw city format and the compressed one)
- Optional: run `python3 prep.py` on the raw file first to shrink it from c.11 MB to c.1.3 MB
