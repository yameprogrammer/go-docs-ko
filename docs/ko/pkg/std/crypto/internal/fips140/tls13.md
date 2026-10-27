# package crypto/internal/fips140/tls13

- 원문: <https://pkg.go.dev/crypto/internal/fips140/tls13>
- 분류: Go 표준 라이브러리

## 한국어 요약

package tls13은 RFC 8446, Section 7.1에 정의되고 FIPS 140-3 IG 2.4.B Resolution 7에서 허용하는 TLS 1.3 키 스케줄(Key Schedule)을 구현합니다.

## 원문 요약

Package tls13 implements the TLS 1.3 Key Schedule as specified in RFC 8446, Section 7.1 and allowed by FIPS 140-3 IG 2.4.B Resolution 7.

## API 상세 (go doc -all)

~~~text
package tls13 // import "crypto/internal/fips140/tls13"

Package tls13 implements the TLS 1.3 Key Schedule as specified in RFC 8446,
Section 7.1 and allowed by FIPS 140-3 IG 2.4.B Resolution 7.

FUNCTIONS

func ExpandLabel[H hash.Hash](hash func() H, secret []byte, label string, context []byte, length int) []byte
    ExpandLabel implements HKDF-Expand-Label from RFC 8446, Section 7.1.

func TestingOnlyExporterSecret(s *ExporterMasterSecret) []byte

TYPES

type EarlySecret struct {
	// Has unexported fields.
}

func NewEarlySecret[H hash.Hash](h func() H, psk []byte) *EarlySecret

func (s *EarlySecret) ClientEarlyTrafficSecret(transcript hash.Hash) []byte
    ClientEarlyTrafficSecret derives the client_early_traffic_secret from the
    early secret and the transcript up to the ClientHello.

func (s *EarlySecret) EarlyExporterMasterSecret(transcript hash.Hash) *ExporterMasterSecret
    EarlyExporterMasterSecret derives the exporter_master_secret from the early
    secret and the transcript up to the ClientHello.

func (s *EarlySecret) HandshakeSecret(sharedSecret []byte) *HandshakeSecret

func (s *EarlySecret) ResumptionBinderKey() []byte

type ExporterMasterSecret struct {
	// Has unexported fields.
}

func (s *ExporterMasterSecret) Exporter(label string, context []byte, length int) []byte

type HandshakeSecret struct {
	// Has unexported fields.
}

func (s *HandshakeSecret) ClientHandshakeTrafficSecret(transcript hash.Hash) []byte
    ClientHandshakeTrafficSecret derives the client_handshake_traffic_secret
    from the handshake secret and the transcript up to the ServerHello.

func (s *HandshakeSecret) MasterSecret() *MasterSecret

func (s *HandshakeSecret) ServerHandshakeTrafficSecret(transcript hash.Hash) []byte
    ServerHandshakeTrafficSecret derives the server_handshake_traffic_secret
    from the handshake secret and the transcript up to the ServerHello.

type MasterSecret struct {
	// Has unexported fields.
}

func (s *MasterSecret) ClientApplicationTrafficSecret(transcript hash.Hash) []byte
    ClientApplicationTrafficSecret derives the
    client_application_traffic_secret_0 from the master secret and the
    transcript up to the server Finished.

func (s *MasterSecret) ExporterMasterSecret(transcript hash.Hash) *ExporterMasterSecret
    ExporterMasterSecret derives the exporter_master_secret from the master
    secret and the transcript up to the server Finished.

func (s *MasterSecret) ResumptionMasterSecret(transcript hash.Hash) []byte
    ResumptionMasterSecret derives the resumption_master_secret from the master
    secret and the transcript up to the client Finished.

func (s *MasterSecret) ServerApplicationTrafficSecret(transcript hash.Hash) []byte
    ServerApplicationTrafficSecret derives the
    server_application_traffic_secret_0 from the master secret and the
    transcript up to the server Finished.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
