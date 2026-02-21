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

The docs are built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

### Local Preview

```bash
pip install -e ".[docs]"
mkdocs serve
```

### Deploy to GitHub Pages

```bash
mkdocs gh-deploy
```

Or add a GitHub Actions workflow:

```yaml
name: Deploy Docs
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[docs]"
      - run: mkdocs gh-deploy --force
```
