# Go Official Docs Korean Mirror

This repository is an unofficial, AI-assisted Korean translation mirror of the Go official documentation.

Important notice:
- The original Go documentation is maintained by the Go project and its contributors.
- This repository is not affiliated with, endorsed by, or officially maintained by the Go project.
- This project is intended as a community translation and reference mirror.
- For authoritative content, always check the original Go documentation at https://go.dev and the source repository https://github.com/golang/go.

## Goals
- Keep a Korean translation mirror synced with upstream Go documentation
- Use GitHub Actions to automate synchronization and translation
- Generate pull requests for human review before merge

## Supported translation backends
This repository supports:
- ollama
- openai

## Required environment variables
- OLLAMA_API_KEY
- OLLAMA_BASE_URL
- OLLAMA_MODEL
- OPENAI_API_KEY
- OPENAI_API_MODEL

## Quick start
1. Configure the repo secrets/variables
2. Commit the workflow and script files
3. Run the workflow from the Actions tab
4. Review the generated PR

## Notes
This repository is meant to help Korean readers access Go documentation more easily, but it is not an official Go documentation mirror.
