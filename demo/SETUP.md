# Setup (GitHub Pages)
1. Create a GitHub repo (e.g. `taskguide`) and upload everything in this folder.
2. Edit `config.json`: `url` (https://USERNAME.github.io), `base` ("/REPO", or "" for a custom domain), `repo`.
3. Edit `admin/config.yml`: set `repo: USERNAME/REPO`.
4. Repo Settings > Pages > Source: **GitHub Actions**. Every push to `main` rebuilds the site.
5. Admin Panel: `https://USERNAME.github.io/REPO/admin/`. Log in with GitHub (access to the repo required).
6. Business registrations arrive by email via Formspree. In the Admin Panel > Businesses, create the entry and switch on "Approved and live" to publish.
Local preview: `pip install -r requirements.txt && SITE_BASE="" python build.py`, then open the `dist` folder with any static server.
