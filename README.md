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
- Download `ptillaten/all` and `servicedagar/all` with the Shortcut (same URL pattern, swap the dataset name)
- On a computer: `python3 prep.py ptillaten.json servicedagar.json` creates a new `data.json`
- Upload `data.json` to the repo, replacing the old one
