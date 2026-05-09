# Museum of Memory

A static prototype for the Museum of Memory public archive and editorial
workspace. Profile content lives in structured JSON so public pages and
agent/editor review screens can be built from one source of truth.

## Project Structure

```
museam/
├── index.html                         # Public home page prototype
├── archive.html                       # Archive listing prototype
├── carmen.html                        # Public profile page shell
├── agent.html                         # Internal editorial/agent workspace shell
├── data/people/carmen-teresa-navas.json
│                                      # Shared profile/source/review data
├── output/                            # Generated deploy artifact
├── generate_site.py                   # Renders site + validates profiles
└── requirements.txt
```

## Building the Site

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate the Site

```bash
python generate_site.py
```

This renders the homepage, archive listing, profile pages, and agent/editor
workspace from JSON, copies static assets and structured data into `output/`,
and writes profile validation reports to `output/validation/`.

## Previewing Locally

Start a local web server to preview the site:

```bash
cd output
python -m http.server 8000
```

Then open http://localhost:8000 in your browser.

## Deploying to GitHub Pages

### Automatic Deployment with GitHub Actions

The repository includes a GitHub Actions workflow that automatically builds and deploys the site.

1. **Configure GitHub Pages:**
   - Go to your repository settings on GitHub
   - Navigate to Pages section
   - Set source to "GitHub Actions"

2. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add static site generator and deployment workflow"
   git push
   ```

Your site will be automatically built and deployed to `https://YOUR_USERNAME.github.io/museum/`

### Manual Deployment

1. Build the site locally:
   ```bash
   python generate_site.py
   ```

2. Use the `gh-pages` branch:
   ```bash
   npm install -g gh-pages
   gh-pages -d output
   ```

## Customizing the Site

### Adding New Profiles

1. Add a JSON profile under `data/people/`.
2. Include sources, claims, review questions, and publish gates.
3. Run `python generate_site.py` and inspect the validation report.
4. Preview `output/` locally. The profile will appear automatically on the
   homepage, archive, and generated public profile page.

### Updating Content

Edit the JSON files in `data/people/` and rebuild the site.

### Modifying Styles

Edit `static/style.css` and rebuild the site.
