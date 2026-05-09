# museum

A static site generator using Jinja2 templates, JSON data, and CSS.

## Project Structure

```
museum/
├── templates/          # Jinja2 HTML templates
│   ├── base.html      # Base template
│   ├── index.html     # Home page template
│   └── about.html     # About page template
├── data/              # JSON data files
│   ├── home.json      # Home page data
│   └── about.json     # About page data
├── static/            # Static assets (CSS, images, etc.)
│   └── style.css      # Site stylesheet
├── output/            # Generated site (created after build)
├── generate_site.py   # Site generator script
└── requirements.txt   # Python dependencies
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

This will create the static site in the `output/` directory.

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

### Adding New Pages

1. Create a template in `templates/` (e.g., `contact.html`)
2. Create corresponding data in `data/` (e.g., `contact.json`)
3. Add the page to `generate_site.py`:
   ```python
   pages = [
       ('index.html', 'home.json', 'index.html'),
       ('about.html', 'about.json', 'about.html'),
       ('contact.html', 'contact.json', 'contact.html'),  # New page
   ]
   ```

### Updating Content

Edit the JSON files in the `data/` directory and rebuild the site.

### Modifying Styles

Edit `static/style.css` and rebuild the site.