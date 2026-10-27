#!/usr/bin/env python3

import argparse
import os
import shutil
import sys
import tempfile
from pathlib import Path

from translate_docs import clone_source, list_markdown_files, translate_markdown_file


def sanitize_for_mkdocs(markdown: str) -> str:
    if markdown.startswith("---\n"):
        end = markdown.find("\n---\n", 4)
        if end != -1:
            markdown = markdown[end + 5 :]
            if markdown.startswith("\n"):
                markdown = markdown[1:]
    return markdown


def build_index(output_dir: Path, translated_files: list[Path]) -> None:
    rel_paths = sorted([p.relative_to(output_dir) for p in translated_files if p.name != "index.md"])
    grouped: dict[str, list[Path]] = {}
    for rel in rel_paths:
        top = rel.parts[0] if len(rel.parts) > 1 else "top-level"
        grouped.setdefault(top, []).append(rel)

    lines = [
        "# go.dev/doc 미러 문서",
        "",
        "이 디렉터리는 `golang/website` 저장소의 `_content/doc` 문서를 기반으로 생성됩니다.",
        "",
        "- 원문 권위: <https://go.dev/doc>",
        "- 이 저장소는 비공식 한국어 번역 미러입니다.",
        "",
        "## 문서 섹션",
        "",
        "> 전체 페이지는 사이트 검색으로도 빠르게 찾을 수 있습니다.",
        "",
    ]
    for section in sorted(grouped.keys()):
        title = "Top-level" if section == "top-level" else section
        lines.append(f"### {title}")
        lines.append("")
        for rel in grouped[section]:
            label = rel.name if section != "top-level" else rel.as_posix()
            lines.append(f"- [{label}]({rel.as_posix()})")
        lines.append("")
    lines.append("")
    (output_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync and translate go.dev/doc markdown sources.")
    parser.add_argument("--source-repo", default="https://github.com/golang/website.git")
    parser.add_argument("--source-branch", default="master")
    parser.add_argument("--output-dir", default="docs/ko/go-dev-doc")
    parser.add_argument("--translate", action="store_true")
    parser.add_argument("--index-only", action="store_true")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    provider = os.getenv("TRANSLATION_PROVIDER", "ollama").lower()
    if args.index_only:
        existing = [p for p in output_dir.rglob("*.md") if p.name != "index.md"]
        build_index(output_dir, existing)
        print(f"Rebuilt index from existing files: {output_dir / 'index.md'}")
        return 0

    with tempfile.TemporaryDirectory() as tmp_dir:
        workdir = Path(tmp_dir)
        source_dir = clone_source(args.source_repo, args.source_branch, workdir)
        doc_root = source_dir / "_content" / "doc"
        if not doc_root.exists():
            raise RuntimeError(f"Missing expected path in source repository: {doc_root}")

        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        markdown_files = list_markdown_files(source_dir)
        selected = [p for p in markdown_files if p.is_relative_to(doc_root)]

        translated_outputs: list[Path] = []
        for file_path in selected:
            relative = file_path.relative_to(doc_root)
            output_file = output_dir / relative
            output_file.parent.mkdir(parents=True, exist_ok=True)
            status = "translated"
            if not args.translate:
                source_text = file_path.read_text(encoding="utf-8")
                output_file.write_text(sanitize_for_mkdocs(source_text), encoding="utf-8")
                status = "copied"
            else:
                try:
                    translate_markdown_file(file_path, output_file, provider=provider)
                    translated_text = output_file.read_text(encoding="utf-8")
                    output_file.write_text(sanitize_for_mkdocs(translated_text), encoding="utf-8")
                except Exception as exc:
                    source_text = file_path.read_text(encoding="utf-8")
                    output_file.write_text(sanitize_for_mkdocs(source_text), encoding="utf-8")
                    status = "copied"
                    print(f"Fallback copied without translation: {relative} ({exc})", file=sys.stderr)
            translated_outputs.append(output_file)
            print(f"{status}: {file_path.relative_to(source_dir)} -> {output_file}")

        build_index(output_dir, translated_outputs)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
