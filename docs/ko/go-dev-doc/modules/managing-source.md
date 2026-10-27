<!--{
  "제목": "모듈 소스 관리"
}-->

다른 개발자들이 사용하기 쉽도록 모듈을 개발할 때, 이 주제에 설명된 저장소 규칙을 따르면, 다음과 같은 사항을 보장할 수 있습니다.

이 주제는 모듈 저장소를 관리할 때 취할 수 있는 작업을 설명합니다. 버전 간 변경 사항을 적용하는 데 필요한 워크플로우 단계의 순서에 대한 정보는 [모듈 출시 및 버전 관리 워크플로우](release-workflow)를 참조하십시오.

여기 설명된 일부 규칙은 모듈에서 필수적이며, 다른 규칙은 권장 사항입니다. 이 내용은 [의존성 관리](/doc/modules/managing-dependencies)에 설명된 기본적인 모듈 사용 관행에 대한 이해를 전제로 합니다.

Go는 다음 저장소를 사용하여 모듈을 게시할 수 있습니다: Git, Subversion,
Mercurial, Bazaar, Fossil.

모듈 개발에 대한 개요는 [모듈 개발 및 배포](developing)를 참조하십시오.

## Go 도구가 게시된 모듈을 찾는 방법 {#tools}

Go 도구는 다음과 같은 방법으로 게시된 모듈을 찾습니다.

*   **Go Modules 저장소:** Go Modules 저장소에서 모듈의 정보를 찾습니다.
*   **Go Packages:** Go Modules 저장소에서 모듈을 가져올 수 있는 Go Packages를 찾습니다.
*   **Go Modules.yaml 파일:** 모듈에 있는 `go.mod` 파일에서 모듈의 메타데이터를 찾습니다.

다음은 Go Modules 저장소에서 모듈을 찾는 방법에 대한 예입니다.

```bash
go mod init mymodule
```

이 명령은 `myproject/myproject/go.mod`라는 새 Go Modules 파일을 생성합니다. 이 파일에는 모듈의 이름, 버전 및 Go Packages 목록이 포함됩니다.

Go의 분산 시스템에서 모듈을 게시하고 코드를 저장하는 방식은 다음과 같습니다.

Go 도구는 저장소 경로와 저장소 태그를 사용하여 모듈의 이름과 버전을 식별하는 명명 규칙에 의존합니다. 저장소가 이러한 요구 사항을 충족하면, Go 도구 (예: [`go get`
명령어](/ref/mod#go-get))를 사용하여 저장소에서 모듈 코드를 다운로드할 수 있습니다.

개발자가 `go get` 명령을 사용하여 패키지의 소스 코드를 가져올 때, 이 명령은 다음과 같은 작업을 수행합니다:

1. Go 소스 코드의 `import` 문에서, `go get`는 패키지 경로 내의 모듈 경로를 식별합니다.
1. 모듈 경로에서 파생된 URL을 사용하여, 명령은 모듈을 모듈 프록시 서버 또는 직접 저장소에서 찾습니다.
1. 저장소 태그에 모듈 버전을 일치시켜 저장소에서 코드를 찾고, 다운로드할 모듈 버전을 찾습니다. 버전 번호를 아직 알지 못하는 경우, `go get`은 최신 릴리스 버전을 찾습니다.
1. 모듈 소스 및 해당 파일을 개발자의 로컬 모듈 캐시에 가져옵니다.

## 저장소 내 코드 정리 {#repository}

```
// Example Go code
package main
```

| Feature | Description |
|---|---|
| File Naming | Use descriptive file names.  예: `user_authentication.go` 대신 `auth_utils.go` 사용 |
| Directory Structure | Organize files into logical directories. 예: `src/auth/`, `src/utils/` 등 |
| Code Comments | Add clear and concise comments to explain the code. |
| Code Formatting | Use a consistent code style (e.g., using `go fmt`). |
| Version Control | Use Git for version control. |

다음에서 설명된 규칙을 따르면, 사용자가 모듈을 유지 관리하는 것을 쉽고, 개발자의 경험을 향상시킬 수 있습니다. 모듈 코드를 저장소에 넣는 것은 일반적으로 다른 코드와 마찬가지로 간단합니다.

다음 다이어그램은 간단한 모듈의 두 패키지를 위한 소스 계층 구조를 보여줍니다.

<img src="images/source-hierarchy.png"
     alt="모듈 소스 코드 계층 구조를 설명하는 다이어그램"
     style="width: 250px;" />

초기 커밋에는 다음 표에 나열된 파일이 포함되어야 합니다:

```markdown
<table id="module-files" class="DocTable">
  <thead>
    <tr class="DocTable-head">
      <th class="DocTable-cell" width="20%">파일</th>
      <th class="DocTable-cell">설명</th>
    </tr>
  </thead>
  <tbody>
    <tr class="DocTable-row">
      <td class="DocTable-cell">LICENSE</td>
      <td class="DocTable-cell">모듈의 라이선스.</td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">go.mod</td>
      <td class="DocTable-cell"><p>모듈에 대한 설명, 여기에는 모듈 경로 (실질적으로 이름) 및 종속성이 포함됩니다. 자세한 내용은 <a href="gomod-ref">go.mod 참조</a>를 참조하십시오.</p>
        <p>모듈 경로는 모듈 지시어에서 지정됩니다. 예를 들면 다음과 같습니다.</p>
        <pre>module example.com/mymodule</pre>
        <p>모듈 경로를 선택하는 방법에 대한 자세한 내용은 <a href="/doc/modules/managing-dependencies#naming_module">종속성 관리</a>를 참조하십시오.</p>
        <p>go.mod 파일을 편집할 수 있지만, <code>go</code> 명령을 사용하여 변경하는 것이 더 안정적입니다.</p>
      </td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">go.sum</td>
      <td class="DocTable-cell"><p>모듈의 종속성을 나타내는 암호화 해시를 포함합니다. Go 도구는 이러한 해시를 사용하여 다운로드한 모듈을 인증하려고 시도하여 다운로드한 모듈이 유효한지 확인합니다. 이 확인이 실패하면 Go는 보안 오류를 표시합니다.</p>
      <p>종속성이 없는 경우 이 파일은 비어 있거나 존재하지 않습니다. <code>go mod tidy</code> 명령을 사용하여 이 파일을 수정하지 마십시오. 이 명령은 불필요한 항목을 제거합니다.</p>
      </td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">패키지 디렉토리 및 .go 소스.</td>
      <td class="DocTable-cell">모듈에 포함된 Go 패키지 및 소스의 디렉토리 및 .go 파일.</td>
    </tr>
  </tbody>
</table

명령줄에서, 빈 리포지토리를 생성하고, 초기 커밋에 포함될 파일들을 추가하고, 메시지와 함께 커밋할 수 있습니다. 여기에는 git을 사용하는 예제가 있습니다:

```
$ git init
$ git add --all
$ git commit -m "mycode: 초기 커밋"
$ git push
```

## 저장소 범위 선택 {#repository-scope}

코드를 모듈로 게시할 때, 코드가 다른 모듈의 코드와 독립적으로 버전 관리될 수 있도록 해야 합니다.

여러 모듈을 하나의 저장소에 유지하는 것은 유지 관리를 더 쉽게 만들어 줍니다. 특히 새로운 미소 및 패치 버전을 게시하고, 새로운 주요 버전으로 분기하는 등 시간이 지남에 따라 더욱 그렇습니다. 그러나 필요에 따라, 하나의 저장소에서 여러 모듈을 유지 관리할 수도 있습니다.

### 하나의 모듈을 하나의 저장소에 소싱하기 {#하나-모듈-소스}

```
# Sourcing one module per repository {#one-module-source}
```

단일 모듈의 소스만 포함하는 저장소를 유지할 수 있습니다. 이 모델에서는 저장소의 루트에 `go.mod` 파일을 배치하고, 그 아래에 Go 소스 파일이 포함된 패키지 하위 디렉토리를 만듭니다.

이것은 가장 간단한 방법이며, 시간이 지남에 따라 모듈을 관리하는 데 도움이 됩니다. 이를 통해 모듈 버전 번호를 디렉토리 경로와 함께 지정할 필요가 없습니다.

<img src="images/single-module.png"
     alt="저장소 내의 단일 모듈의 소스에 대한 다이어그램"
     style="width: 425px;" />

### 단일 저장소에서 여러 모듈 소싱하기 {#여러-모듈-소스}

단일 저장소에서 여러 모듈을 게시할 수 있습니다. 예를 들어, 하나의 저장소에 여러 모듈을 구성하는 코드가 있을 수 있지만, 해당 모듈을 개별적으로 버전 관리하고 싶을 수 있습니다.

각 서브 디렉터리, 즉 모듈 루트 디렉터리는 자체 `go.mod` 파일을 가져야 합니다.

서브디렉토리에 있는 모듈 코드를 가져오면, 모듈을 게시할 때 사용해야 하는 버전 태그 형식이 변경됩니다. 태그의 버전 번호 부분을 모듈의 루트 디렉토리 이름으로 접두사로 지정해야 합니다. 버전 번호에 대한 자세한 내용은 [모듈 버전 번호 지정](/doc/modules/version-numbers)를 참조하십시오.

다음 예시를 참조하여, `example.com/mymodules/module1` 모듈의 경우, 버전 v1.2.3에 대한 다음과 같은 내용을 제공합니다.

*   모듈 경로: `example.com/mymodules/module1`
*   버전 태그: `module1/v1.2.3`
*   사용자가 가져오는 패키지 경로: `example.com/mymodules/module1/package1`
*   사용자의 `require` 지시문에 명시된 모듈 경로 및 버전: `example.com/mymodules/module1 v1.2.3`

<img src="images/multiple-modules.png"
     alt="단일 저장소 내의 두 모듈을 설명하는 다이어그램"
     style="width: 480px;" />
