# Go Official Docs Korean Mirror

This repository is an unofficial, AI-assisted Korean translation mirror of the Go official documentation.

## Important notice

- The original Go documentation is maintained by the Go project and its contributors.
- This repository is not affiliated with, endorsed by, or officially maintained by the Go project.
- This project is intended as a community translation and reference mirror.
- For authoritative content, always check:
  - https://go.dev/doc
  - https://github.com/golang/go

## Goals

- Keep a Korean translation mirror synced with upstream Go documentation
- Use GitHub Actions to automate synchronization and translation
- Generate pull requests for human review before merge
- Publish a browsable static documentation site with MkDocs

## Documentation site

- GitHub Pages URL: https://yameprogrammer.github.io/go-docs-ko/
- Source docs directory: `docs/ko/`
- Static site tooling: MkDocs + Material theme
- Additional mirrored sections:
  - `docs/ko/go-dev-doc/` (go.dev/doc source mirror)
  - `docs/ko/pkg/std/` (std package summary pages)

## Local preview

From the repository root:

```bash
pip install -r scripts/requirements.txt
mkdocs serve
```

Then open:

- http://127.0.0.1:8000

You can run a strict local build check with:

```bash
mkdocs build --strict
```

## GitHub Pages deployment

- Workflow file: `.github/workflows/deploy-pages.yml`
- Trigger: push to `main` branch (and manual `workflow_dispatch`)
- Build command: `mkdocs build --strict`
- Deploy target: GitHub Pages artifact upload + `actions/deploy-pages`

## Content sync pipelines

- `scripts/translate_docs.py`: syncs and translates Markdown docs from `golang/go`.
- `scripts/sync_go_dev_doc.py`: syncs and translates Markdown docs from `golang/website` `_content/doc`.
- `scripts/generate_std_docs.py`: generates std package summary pages from `go list std`.
  - Optional flags:
    - `--translate-synopsis`: translate package synopsis to Korean.
    - `--include-go-doc-all`: include full API text from `go doc -all <pkg>`.

## Notes

This repository helps Korean readers access Go documentation more easily, but it is not an official Go documentation mirror. The source of truth remains the upstream Go documentation and source repositories.
