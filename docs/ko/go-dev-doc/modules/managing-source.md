<!--{
  "Title": "모듈 소스 관리"
}-->

다른 개발자들이 사용할 수 있도록 게시할 모듈을 개발할 때, 이 주제에서 설명하는 저장소 컨벤션을 따르면 다른 개발자들이 귀하의 모듈을 더 쉽게 사용할 수 있도록 도울 수 있습니다.

이 주제에서는 모듈 저장소를 관리할 때 수행할 수 있는 작업들에 대해 설명합니다. 버전별 수정 시 수행해야 하는 워크플로우 단계의 순서에 대한 정보는 [Module release and versioning workflow](release-workflow)를 참조하십시오.

여기에서 설명하는 컨벤션 중 일부는 모듈에서 필수적으로 요구되는 사항이며, 일부는 권장되는 모범 사례(best practices)입니다. 이 내용은 [Managing dependencies](/doc/modules/managing-dependencies)에서 설명하는 기본적인 모듈 사용 관행에 익숙하다는 가정하에 작성되었습니다.

Go는 모듈 게시를 위해 Git, Subversion, Mercurial, Bazaar 및 Fossil 리포지토리를 지원합니다.

모듈 개발에 대한 개요는 [Developing and publishing modules](developing)를 참조하십시오.

## Go 도구가 게시된 모듈을 찾는 방법 {#tools}

Go의 모듈 게시 및 코드 검색을 위한 분산 시스템에서는, 코드를 저장소에 그대로 둔 채로 모듈을 게시할 수 있습니다. Go 도구들은 모듈의 이름과 버전 번호를 나타내는 저장소 경로 및 저장소 태그가 포함된 명명 규칙에 의존합니다. 저장소가 이러한 요구 사항을 따르면, [`go get` 명령어](/ref/mod#go-get)와 같은 Go 도구를 통해 저장소에서 모듈 코드를 다운로드할 수 있습니다.

개발자가 자신의 코드에서 임포트하는 패키지의 소스 코드를 가져오기 위해 `go get` 명령어를 사용하면, 해당 명령어는 다음과 같은 작업을 수행합니다.

1. Go 소스 코드의 `import` 문에서 `go get`은 패키지 경로 내의 모듈 경로를 식별합니다.
1. 모듈 경로에서 파생된 URL을 사용하여, 해당 명령은 모듈 프록시 서버 또는 리포지토리에서 직접 모듈 소스를 찾습니다.
1. 모듈의 버전 번호를 리포지토리 태그와 매칭하여 다운로드할 모듈 버전의 소스를 찾고 리포지토리 내의 코드를 발견합니다. 사용할 버전 번호를 아직 알 수 없는 경우, `go get`은 최신 릴리스 버전을 찾습니다.
1. 모듈 소스를 검색하여 개발자의 로컬 모듈 캐시에 다운로드합니다.

## 리포지토리 내 코드 구성 {#repository}

여기에 설명된 컨벤션을 따르면 모듈의 유지관리를 간소화하고 개발자 경험을 향상시킬 수 있습니다. 모듈 코드를 저장소에 넣는 과정은 일반적으로 다른 코드와 마찬가지로 간단합니다.

다음 다이어그램은 두 개의 패키지로 구성된 단순한 모듈의 소스 계층 구조를 보여줍니다.

<img src="images/source-hierarchy.png"
     alt="모듈 소스 코드 계층 구조를 보여주는 다이어그램"
     style="width: 250px;" />

첫 번째 커밋에는 다음 표에 나열된 파일들이 포함되어야 합니다:

<table id="module-files" class="DocTable">
  <thead>
    <tr class="DocTable-head">
      <th class="DocTable-cell" width="20%">File</th>
      <th class="DocTable-cell">Description</th>
    </tr>
  </thead>
  <tbody style="text-align: left;">
    <tr class="DocTable-row">
      <td class="DocTable-cell">LICENSE</td>
      <td class="DocTable-cell">모듈의 라이선스입니다.</td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">go.mod</td>
      <td class="DocTable-cell">
        <p>모듈 경로(사실상 모듈 이름)와 의존성을 포함하여 모듈을 설명합니다. 자세한 내용은
        <a href="gomod-ref">go.mod reference</a>를 참조하십시오.</p>
        <p>모듈 경로는 다음과 같은 모듈 지시어(directive)로 지정됩니다:</p>
        <pre>module example.com/mymodule</pre>
        <p>모듈 경로 선택에 관한 자세한 내용은
        <a href="/doc/modules/managing-dependencies#naming_module">Managing
        dependencies</a>를 참조하십시오.</p>
        <p>go.mod 파일을 직접 편집할 수도 있지만, <code>go</code> 명령어를 통해
        변경 사항을 적용하는 것이 더 안정적입니다.</p>
      </td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">go.sum</td>
      <td class="DocTable-cell">
        <p>모듈의 의존성을 나타내는 암호화 해시를 포함합니다. Go 도구는 이 해시를 사용하여
        다운로드한 모듈을 인증하며, 다운로드된 모듈이 정당한 것인지 확인하려고 시도합니다.
        이 확인이 실패하면 Go는 보안 오류를 표시합니다.</p>
        <p>의존성이 없는 경우 이 파일은 비어 있거나 존재하지 않습니다.
        불필요한 항목을 제거하는 <code>go mod tidy</code> 명령어를 사용하는 것 외에는
        이 파일을 편집해서는 안 됩니다.</p>
      </td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">Package directories and .go sources.</td>
      <td class="DocTable-cell">모듈 내의 Go 패키지와 소스를 구성하는 디렉토리 및 .go 파일들입니다.</td>
    </tr>
  </tbody>
</table>

명령줄(command-line)에서 빈 저장소를 생성하고, 초기 커밋에 포함될 파일들을 추가한 다음, 메시지와 함께 커밋할 수 있습니다. 다음은 git을 사용한 예시입니다:

```
$ git init
$ git add --all
$ git commit -m "mycode: initial commit"
$ git push
```

## 리포지토리 범위 선택하기 {#repository-scope}

코드가 다른 모듈의 코드와 독립적으로 버전 관리가 되어야 할 때, 해당 코드를 모듈로 발행합니다.

저장소의 루트 디렉토리에 단일 모듈만 호스팅하도록 설계하면, 특히 시간이 지나 새로운 마이너 및 패치 버전을 게시하거나 새로운 메이저 버전으로 브랜치를 나눌 때 유지 관리를 더 단순하게 유지하는 데 도움이 됩니다. 하지만 필요에 따라 단일 저장소에서 여러 모듈 모음을 유지 관리할 수도 있습니다.

### 리포지토리당 하나의 모듈 소싱하기 {#one-module-source}

단일 모듈의 소스만 포함하는 저장소를 유지 관리할 수 있습니다. 이 모델에서는 `go.mod` 파일을 저장소 루트에 두고, 그 아래에 Go 소스가 포함된 패키지 하위 디렉토리를 배치합니다.

이것은 가장 단순한 접근 방식으로, 시간이 지나도 모듈을 더 쉽게 관리할 수 있게 해줍니다. 또한 모듈 버전 번호 앞에 디렉터리 경로를 접두사로 붙여야 하는 번거로움을 피할 수 있도록 도와줍니다.

<img src="images/single-module.png"
     alt="리포지토리 내 단일 모듈의 소스를 보여주는 다이어그램"
     style="width: 425px;" />

### 단일 저장소에서 여러 모듈 소싱하기 {#multiple-module-source}

단일 리포지토리에서 여러 모듈을 게시할 수 있습니다. 예를 들어, 단일 리포지토리 내에 여러 모듈을 구성하는 코드가 있지만, 해당 모듈들의 버전을 각각 별도로 관리하고 싶은 경우가 있을 수 있습니다.

모듈 루트 디렉토리인 각 하위 디렉토리는 자체적인 `go.mod` 파일을 가져야 합니다.

하위 디렉토리에 있는 모듈 코드를 소싱하는 경우, 모듈을 게시할 때 사용해야 하는 버전 태그의 형식이 변경됩니다. 태그의 버전 번호 부분 앞에 모듈 루트인 하위 디렉토리의 이름을 접두사로 붙여야 합니다. 버전 번호에 대한 자세한 내용은 [모듈 버전 번호 지정](/doc/modules/version-numbers)을 참조하십시오.

예를 들어, 아래의 `example.com/mymodules/module1` 모듈의 경우, 버전 v1.2.3에 대해 다음과 같이 작성합니다:

*   모듈 경로: `example.com/mymodules/module1`
*   버전 태그: `module1/v1.2.3`
*   사용자가 임포트한 패키지 경로: `example.com/mymodules/module1/package1`
*   사용자의 require 지시문에 지정된 모듈 경로 및 버전: `example.com/mymodules/module1 v1.2.3`

<img src="images/multiple-modules.png"
     alt="단일 리포지토리 내의 두 모듈을 보여주는 다이어그램"
     style="width: 480px;" />
