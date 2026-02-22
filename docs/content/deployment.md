# Deployment

## Publishing to PyPI

Releases are automated via GitHub Actions. The workflow triggers on GitHub Releases.

### Steps

1. Update `version` in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Commit and push to `main`
4. Create a GitHub Release with tag `v0.x.y`
5. The `publish.yml` workflow builds, verifies, and publishes to PyPI via trusted publishing

### Manual Publish

```bash
pip install build twine
python -m build
twine check dist/*
twine upload dist/*
```

## Documentation Site

The docs are built with Vite, React 19, and Tailwind CSS 4. Markdown files live in `docs/content/` and are rendered at build time.

### Local Preview

```bash
cd docs
npm ci
npm run dev
```

### Production Build

```bash
cd docs
npm run build
npm run preview
```

### Deploy to Vercel

The `docs/vercel.json` configures SPA rewrites. Point Vercel at the `docs/` directory with:

- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **Install Command:** `npm ci`

### Deploy to GitHub Pages

Add a GitHub Actions workflow:

```yaml
name: Deploy Docs
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pages: write
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
      - name: Install & Build
        working-directory: docs
        run: npm ci && npm run build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: docs/dist
      - uses: actions/deploy-pages@v4
```
