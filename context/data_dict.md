# [데이터 사전] 260929_반도체사관학교_159개_훈련과정_원천데이터_정의서

본 문서는 `context/` 폴더에 저장되는 반도체사관학교 159개 훈련과정 원천 데이터(Read-Only)의 구조, 컬럼 및 보관 규칙을 정의한 데이터 딕셔너리입니다.

---

## 1. 데이터 소스 및 개요
- **원천 URL**: `https://sshmyb.tistory.com/category/반도체사관학교 훈련과정`
- **수집 대상**: 159개 훈련과정 포스트 전체 본문, 이미지, 예상 면접 질문, 메타데이터
- **수집 일시**: 2026-09-29
- **저장 위치**:
  - `context/post_catalog.json`: 159개 글 메타데이터 목록 (ID, URL, 제목, 카테고리)
  - `context/posts/<id>.json`: 포스트별 원문 텍스트, HTML 구조, 도해 이미지 URL 및 로컬 경로
  - `context/images/<id>_<index>.<ext>`: 포스트별 모든 고화질 도해 이미지 로컬 저장소

---

## 2. 컬럼 및 필드 정의서

- `id`
  - 설명: 티스토리 포스트 고유 번호 (예: 393, 351, 350 등)
  - 데이터 타입: String
  - 필수 여부: 필수 고유키 (PK)

- `url`
  - 설명: 티스토리 원본 포스트 URL
  - 데이터 타입: String
  - 형식: `https://sshmyb.tistory.com/<id>`

- `title`
  - 설명: 원본 포스트 제목
  - 데이터 타입: String
  - 용도: 학습 주제 및 검색 키워드

- `main_category`
  - 설명: 재분류된 상위 카테고리 (8대공정 / 반도체소자 / 최신기술 및 기업 / 평가분석 및 물리)
  - 데이터 타입: String

- `sub_category`
  - 설명: 세부 공정/소자 명칭 (포토, 식각, 박막증착, 확산열처리, CMP세정, 이온주입, 금속배선, MOSFET, FinFET, GAA, DRAM, NAND, SiC/GaN, HBM, 파운드리 등)
  - 데이터 타입: String

- `core_c`
  - 설명: CORE 프레임워크 - Concept (개념 정의, 두괄식 1~2문장)
  - 데이터 타입: String

- `core_o`
  - 설명: CORE 프레임워크 - Origin/Background (도입 배경 및 기존 기술 한계)
  - 데이터 타입: String

- `core_r`
  - 설명: CORE 프레임워크 - Principle/Mechanism (작동 원리, 물리/화학적 메커니즘, 장비 파라미터)
  - 데이터 타입: String

- `core_e`
  - 설명: CORE 프레임워크 - Effect/Challenge (공정 효과, 수율 개선, 한계 및 극복 방안)
  - 데이터 타입: String

- `interview_questions`
  - 설명: 원문에 포함된 면접관 예상 질문 및 꼬리질문 목록
  - 데이터 타입: Array of Objects (`[{ question, answer_points, defense_script }]`)

- `verbatim_text`
  - 설명: 토씨 하나 빠짐없이 보존된 원문 전체 줄글 텍스트
  - 데이터 타입: String

- `images`
  - 설명: 포스트에 포함된 모든 도해/다이어그램/공정 이미지 메타데이터
  - 데이터 타입: Array of Objects (`[{ original_url, local_path, alt_text, caption }]`)

---

## 3. 원천 데이터 무결성 및 보관 원칙
1. 원본 본문 텍스트는 임의 축약이나 왜곡 없이 원본 그대로 `context/posts/<id>.json`에 보존합니다.
2. 모든 도해 이미지는 원격 링크 소실에 대비하여 반드시 `context/images/`에 로컬 다운로드하여 보관합니다.
3. 데이터 파이프라인 재실행 시 `context/` 데이터는 Read-Only로 취급하여 원본을 보호합니다.
