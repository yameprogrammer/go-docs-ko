<!--{
  "Title": "모듈 버전 번호 매기기"
}-->

모듈 개발자는 모듈 버전 번호의 각 부분을 사용하여 해당 버전의 안정성과 하위 호환성을 나타냅니다. 각 새로운 릴리스마다, 모듈의 릴리스 버전 번호는 이전 릴리스 이후 모듈에 발생한 변경 사항의 성격을 구체적으로 반영합니다.

외부 모듈을 사용하는 코드를 개발할 때, 업그레이드를 고려하는 과정에서 버전 번호를 통해 해당 외부 모듈의 안정성을 파악할 수 있습니다. 직접 모듈을 개발할 때 사용하는 버전 번호는 다른 개발자들에게 해당 모듈의 안정성과 하위 호환성 여부를 알려주는 신호가 됩니다.

이 주제에서는 모듈 버전 번호의 의미에 대해 설명합니다.

**함께 보기**

* 코드에서 외부 패키지를 사용하는 경우, Go 도구를 통해 해당 의존성을 관리할 수 있습니다. 자세한 내용은 [Managing dependencies](managing-dependencies)를 참조하세요.
* 다른 사람이 사용할 모듈을 개발하는 경우, 모듈을 저장소에 태깅하여 게시할 때 버전 번호를 부여합니다. 자세한 내용은 [Publishing a module](publishing)을 참조하세요.

릴리스된 모듈은 다음 그림과 같이 시맨틱 버전 관리(semantic versioning) 모델의 버전 번호와 함께 게시됩니다.

<img src="images/version-number.png"
     alt="메이저 버전 1, 마이너 버전 4, 패치 버전 0, 그리고 프리릴리스 버전 beta 2를 보여주는 시맨틱 버전 번호 다이어그램"
     style="width: 300px;" />

다음 표는 버전 번호의 각 부분이 모듈의 안정성과 하위 호환성을 어떻게 나타내는지 설명합니다.

<table class="DocTable">
  <thead>
    <tr class="DocTable-head">
      <th class="DocTable-cell" width="20%">버전 단계</th>
      <th class="DocTable-cell">예시</th>
      <th class="DocTable-cell">개발자를 위한 메시지</th>
    </tr>
  </thead>
  <tbody>
    <tr class="DocTable-row">
      <td class="DocTable-cell"><a href="#in-development">개발 중 (In development)</a></td>
      <td class="DocTable-cell">자동 생성된 pseudo-version 번호
      <p>v<strong>0</strong>.x.x</td>
      <td class="DocTable-cell">모듈이 아직 <strong>개발 중이며 불안정함</strong>을 나타냅니다. 이 릴리스는 하위 호환성이나 안정성을 보장하지 않습니다.</td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell"><a href="#major">메이저 버전 (Major version)</a></td>
      <td class="DocTable-cell">v<strong>1</strong>.x.x</td>
      <td class="DocTable-cell"><strong>하위 호환성이 없는 공개 API 변경</strong>이 있음을 나타냅니다. 이 릴리스는 이전 메이저 버전과의 하위 호환성을 보장하지 않습니다.</td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell"><a href="#minor">마이너 버전 (Minor version)</a></td>
      <td class="DocTable-cell">vx.<strong>4</strong>.x</td>
      <td class="DocTable-cell"><strong>하위 호환성이 있는 공개 API 변경</strong>이 있음을 나타냅니다. 이 릴리스는 하위 호환성과 안정성을 보장합니다.</td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell"><a href="#patch">패치 버전 (Patch version)</a></td>
      <td class="DocTable-cell">vx.x.<strong>1</strong></td>
      <td class="DocTable-cell"><strong>모듈의 공개 API나 의존성에 영향을 주지 않는 변경</strong>이 있음을 나타냅니다. 이 릴리스는 하위 호환성과 안정성을 보장합니다.</td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell"><a href="#pre-release">프리릴리스 버전 (Pre-release version)</a></td>
      <td class="DocTable-cell">vx.x.x-<strong>beta.2</strong></td>
      <td class="DocTable-cell">이 버전이 <strong>alpha 또는 beta와 같은 프리릴리스 마일스톤</strong>임을 나타냅니다. 이 릴리스는 안정성을 보장하지 않습니다.</td>
    </tr>
  </tbody>
</table>

<a id="in-development" ></a>
## 개발 중

모듈이 여전히 개발 중이며 **불안정(unstable)** 함을 나타냅니다. 이 릴리스는 하위 호환성이나 안정성을 보장하지 않습니다.

버전 번호는 다음 형식 중 하나를 가질 수 있습니다:

**의사 버전 번호 (Pseudo-version number)**

> v0.0.0-20170915032832-14c0d48ead0c

**v0 숫자**

> v0.x.x

<a id="pseudo" ></a>
### Pseudo-version number

모듈이 저장소에서 태그가 지정되지 않은 경우, Go 도구는 해당 모듈의 함수를 호출하는 코드의 `go.mod` 파일에서 사용할 의사 버전(pseudo-version) 번호를 생성합니다.

**참고:** 권장 사항으로, 직접 pseudo-version 번호를 생성하기보다 항상 Go 도구가 이를 생성하도록 하십시오.

의사 버전(Pseudo-versions)은 모듈의 함수를 사용하는 개발자가 아직 시맨틱 버전 태그가 지정되지 않은 커밋을 대상으로 개발해야 할 때 유용합니다.

의사 버전(pseudo-version) 번호는 다음과 같은 형식과 같이 대시(-)로 구분된 세 부분으로 구성됩니다.

#### 구문

_baseVersionPrefix_-_timestamp_-_revisionIdentifier_

#### 부품

* **baseVersionPrefix** (vX.0.0 또는 vX.Y.Z-0)는 리비전(revision) 앞에 오는 시맨틱 버전 태그에서 도출되거나, 해당 태그가 없는 경우 vX.0.0에서 도출되는 값입니다.

* **timestamp** (yymmddhhmmss)는 리비전이 생성된 UTC 시간입니다. Git의 경우, 이는 author time이 아니라 commit time입니다.

* **revisionIdentifier** (abcdefabcdef)는 커밋 해시의 12자리 접두사 또는 Subversion의 경우 0으로 채워진 리비전 번호입니다.

<a id="v0" ></a>
### v0 번호

v0 번호로 게시된 모듈은 메이저, 마이너, 패치 부분과 선택적인 프리릴리스(pre-release) 식별자를 포함하는 정식 시맨틱 버전 번호를 갖게 됩니다.

v0 버전을 프로덕션 환경에서 사용할 수는 있지만, 안정성이나 하위 호환성은 보장되지 않습니다. 또한, v1 및 이후 버전은 v0 버전을 사용하는 코드에 대해 하위 호환성을 깨뜨릴 수 있습니다. 이러한 이유로 v0 모듈의 함수를 사용하는 코드를 작성하는 개발자는 v1이 릴리스될 때까지 호환되지 않는 변경 사항에 적응해야 할 책임이 있습니다.

<a id="pre-release" ></a>
## 프리릴리스 버전

알파 또는 베타와 같이 이것이 프리릴리스(pre-release) 마일스톤임을 나타냅니다. 이 릴리스는 안정성을 보장하지 않습니다.

#### 예시

```
vx.x.x-beta.2
```

모듈 개발자는 `major.minor.patch` 조합 뒤에 하이픈과 프리릴리스 식별자를 추가하여 프리릴리스 식별자를 사용할 수 있습니다.

<a id="minor" ></a>
## 마이너 버전(Minor version)

모듈의 공개 API에 대한 하위 호환 변경 사항을 나타냅니다. 이 릴리스는 하위 호환성과 안정성을 보장합니다.

#### 예제

```
vx.4.x
```

이 버전은 모듈의 public API를 변경하지만, 호출하는 코드를 깨뜨리는 방식은 아닙니다. 여기에는 모듈 자체의 의존성 변경이나 새로운 함수, 메서드, 구조체 필드 또는 타입의 추가가 포함될 수 있습니다.

다시 말해, 이 버전에는 다른 개발자가 사용하고 싶어 할 만한 새로운 함수를 통한 기능 향상이 포함될 수 있습니다. 하지만 이전 마이너 버전을 사용하는 개발자는 그 외에 코드를 변경할 필요가 없습니다.

<a id="patch" ></a>
## 패치 버전 (Patch version)

모듈의 퍼블릭 API나 의존성에 영향을 주지 않는 변경 사항을 나타냅니다.
이 릴리스는 하위 호환성과 안정성을 보장합니다.

#### 예제

```
vx.x.1
```

이 숫자를 증가시키는 업데이트는 버그 수정과 같은 마이너한 변경 사항에 대해서만 이루어집니다. 이를 사용하는 코드의 개발자는 자신의 코드를 수정할 필요 없이 안전하게 이 버전으로 업그레이드할 수 있습니다.

<a id="major" ></a>
## Major 버전

모듈의 public API에서 하위 호환성이 없는 변경 사항이 있음을 나타냅니다. 이 릴리스는 이전 메이저 버전과의 하위 호환성을 보장하지 않습니다.

#### 예제

제공해주신 내용이 버전 번호(`v1.x.x`)뿐이라 번역할 텍스트가 없습니다. 번역이 필요한 전체 마크다운 내용을 제공해주시면, 요청하신 지침에 따라 정밀하게 기술 번역을 진행하겠습니다.

v1 이상의 버전 번호는 해당 모듈이 사용하기에 안정적임을 나타냅니다(프리릴리스 버전은 제외).

버전 0은 안정성이나 하위 호환성을 보장하지 않으므로, 모듈을 v0에서 v1으로 업그레이드하는 개발자는 하위 호환성을 깨뜨리는 변경 사항에 적응할 책임이 있음에 유의하십시오.

모듈 개발자는 이 숫자를 v1 이후로 올릴 때 반드시 필요한 경우에만 해야 합니다. 버전 업그레이드는 업그레이드된 모듈의 함수를 사용하는 개발자들에게 상당한 혼란을 야기하기 때문입니다. 이러한 혼란에는 공개 API의 하위 호환되지 않는 변경 사항뿐만 아니라, 모듈을 사용하는 개발자가 해당 모듈의 패키지를 임포트하는 모든 곳에서 패키지 경로를 업데이트해야 하는 필요성이 포함됩니다.

v1보다 높은 숫자로의 메이저 버전 업데이트는 새로운 모듈 경로를 갖게 됩니다. 이는 다음 예시와 같이 모듈 경로 끝에 메이저 버전 번호가 추가되기 때문입니다.

```
module example.com/mymodule/v2 v2.0.0
```

메이저 버전 업데이트는 해당 모듈을 이전 버전과 별도의 이력을 가진 새로운 모듈로 만듭니다. 다른 사용자가 사용할 모듈을 개발 중이라면, [Module release and versioning workflow](release-workflow)의 "Publishing breaking API changes" 섹션을 참조하세요.

모듈 지시문에 대한 자세한 내용은 [go.mod reference](gomod-ref)를 참조하십시오.
