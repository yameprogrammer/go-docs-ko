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
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    provider = os.getenv("TRANSLATION_PROVIDER", "ollama").lower()
    list_output = run(["go", "list", "-f", "{{.ImportPath}}\t{{.Doc}}", "std"])
    packages = parse_std_packages(list_output)

    index_lines = [
        "# Go 표준 라이브러리 문서 미러",
        "",
        "- 원문: <https://pkg.go.dev/std>",
        "- 이 디렉터리는 `go list std` 결과를 기반으로 생성됩니다.",
        "- API 상세의 권위 있는 원문은 pkg.go.dev 및 golang/go입니다.",
        "",
        "## 패키지 섹션",
        "",
    ]
    grouped: dict[str, list[tuple[str, str]]] = {}

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

        rel_path = page_path.relative_to(output_dir).as_posix()
        top = import_path.split("/", 1)[0]
        grouped.setdefault(top, []).append((import_path, rel_path))
        print(f"Generated: {page_path}")

    for section in sorted(grouped.keys()):
        index_lines.append(f"### {section}")
        index_lines.append("")
        for import_path, rel_path in grouped[section]:
            index_lines.append(f"- [{import_path}]({rel_path})")
        index_lines.append("")

    (output_dir / "index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
