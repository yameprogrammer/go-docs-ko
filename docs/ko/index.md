# Go 문서 한국어 미러

이 사이트는 **Go 공식 문서의 비공식 한국어 번역 미러**입니다.

- 원문 문서의 권위(authoritative source)는 [go.dev](https://go.dev/doc) 및 [golang/go](https://github.com/golang/go)에 있습니다.
- 이 저장소([yameprogrammer/go-docs-ko](https://github.com/yameprogrammer/go-docs-ko))는 한국어 커뮤니티 번역과 참고를 위한 미러 프로젝트입니다.
- 공식 Go 프로젝트와는 별개의 커뮤니티 저장소입니다.

## 로컬 미리보기

저장소 루트에서 다음 명령으로 로컬 미리보기를 실행할 수 있습니다.

```bash
pip install -r scripts/requirements.txt
mkdocs serve
```

실행 후 브라우저에서 <http://127.0.0.1:8000> 으로 접속하세요.

## GitHub Pages 배포

이 저장소는 `main` 브랜치에 push 되면 GitHub Actions가 정적 사이트를 빌드하고 GitHub Pages로 배포합니다.

- 배포 URL: <https://yameprogrammer.github.io/go-docs-ko/>
- 빌드 검증 명령: `mkdocs build --strict`

## 문서 구조

문서 원본은 `docs/ko/` 아래에 있으며, 기존 Go 문서 관련 파일 구조를 그대로 유지합니다.

- `doc/`: 기존 Go 문서 및 릴리스 노트 관련 번역
- `go-dev-doc/`: `go.dev/doc` 계열 미러 문서
- `pkg/std/`: `pkg.go.dev/std` 기반 표준 라이브러리 패키지 요약 문서
