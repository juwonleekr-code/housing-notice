# 입주자모집공고 분석 DB

PF 대주 심사 · 시행 P&L 관점의 전국 분양현장 정적 대시보드 (GitHub Pages).

## 구조
```
index.html              전국 인덱스 (시도별 집계 + 필터/정렬 카드)
site.html?id={id}       개별 현장 대시보드 (6개 모듈)
data/index.json         전현장 요약 (인덱스 화면용)
data/sites/{id}.json    현장별 상세 (대시보드용)
```
화면 코드(html)는 고정. **새 현장은 JSON만 추가**하면 됩니다.

## 새 현장 추가법
1. `data/sites/{새id}.json` 추가 (기존 kimhae-sinmun-central.json 복사 후 값 교체)
2. `data/index.json`의 `sites` 배열에 요약 1건 추가
3. `git push` → GitHub Pages 자동 반영

## 대시보드 6개 모듈
1. 입지·건축개요
2. 단지개요·분양가 (총세대수 · 타입별 비중 · 면적가중 평균 평당가)
3. 시행사 P&L (발코니 확장 · 중도금 무이자/유이자)
4. 유상옵션 (사실상필수 / 필수+준필수 / 풀옵션 3단계)
5. 판촉·계약금 (A/B/C/D 등급 · 허수계약 점검)
6. 사업주체 (시공·신탁·시행 · 분양보증)

## 핵심 산정식
- 평당가 = 전 세대 분양가 합산 ÷ 총 공급평수 (면적가중)
- 평형 환산 = 공급면적(㎡) ÷ 3.3058
- 계약금 등급: 10%=A · 5%+5%=B · 정액제=C · 자납+신용대출=D

## 배포 (GitHub Pages)
레포 Settings → Pages → Branch: main / root → Save.
로컬 확인은 `python3 -m http.server` 후 localhost 접속 (파일 직접 열기는 CORS로 차단됨).
