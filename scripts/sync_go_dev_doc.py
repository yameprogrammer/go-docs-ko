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
    rel_set = {p.as_posix() for p in rel_paths}

    def pick(path: str) -> str | None:
        return path if path in rel_set else None

    learning_paths: list[tuple[str, list[str]]] = [
        (
            "입문 시작 (설치와 기본 개념)",
            [p for p in [pick("root.md"), pick("install-source.md"), pick("faq.md"), pick("go1.md")] if p],
        ),
        (
            "실무 튜토리얼 (따라 하며 학습)",
            [
                p
                for p in [
                    pick("tutorial/json.md"),
                    pick("tutorial/database-access.md"),
                    pick("tutorial/web-service-gin.md"),
                    pick("tutorial/workspaces.md"),
                ]
                if p
            ],
        ),
        (
            "모듈/의존성 관리",
            [
                p
                for p in [
                    pick("modules/developing.md"),
                    pick("modules/managing-dependencies.md"),
                    pick("modules/release-workflow.md"),
                    pick("modules/version-numbers.md"),
                ]
                if p
            ],
        ),
        (
            "운영/보안 심화",
            [
                p
                for p in [
                    pick("security/best-practices.md"),
                    pick("security/threat-model.md"),
                    pick("security/vulncheck.md"),
                    pick("toolchain.md"),
                    pick("telemetry.md"),
                ]
                if p
            ],
        ),
    ]

    grouped: dict[str, list[Path]] = {}
    for rel in rel_paths:
        key = rel.parts[0] if len(rel.parts) > 1 else "top-level"
        grouped.setdefault(key, []).append(rel)

    section_order = ["tutorial", "database", "modules", "security", "top-level"]
    section_titles = {
        "tutorial": "튜토리얼",
        "database": "데이터베이스",
        "modules": "모듈",
        "security": "보안",
        "top-level": "기타 문서",
    }

    lines = [
        "# go.dev/doc 학습 허브",
        "",
        "이 섹션은 `go.dev/doc` 문서를 한국어로 따라가기 쉽게 정리한 학습 허브입니다.",
        "",
        "- 원문 권위: <https://go.dev/doc>",
        "- 이 저장소는 비공식 한국어 번역 미러입니다.",
        "",
        "## 추천 학습 순서",
        "",
    ]
    for title, items in learning_paths:
        if not items:
            continue
        lines.append(f"### {title}")
        lines.append("")
        for item in items:
            label = item.replace(".md", "")
            lines.append(f"- [{label}]({item})")
        lines.append("")

    lines.extend(
        [
            "## 주제별 문서 탐색",
            "",
            "관심 주제별로 바로 이동하세요.",
            "",
        ]
    )

    for key in section_order:
        if key not in grouped:
            continue
        lines.append(f"### {section_titles[key]}")
        lines.append("")
        for rel in grouped[key]:
            rel_str = rel.as_posix()
            label = rel_str.replace(".md", "")
            lines.append(f"- [{label}]({rel_str})")
        lines.append("")

    for key in sorted(grouped.keys()):
        if key in section_order:
            continue
        lines.append(f"### {key}")
        lines.append("")
        for rel in grouped[key]:
            rel_str = rel.as_posix()
            label = rel_str.replace(".md", "")
            lines.append(f"- [{label}]({rel_str})")
        lines.append("")

    lines.extend(
        [
            "## 읽는 방법",
            "",
            "1. **추천 학습 순서**에서 1개 트랙을 고릅니다.",
            "2. 각 문서의 예제 코드를 로컬에서 직접 실행합니다.",
            "3. 필요할 때 주제별 문서 탐색에서 관련 심화 문서를 확장합니다.",
            "",
            "> 전체 문서는 사이트 상단 검색으로도 빠르게 찾을 수 있습니다.",
            "",
        ]
    )
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
