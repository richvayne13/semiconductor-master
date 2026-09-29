# [반도체 159개 훈련과정] CORE 면접 대비 및 공정/소자/기술 학습 대시보드 구축 완료 보고서

## 1. 프로젝트 개요 및 추진 배경
- 대상 원천: 딴딴's 반도체사관학교 훈련과정 (총 159개 포스트 전수)
- 작업 디렉터리: C:\Work\반도체
- 핵심 목표:
  1) 159개 전 포스트와 736개 기술 도해 다이어그램의 100% 무손실 오프라인 영구 보존
  2) CORE 프레임워크(C: 개념, O: 도입 배경, R: 작동 원리, E: 공정 효과 및 한계) 기반 면접 답변 구조화
  3) 반도체 8대 공정, 반도체 소자, 최신 기술 및 기업 동향의 정밀 분류
  4) 실전 면접 질문 326개 및 30초 스피치 타이머가 내장된 단독 실행형 인터랙티브 HTML 대시보드 구축
  5) Context-Tool-Result 표준 가드레일 준수 및 원클릭 재현 run.bat 파이프라인 완성

---

## 2. 데이터 수집 및 정제 결과 (Context)
- 수집 범위: 16개 카탈로그 페이지 전체 크롤링 (159개 포스트 식별)
- 텍스트 수집: 공개 포스트 154개 본문 텍스트 100% 무손실 수집 (약 5.4MB)
- 이미지 수집: 총 736개 고화질 기술 도해 다이어그램 로컬 다운로드 완료 (`context/images/`)
- 비공개/보호글 처리: 비밀번호가 설정된 5개 포스트(ID 109, 189, 190, 191, 194)는 잠금 메타데이터 및 원본 링크 제공으로 안전 처리
- 산출 파일:
  - context/post_catalog.json (159개 원천 메타데이터)
  - context/data_dict.md (데이터 사전)
  - context/processed_all_posts.json (CORE 구조화 통합 데이터셋, 5.39MB)

---

## 3. 분류 체계 및 포스트 매핑 현황

### [대분류 1] 반도체 8대 공정 (총 112개 포스트)
- 포토 공정 (Photo Lithography) : 28개
  - 노광 원리, 해상도(Resolution)와 초점심도(DoF), Rayleigh 공식
  - Photoresist (PR) 화학 메커니즘, 화학증폭형 감광액 (CAR)
  - EUV, High-NA, Mask 3D Effects, ArF-Immersion, DPT/QPT, SADP/SAQP
  - OPC, PSM, OAI, NIL, DSA 등 미세 패턴 기술
- 박막 & 증착 공정 (Thin Film / CVD / ALD) : 23개
  - CVD 분류 (APCVD, LPCVD, PECVD, HDPCVD, MOCVD)
  - Atomic Layer Deposition (ALD) 메커니즘, 표면 포화 반응
  - PVD, 스퍼터링 (DC/RF Sputter, 반응성 스퍼터링), 음극전압강하, Sheath 영역
  - High-k / Low-k 절연막 및 금속막 (Plug W, Si3N4, SiO2)
- 식각 공정 (Etch & Plasma) : 20개
  - 건식 식각(Dry Etch) 원리 및 RIE (Reactive Ion Etching)
  - 플라즈마 물리: 파센 법칙(Paschen's Law), Debye length, 플라즈마 전위, 자기바이어스
  - 차세대 식각 기술: Atomic Layer Etching (ALE), Pulsed Etch, Cryogenic Etch, Bosch 공정
  - 깊이 로딩 효과(Depth Loading Effect), 마이크로 로딩, 선택비 및 식각 프로파일
- 공정 제어 & 수율/불량 분석 (Yield & PCM) : 13개
  - 수율 모델링 및 수율 향상 공정 제어 기술
  - PCM (Process Control Monitor) 구조 및 전기적 파라미터 총정리
  - Process Corner Model (FF, SS, FS, SF, TT)을 통한 공정 마진 평가
  - In-line 모니터링, 상관성 분석, Shmoo Plot
- 금속배선 & 패키징 (Metallization & Packaging) : 11개
  - 오믹 접합(Ohmic) 및 쇼트키 접합(Schottky Contact), 에너지 밴드 다이어그램
  - Salicide (Self-aligned Silicide) 공정
  - 신뢰성 불량: 일렉트로마이그레이션(EM), 스트레스 마이그레이션(SM)
  - TSV (Through Silicon Via) 관통 전극 및 첨단 인터커넥트
- 이온주입 공정 (Ion Implantation) : 9개
  - Ion Implant 설비 구조 및 Diffusion 공정과의 정량적 비교
  - Stopping Mechanism (Nuclear Stopping vs. Electronic Stopping)
  - Doping Profile, 접합 깊이(Junction Depth), 채널링(Channeling) 및 Shadowing 방지
  - 격자 결함, Damage 회복 열처리 (RTA, TED, OED, ORD)
- CMP & 세정 공정 (C&C / Planarization) : 7개
  - Chemical Mechanical Polishing (CMP) 메커니즘, Preston 식, 패드 컨디셔닝, 슬러리 화학
  - 세정 공정 개요 및 습식 세정 (RCA, SC-1, SC-2, Piranha, DHF)
- 확산 & 열처리 공정 (Oxidation / Thermal) : 1개
  - Diffusion 공정 기출 및 실전 면접 정리

### [대분류 2] 반도체 소자 (총 40개 포스트)
- MOSFET 기초 & 소자 물리 : 17개
  - MOS 커패시터 동작 모드 (축적, 공핍, 반전), MOSFET 동작 원리
  - 문턱 전압 (Threshold Voltage) 조절 메커니즘 및 Body Effect
  - 출력 특성 곡선 (선형 영역, 포화 영역, 핀치오프)
  - HKMG (High-k Metal Gate) 도입 배경 및 EOT 저감
  - 누설 전류(Leakage Current) 분류 및 제어 방안
  - 차세대 연구 소자: SOI, FD-SOI, TFET, I-MOS, NC-FET
- 단채널 효과 (SCE) & 신뢰성 : 8개
  - DIBL (Drain Induced Barrier Lowering), Subthreshold Current
  - Punch-Through, Velocity Saturation, Hot Carrier Injection (HCI)
  - GIDL (Gate Induced Drain Leakage)
  - Subthreshold Swing (SS) 물리적 한계 (60mV/dec) 극복 전략
  - 소자 신뢰성: NBTI, PBTI 열화 메커니즘
- 차세대 전력 & 특수 소자 (SiC/GaN/PMIC) : 6개
  - 와이드 밴드갭(WBG) 반도체: SiC (탄화규소), GaN (질화갈륨) 특성 및 물성 비교
  - Power Module IC (PMIC), 파워 디바이스 Isolation 기술
  - CIS (CMOS Image Sensor) vs CCD 구조 비교, DDI, T-CON
- NAND Flash 메모리 : 4개
  - 플로팅 게이트(FG) vs 차지 트랩(CTF) 구조
  - 낸드 셀 레벨: SLC, MLC, TLC, QLC 동작 및 신뢰성 윈도우
  - 3D NAND 및 V-NAND 적층 기술
- DRAM 메모리 : 3개
  - DRAM 동작 원리 (1T-1C), 커패시터 전하 저장 및 리프레시(Refresh)
  - DDR vs LPDDR 아키텍처 및 세대별 대역폭 비교
  - RCAT, DCAT 및 차세대 3D DRAM 소자 구조
- 3D 트랜지스터 (FinFET/GAA) : 2개
  - FinFET 3면 게이트 구조 및 누설전류 억제 효과
  - Gate-All-Around (GAAFET) 및 MBCFET (나노시트) 3nm/2nm 적용 원리

### [대분류 3] 최신 기술 및 기업 동향 (총 7개 포스트)
- 파운드리 & 선단공정 : 4개
  - TSMC 2nm N2 공정 핵심 경쟁력 및 GAA 도입
  - 선단 파운드리 2025년 2nm 양산 로드맵
  - 첨단 3nm 경쟁력 분석: Samsung vs. TSMC
  - 선단 공정 로드맵 및 차세대 노드 기술
- HBM & 차세대 메모리 : 3개
  - HBM (High Bandwidth Memory) 세대별 로드맵 (HBM3e -> HBM4 -> HBM4e)
  - HBM 적층 단수 증가에 따른 휨(Warpage) 및 방열 문제
  - SK하이닉스 MR-MUF 기술 vs 삼성전자 TC-NCF 기술 비교
  - HBM4 첨단 파운드리 베이스 다이(Base Die) 협력 생태계
  - Processing-In-Memory (PIM) 차세대 지능형 메모리

---

## 4. 대시보드 주요 기능 및 사용법 (방안 C)

1) CORE 30초/1분 답변 치트키 카드:
   - 각 포스트 선택 시 면접장에서 바로 발화할 수 있는 핵심 요약이 4개 카드로 제시됩니다.
   - C (Concept): 용어 및 기술의 핵심 개념 1~2줄 정의
   - O (Origin/Background): 왜 기존 기술의 한계로 인해 도입되었는지 배경
   - R (Principle/Mechanism): 내부 물리/화학적 동작 원리
   - E (Effect/Application): 공정 수율 및 소자 성능 개선 효과, 잔여 한계점
2) 실전 면접 예상 질문 & 꼬리질문 뷰어:
   - 총 326개의 엄선된 실제 면접 기출/예상 질문이 포스트별로 카드 형태로 직관적 렌더링됩니다.
3) 원문 전문 및 736개 고화질 다이어그램 뷰어:
   - 원문의 토씨 하나 빠짐없는 전체 텍스트와 본문 삽입 다이어그램이 100% 로컬 오프라인 이미지로 렌더링됩니다.
   - 로컬 이미지는 원본 CDN fallback이 적용되어 오프라인과 온라인 배포 환경 모두에서 완벽히 작동합니다.
4) 30초 스피치 타이머:
   - 헤더에 내장된 30초 카운트다운 타이머로 실전 압박 면접 구술 연습이 가능합니다.
5) 통합 검색 및 카테고리 필터링:
   - 4대 대분류 탭 전환, 16개 세부 공정/소자 칩 필터, 실시간 키워드 통합 검색을 지원합니다.
6) 다크 모드 / 라이트 모드 전환:
   - 장시간 학습 시 눈의 피로를 최소화하는 고대비 다크 테마를 기본 지원합니다.

---

## 5. 산출물 및 재현 파이프라인 안내 (Tool & Result)

- 배포 대시보드 HTML:
  - C:\Work\반도체\result\index.html (루트 배포용, 5.34MB)
  - C:\Work\반도체\result\260929_v1.0\index.html (버전 아카이브용, 5.34MB)
- 오프라인 도해 이미지:
  - C:\Work\반도체\result\images\ (736개 고화질 다이어그램)
  - C:\Work\반도체\result\260929_v1.0\images\ (736개 고화질 다이어그램)
- 원클릭 재현 스크립트:
  - C:\Work\반도체\tool\260929_v1.0\run.bat
  - 더블 클릭 한 번으로 신규 글 크롤링 확인, CORE 구조화, 대시보드 빌드, 브라우저 자동 실행까지 전 과정이 100% 무인 자동 수행됩니다.
