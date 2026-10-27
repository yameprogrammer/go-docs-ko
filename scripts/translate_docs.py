#!/usr/bin/env python3

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List

import requests


def run(cmd: List[str], cwd: str | None = None) -> str:
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    return result.stdout.strip()


def clone_source(source_repo: str, source_branch: str, workdir: Path) -> Path:
    repo_dir = workdir / "source"
    if repo_dir.exists():
        shutil.rmtree(repo_dir)

    run(["git", "clone", "--depth", "1", "--branch", source_branch, "--filter=blob:none", source_repo, str(repo_dir)])
    return repo_dir


def list_markdown_files(repo_dir: Path) -> List[Path]:
    output = run(["git", "-C", str(repo_dir), "ls-files", "*.md", "*.mdx", "*.markdown"])
    files = [repo_dir / p for p in output.splitlines() if p]
    allowed = []
    for file_path in files:
        relative = file_path.relative_to(repo_dir)
        path_str = str(relative)
        if path_str.startswith(".github/"):
            continue
        if any(part in {"vendor", "third_party", "node_modules"} for part in path_str.split("/")):
            continue
        if not path_str.lower().endswith((".md", ".mdx", ".markdown")):
            continue
        allowed.append(file_path)
    return allowed


def normalize_output_path(relative_path: str, output_dir: Path) -> Path:
    rel = Path(relative_path)
    target = output_dir / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def chunk_markdown(text: str, max_chars: int = 2200) -> List[str]:
    paragraphs = re.split(r"(\n\s*\n+)", text)
    chunks: List[str] = []
    current = ""
    for part in paragraphs:
        if not part:
            continue
        if len(current) + len(part) > max_chars and current.strip():
            chunks.append(current.strip())
            current = part
        else:
            current += part
    if current.strip():
        chunks.append(current.strip())
    return chunks if chunks else [text.strip()]


def translate_text(provider: str, text: str) -> str:
    provider = provider.lower()
    if provider == "ollama":
        return translate_with_ollama(text)
    if provider == "openai":
        return translate_with_openai(text)
    raise ValueError(f"Unsupported TRANSLATION_PROVIDER: {provider}")


def translate_with_ollama(text: str) -> str:
    base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    model = os.getenv("OLLAMA_MODEL", "llama3.1")
    api_key = os.getenv("OLLAMA_API_KEY")

    endpoint = base_url.rstrip("/") + "/api/chat"
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a careful technical translator. Translate the following Markdown content from English to Korean. "
                    "Preserve Markdown structure, headings, tables, links, lists, inline code, and code fences. "
                    "Do not translate Go package names, identifiers, URLs, commands, or code snippets. "
                    "Return only the translated Markdown."
                ),
            },
            {"role": "user", "content": text},
        ],
        "stream": False,
    }

    response = requests.post(endpoint, headers=headers, json=payload, timeout=180)
    if response.status_code != 200:
        raise RuntimeError(f"Ollama API failed ({response.status_code}): {response.text}")

    response_json = response.json()
    if "message" not in response_json:
        raise RuntimeError(f"Unexpected Ollama response: {response_json}")

    content = response_json["message"].get("content", "")
    if not content:
        raise RuntimeError("Ollama API returned empty content.")
    return content.strip()


def translate_with_openai(text: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required when using the OpenAI translation provider.")

    model = os.getenv("OPENAI_API_MODEL", "gpt-4o-mini")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a careful technical translator. Translate the following Markdown content from English to Korean. "
                    "Preserve Markdown structure, headings, tables, links, lists, inline code, and code fences. "
                    "Do not translate Go package names, identifiers, URLs, commands, or code snippets. "
                    "Return only the translated Markdown."
                ),
            },
            {"role": "user", "content": text},
        ],
        "temperature": 0.2,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(f"{base_url.rstrip('/')}/chat/completions", headers=headers, json=payload, timeout=180)
    if response.status_code != 200:
        raise RuntimeError(f"OpenAI API call failed ({response.status_code}): {response.text}")

    payload_json = response.json()
    choices = payload_json.get("choices", [])
    if not choices:
        raise RuntimeError(f"OpenAI API returned no choices: {payload_json}")

    content = choices[0].get("message", {}).get("content", "")
    if not content:
        raise RuntimeError("OpenAI API returned empty content.")
    return content.strip()


def protect_markdown_sections(markdown: str) -> List[str]:
    sections: List[str] = []
    current: List[str] = []
    in_code_block = False
    fence = ""

    for line in markdown.splitlines():
        if line.startswith("```") or line.startswith("~~~"):
            current.append(line)
            if not in_code_block:
                in_code_block = True
                fence = line[:3]
            elif line.startswith(fence):
                in_code_block = False
                fence = ""
            continue

        if not in_code_block and line.strip() == "":
            if current:
                sections.append("\n".join(current).strip())
                current = []
            continue

        current.append(line)

    if current:
        sections.append("\n".join(current).strip())

    return [part for part in sections if part.strip()]


def translate_markdown_file(file_path: Path, output_file: Path, provider: str) -> None:
    original = file_path.read_text(encoding="utf-8")
    if not original.strip():
        return

    translated_sections: List[str] = []
    segments = protect_markdown_sections(original)
    for segment in segments:
        for chunk in chunk_markdown(segment):
            translated_sections.append(translate_text(provider, chunk))

    translated = "\n\n".join(translated_sections).strip() + "\n"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(translated, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync Go official docs and translate selected Markdown files to Korean.")
    parser.add_argument("--source-repo", required=True)
    parser.add_argument("--source-branch", default="master")
    parser.add_argument("--output-dir", default="docs/ko")
    args = parser.parse_args()

    provider = os.getenv("TRANSLATION_PROVIDER", "ollama").lower()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp_dir:
        workdir = Path(tmp_dir)
        source_dir = clone_source(args.source_repo, args.source_branch, workdir)
        markdown_files = list_markdown_files(source_dir)

        if not markdown_files:
            print("No Markdown files matched the selected source repository.")
            return 0

        for file_path in markdown_files:
            relative = file_path.relative_to(source_dir)
            output_file = normalize_output_path(str(relative), output_dir)
            try:
                translate_markdown_file(file_path, output_file, provider)
                print(f"Translated: {relative} -> {output_file}")
            except Exception as exc:
                print(f"Skipping {relative}: {exc}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)