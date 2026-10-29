## Go trace viewer를 위한 리소스

Go 실행 트레이스 UI (`go tool trace`)는 [안내서](https://chromium.googlesource.com/catapult/+/refs/heads/master/tracing/docs/embedding-trace-viewer.md)에 따라 Chrome의 트레이스 뷰어(Catapult)를 임베드합니다. 이 디렉터리는 Chrome 트레이스 뷰어를 임베드하는 데 필요한 헬퍼 파일들을 포함하고 있습니다.

현재 리소스는 [`Catapult@9508452e18f130c98499cb4c4f1e1efaedee8962`](https://chromium.googlesource.com/catapult/+/9508452e18f130c98499cb4c4f1e1efaedee8962)에서 생성/복사되었습니다.

### `trace_viewer_full.html` 업데이트하기

이 파일은 catapult의 `vulcanize_trace_viewer` 명령어로 생성되었습니다.

```
$ git clone https://chromium.googlesource.com/catapult
$ cd catapult
$ ./tracing/bin/vulcanize_trace_viewer --config=full
$ cp tracing/bin/trace_viewer_full.html $GOROOT/src/cmd/trace/static/trace_viewer_full.html
```

`--config=lean` (더 작은 html 생성)을 사용해야 하지만, 현재 다음과 같은 이유로 작동하지 않습니다:
https://github.com/catapult-project/catapult/issues/2247

### `webcomponents.min.js` 업데이트하기

`webcomponents.min.js`는 트레이스 뷰어(trace viewer) 페이지가 `trace_viewer_full.html`을 임포트할 수 있도록 하는 데 필요합니다.
이 파일은 catapult 저장소에서 복사되었습니다.

```
$ cp third_party/polymer/components/webcomponentsjs/webcomponents.min.js $GOROOT/src/cmd/trace/static/webcomponents.min.js
```

## 라이선스

trace-viewer의 라이선스는 다음과 같습니다:

// Copyright (c) 2012 The Chromium Authors. All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
//    * Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
//    * Redistributions in binary form must reproduce the above
// copyright notice, this list of conditions and the following disclaimer
// in the documentation and/or other materials provided with the
// distribution.
//    * Neither the name of Google Inc. nor the names of its
// contributors may be used to endorse or promote products derived from
// this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

webcomponents.min.js의 라이선스는 다음과 같습니다:

제공해주신 텍스트는 소프트웨어 라이선스(BSD License) 전문이며, 일반적으로 라이선스 법률 문구는 번역 시 법적 효력의 문제가 발생할 수 있어 원문을 그대로 유지하는 것이 관례입니다. 하지만 요청하신 대로 기술 번역 가이드라인에 따라 한국어로 번역해 드립니다.

***

/**
 * @license
 * Copyright (c) 2014 The Polymer Project Authors. All rights reserved.
 * 이 코드는 http://polymer.github.io/LICENSE.txt 에 명시된 BSD 스타일 라이선스 하에서만 사용할 수 있습니다.
 * 전체 저자 목록은 http://polymer.github.io/AUTHORS.txt 에서 확인할 수 있습니다.
 * 전체 기여자 목록은 http://polymer.github.io/CONTRIBUTORS.txt 에서 확인할 수 있습니다.
 * polymer 프로젝트의 일부로 Google에 의해 배포되는 코드는
 * http://polymer.github.io/PATENTS.txt 에 명시된 추가 IP 권리 부여 대상이기도 합니다.
 */
// Copyright (c) 2014 The Polymer Authors. All rights reserved.
//
// 수정 여부와 관계없이 소스 및 바이너리 형식의 재배포 및 사용은
// 다음 조건이 충족되는 경우 허용됩니다:
//
//    * 소스 코드의 재배포 시 위의 저작권 고지, 본 조건 목록 및
// 다음 면책 조항을 유지해야 합니다.
//    * 바이너리 형식의 재배포 시 배포 시 제공되는 문서 및/또는
// 기타 자료에 위의 저작권 고지, 본 조건 목록 및 다음 면책 조항을
// 재현해야 합니다.
//    * 사전 서면 승인 없이는 Google Inc.의 이름이나 기여자의 이름을
// 본 소프트웨어에서 파생된 제품을 홍보하거나 보증하는 데 사용할 수 없습니다.
//
// 본 소프트웨어는 저작권 보유자와 기여자들에 의해 "있는 그대로" 제공되며,
// 상품성 및 특정 목적에 대한 적합성에 대한 묵시적 보증을 포함하여,
// 명시적 또는 묵시적인 모든 보증을 부인합니다. 저작권 보유자나
// 기여자는 어떠한 경우에도 본 소프트웨어의 사용으로 인해 발생한
// 직접적, 간접적, 부수적, 특별, 징벌적 또는 결과적 손해(대체 상품 또는
// 서비스의 조달, 사용 손실, 데이터 또는 이익 손실, 또는 영업 중단 등을
// 포함하되 이에 국한되지 않음)에 대해, 계약, 엄격 책임 또는 불법 행위
// (과실 포함 또는 기타) 등 책임 이론에 관계없이, 그러한 손해의 가능성을
// 통지받았더라도 책임을 지지 않습니다.
