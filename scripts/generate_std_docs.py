#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
from pathlib import Path

from translate_docs import translate_text


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, text=True, capture_output=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    return result.stdout


def parse_std_packages(output: str) -> list[tuple[str, str]]:
    packages: list[tuple[str, str]] = []
    for line in output.splitlines():
        if not line.strip():
            continue
        if "\t" in line:
            import_path, doc = line.split("\t", 1)
        else:
            import_path, doc = line.strip(), ""
        packages.append((import_path.strip(), doc.strip()))
    return packages


def classify_domain(import_path: str) -> str:
    domain_rules = [
        ("웹/네트워크", ("net", "net/http", "net/url", "mime", "html")),
        ("데이터 처리", ("encoding", "bytes", "strings", "strconv", "unicode", "regexp")),
        ("입출력/파일", ("io", "io/fs", "os", "path", "archive", "compress", "bufio")),
        ("동시성/런타임", ("context", "sync", "sync/atomic", "time", "runtime")),
        ("보안/암호화", ("crypto", "hash")),
        ("개발도구/언어", ("testing", "go/", "reflect", "unsafe", "flag", "log", "fmt", "errors")),
    ]
    for name, prefixes in domain_rules:
        for prefix in prefixes:
            if import_path == prefix or import_path.startswith(prefix + "/"):
                return name
    return "기타"


def build_std_index(output_dir: Path, package_paths: list[str]) -> None:
    sorted_packages = sorted(set(package_paths))
    domain_groups: dict[str, list[str]] = {}
    for pkg in sorted_packages:
        domain = classify_domain(pkg)
        domain_groups.setdefault(domain, []).append(pkg)

    def exists(pkg: str) -> bool:
        return pkg in sorted_packages

    learning_tracks: list[tuple[str, list[str]]] = [
        (
            "입문 트랙 (기본 문법/출력/오류)",
            [p for p in ["fmt", "errors", "strings", "strconv"] if exists(p)],
        ),
        (
            "백엔드 실무 트랙 (HTTP/JSON/컨텍스트)",
            [p for p in ["net/http", "encoding/json", "context", "io"] if exists(p)],
        ),
        (
            "데이터/스토리지 트랙",
            [p for p in ["database/sql", "encoding/csv", "encoding/xml", "bufio"] if exists(p)],
        ),
        (
            "동시성/운영 트랙",
            [p for p in ["sync", "sync/atomic", "time", "os/signal", "runtime"] if exists(p)],
        ),
    ]

    lines = [
        "# Go 표준 라이브러리 학습 허브",
        "",
        "- 원문: <https://pkg.go.dev/std>",
        "- 각 패키지 페이지에는 한국어 요약과 `go doc -all` API 상세가 포함됩니다.",
        "- API 권위 원문은 pkg.go.dev 및 golang/go입니다.",
        "",
        "## 추천 학습 트랙",
        "",
    ]
    for title, items in learning_tracks:
        if not items:
            continue
        lines.append(f"### {title}")
        lines.append("")
        for pkg in items:
            lines.append(f"- [{pkg}]({pkg}.md)")
        lines.append("")

    lines.extend(
        [
            "## 도메인별 패키지 탐색",
            "",
            "관심 있는 주제부터 선택해서 학습하세요.",
            "",
        ]
    )

    domain_order = ["입출력/파일", "데이터 처리", "웹/네트워크", "동시성/런타임", "보안/암호화", "개발도구/언어", "기타"]
    for domain in domain_order:
        pkgs = domain_groups.get(domain, [])
        if not pkgs:
            continue
        lines.append(f"### {domain}")
        lines.append("")
        for pkg in pkgs:
            lines.append(f"- [{pkg}]({pkg}.md)")
        lines.append("")

    lines.extend(
        [
            "## 읽는 방법",
            "",
            "1. 추천 학습 트랙에서 목표에 맞는 트랙을 고릅니다.",
            "2. 패키지 페이지의 **한국어 요약**으로 개념을 먼저 파악합니다.",
            "3. 필요할 때 **API 상세 (go doc -all)** 섹션으로 내려가 시그니처/동작을 확인합니다.",
            "",
        ]
    )
    (output_dir / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_std_page(import_path: str, synopsis: str, translated_synopsis: str) -> str:
    lines = [
        f"# package {import_path}",
        "",
        f"- 원문: <https://pkg.go.dev/{import_path}>",
        "- 분류: Go 표준 라이브러리",
        "",
        "## 한국어 요약",
        "",
        translated_synopsis or "_요약이 비어 있습니다._",
        "",
        "## 원문 요약",
        "",
        synopsis or "_Synopsis is empty._",
        "",
        "> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.",
        "",
    ]
    return "\n".join(lines)


def build_std_page_with_full_doc(
    import_path: str,
    synopsis: str,
    translated_synopsis: str,
    full_doc: str,
) -> str:
    lines = [
        f"# package {import_path}",
        "",
        f"- 원문: <https://pkg.go.dev/{import_path}>",
        "- 분류: Go 표준 라이브러리",
        "",
        "## 한국어 요약",
        "",
        translated_synopsis or "_요약이 비어 있습니다._",
        "",
        "## 원문 요약",
        "",
        synopsis or "_Synopsis is empty._",
        "",
        "## API 상세 (go doc -all)",
        "",
        "~~~text",
        full_doc.rstrip(),
        "~~~",
        "",
        "> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate markdown pages for Go std packages.")
    parser.add_argument("--output-dir", default="docs/ko/pkg/std")
    parser.add_argument("--translate-synopsis", action="store_true")
    parser.add_argument("--include-go-doc-all", action="store_true")
    parser.add_argument("--index-only", action="store_true")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.index_only:
        existing = [
            p.relative_to(output_dir).as_posix().replace(".md", "")
            for p in output_dir.rglob("*.md")
            if p.name != "index.md"
        ]
        build_std_index(output_dir, existing)
        print(f"Rebuilt std index from existing files: {output_dir / 'index.md'}")
        return 0

    provider = os.getenv("TRANSLATION_PROVIDER", "ollama").lower()
    list_output = run(["go", "list", "-f", "{{.ImportPath}}\t{{.Doc}}", "std"])
    packages = parse_std_packages(list_output)
    package_paths: list[str] = []

    for import_path, synopsis in packages:
        translated_synopsis = synopsis
        if args.translate_synopsis and synopsis:
            try:
                translated_synopsis = translate_text(provider, synopsis)
            except Exception as exc:
                translated_synopsis = synopsis
                print(f"Fallback to original synopsis for {import_path}: {exc}", file=sys.stderr)

        page_path = output_dir / f"{import_path}.md"
        page_path.parent.mkdir(parents=True, exist_ok=True)
        page_content = build_std_page(import_path, synopsis, translated_synopsis)
        if args.include_go_doc_all:
            try:
                full_doc = run(["go", "doc", "-all", import_path]).strip()
                page_content = build_std_page_with_full_doc(
                    import_path=import_path,
                    synopsis=synopsis,
                    translated_synopsis=translated_synopsis,
                    full_doc=full_doc,
                )
            except Exception as exc:
                print(f"Failed to include go doc -all for {import_path}: {exc}", file=sys.stderr)

        page_path.write_text(page_content, encoding="utf-8")
        package_paths.append(import_path)
        print(f"Generated: {page_path}")

    build_std_index(output_dir, package_paths)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
