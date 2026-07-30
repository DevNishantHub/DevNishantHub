# Setup Instructions for DevNishantHub Profile

## 1. Create the profile repo
Create a new GitHub repo named exactly: `DevNishantHub`
(same as your username — this is what makes it a profile README)

## 2. Upload all files
Push everything in this folder to that repo's `main` branch.

## 3. Enable GitHub Actions write permission
Repo → Settings → Actions → General → Workflow permissions → "Read and write permissions" ✓

## 4. Run the stats action
Repo → Actions → "refresh stats" → Run workflow
This generates: stats.svg, streak.svg, langs.svg, year.svg, hd-*.svg

## 5. Add your photo as ascii.svg (optional but recommended)
The original profile uses a photo converted to ASCII art saved as ascii.svg.
To replicate:
- Use: https://github.com/andriidrok1/andriidrok1 as reference
- Or replace ascii.svg with any image/SVG you prefer
- Or delete the ascii.svg line from README.md entirely

## 6. Update your links in README.md
Edit README.md and replace:
- `your@email.com` → your real email
- LinkedIn URL if different

## Daily auto-refresh
The workflow runs at 05:17 UTC daily via cron. Stats update automatically.
