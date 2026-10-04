# 반도체 학습 프로젝트 (반도체_2) 운영 매뉴얼 & 지령 수행 SOP

본 문서는 사용자의 지시 사항, 핵심 학습 원칙, 그리고 새로운 개념 질의(지령)가 주어졌을 때 **어떻게 조사하고, 시각화하며, 시스템에 누적 및 배포하는지**에 대한 표준 작업 절차(SOP: Standard Operating Procedure)를 명시한 공식 가이드입니다.

---

## 1. 사용자의 핵심 지시 원칙 (반드시 준수할 절대 규칙)

사용자가 지속적인 피드백을 통해 확립한 핵심 지침은 다음과 같습니다:

1. **[⭐ 1, 2번 집중 설명 원칙] (절대 가드레일)**:
   - 복잡한 3번(소자 물리 수식 나열), 4번(팹 공정 단계 나열), 5번(전체 스크롤 뷰)은 **완전히 삭제**한다.
   - 모든 대화 설명과 HTML 대시보드는 오직 **2대 핵심 축**으로만 구성한다:
     - **`[1. 핵심 요약 & 1분 스피치]`**: 직관적 일상 비유 + 3줄 핵심 포인트 + SK하이닉스 양산기술 실전 1분 발화 스크립트.
     - **`[2. 정밀 도감 & 사진 해부]`**: 자체 설계한 고화질 풀컬러 SVG 도면 + 원천 강의 실물 사진 매칭 해부.

2. **[SK하이닉스 양산기술(PE) 정공법 일원화]**:
   - 타 산업(배터리, 디스플레이 등) 경험을 억지로 접목하지 않고, 철저한 **순수 반도체 공학 정공법(Orthodox Approach)**으로 설명한다.
   - 실무 키워드 필수 반영: Cpk, 산포, 종횡비(A/R), 표면장력 점착(Stiction), GIDL, Retention Time(tREF), 오믹 콘택트, 마스킹 오버레이 등.

3. **[초심자 맞춤형 직관 비유 선행]**:
   - 전공 용어를 남발하기 전, 누구나 1초 만에 이해할 수 있는 일상 비유를 먼저 제시한다.
   - (예: 커패시터 = 물통, 트랜지스터 = 수도꼭지 밸브, 워드라인 = 손잡이 선, 비트라인 = 수도관 고속도로, 실린더 = 속 빈 종이컵, 필러 = 속 찬 전봇대 쇠기둥).

4. **[영구 누적(Append)형 백과사전 체계]**:
   - 질문할 때마다 이전 내용을 덮어쓰지 않고, `topics.json`에 `topic_001`, `topic_002`... 형태로 영구 누적하여 단일 HTML 대시보드로 보존한다.

---

## 2. 신규 지령 접수 시 6단계 표준 조사 및 추가 프로세스 (AI Agent SOP)

사용자가 모르는 개념이나 면접 기출 문항을 질문했을 때 AI 에이전트는 다음 절차를 엄격히 수행합니다:

```
[사용자 지령 접수]
       │
       ▼
 [Step 1: 본질 파악] ── 사용자가 헷갈려하는 물리적/구조적 핵심 맹점 추출
       │
       ▼
 [Step 2: 원천 조사] ── 159개 강의 텍스트(JSON) 및 실물 도면(159_*.png) 교차 검증
       │
       ▼
 [Step 3: 도면 설계] ── 직관적 대비가 극대화된 풀컬러 반응형 SVG 도면 코딩
       │
       ▼
 [Step 4: 데이터 누적] ── context/data/topics.json에 topic_00X 신규 Append
       │
       ▼
 [Step 5: HTML 빌드] ── tool/.../build_encyclopedia.py 실행 (독립형 HTML 갱신)
       │
       ▼
 [Step 6: Git 배포] ── deploy.bat 실행 ➔ GitHub Pages (origin/main) 1초 자동 배포!
```

### 상세 단계별 행동 요령:
- **Step 1 (본질 파악 - 본기함구의 本)**:
  - 사용자가 던진 질문 문장에서 '왜 이런 의문이 생겼는가?'를 역추적합니다.
  - (예: "B/L이 드레인이고 CAP이 소스야?" ➔ MOSFET 대칭성에 따른 쓰기/읽기 캐리어 역전 현상과 도면 표기 관례의 충돌을 파악).
- **Step 2 (원천 조사 - Context 검증)**:
  - `C:\Work\반도체\context\posts\159.json` 및 `images/`에 있는 실물 다이어그램을 열람하여 교재 원문의 논리와 도면을 정확히 매칭합니다.
- **Step 3 (정밀 도감 제작 - SVG 코딩)**:
  - 텍스트만으로는 이해하기 힘든 구조적 차이를 나란히(Side-by-Side) 배치한 920x460 규격의 인라인 SVG 다이어그램을 생성합니다.
- **Step 4 (topics.json 누적)**:
  - `user_feedback`(칭찬/개선점), `pe_1min_script`(1분 스피치 대본), `core_analysis`, `physics_deep_dive`를 JSON 표준 스키마에 맞춰 추가합니다.
- **Step 5 (HTML 대시보드 빌드)**:
  - `build_encyclopedia.py`를 실행하여 1, 2번 서브 탭 뷰가 적용된 `result/.../index.html`을 생성합니다.
- **Step 6 (Git 연동 및 원클릭 배포)**:
  - 생성된 HTML을 `C:\Work\반도체\semiconductor2.html`로 동기화하고, `git commit` 및 `git push origin main`을 수행하여 온라인에 즉시 반영합니다.

---

## 3. 관리 파일 및 디렉토리 맵

| 위치 | 파일/디렉토리 | 역할 및 보존 내용 |
| :--- | :--- | :--- |
| **저장소 루트** | `index.html` | [배포] 반도체_2 누적형 소자·도감 백과사전 (단일 메인 대시보드) |
| **저장소 루트** | `archive_159.html` | [배포] 원천 159개 강의 전문 뷰어 아카이브 |
| **저장소 루트** | `rules.md` | AGY 워크스페이스 전역 개발 가드레일 & 반도체_2 특별 지침 |
| **저장소 루트** | `OPERATING_MANUAL.md` | **(본 파일) 사용자 지시 이력 및 조사/배포 SOP 매뉴얼** |
| `반도체_2/context/` | `data/topics.json` | 사용자의 모든 질문과 도감 데이터가 영구 보존되는 원천 DB |
| `반도체_2/tool/` | `build_encyclopedia.py` | 1, 2번 탭 전용 독립형 대시보드 생성 엔진 |
| `반도체_2/tool/` | `deploy.bat` | 원클릭 빌드 ➔ 동기화 ➔ Git Push 자동 배포 스크립트 |

---

## 4. 누적 토픽 히스토리 (현재 14개 토픽 완료)
1. **Topic #001**: BCAT(Buried Channel Array Transistor) 개념 및 100점 피드백
2. **Topic #002**: BCAT 3D 공간격리(Vertical Decoupling) 및 배선 쇼트 방지 메커니즘
3. **Topic #003**: 워드라인·비트라인·커패시터의 본질과 DRAM 동작 원리 (물통 & 바둑판 좌표계)
4. **Topic #004**: DRAM 단자 정의(BL=드레인, CAP=소스)와 SNC 플러그 및 Source(n+) 접합 해부
5. **Topic #005**: DRAM 커패시터 혁신 (실린더형 vs 필러형 & 더블 서포터 및 High-k)
6. **Topic #006**: HBM4에서 비아 홀(TSV I/O)의 개수가 2048개인 이유 (속도 한계 극복 & TSMC 파운드리 베이스 다이)
7. **Topic #007**: HBM4 2048개 비아 홀의 16단 적층 계산법 (16층 × 2048개 = 32,768개 비아 홀 및 채널 매핑)
8. **Topic #008**: MR-MUF (Mass Reflow Molded Underfill) 명칭 완벽 해부 (M·R·M·UF 단어 분해 및 방열 2.5배 비밀)
9. **Topic #009**: 2D DRAM vs 3D DRAM 차이 완벽 해부 (셀 눕힘 & 40단 수직 적층, EUV 탈피, 간섭 제로, 48GB 용량 돌파)
10. **Topic #010**: 게이트-채널 감쌈 면적과 SCE 억제 & Field Effect의 On-Current(Ion) 증가 원리 (Planar vs FinFET vs GAA)
11. **Topic #011**: 게이트가 채널을 많이 감쌀수록 '좋은 이유(원인)'와 '구체적 4대 이득(Ion/Ioff/S.S/면적)'
12. **Topic #012**: 평면의 바닥 누설(Sub-surface Leakage) 원인과 FinFET·GAA의 바닥 차단 3대 메커니즘 (Body Thinning & BDI)
13. **Topic #013**: Peri 회로(Peripheral Circuit, 주변 회로)의 본질과 4대 기능 & PUC(Peri Under Cell) 공간 혁신
14. **Topic #014**: Peri 회로 vs Base Die 비교 해부: 단일 칩 내부 회로(Circuit) vs 3D HBM 최하단 로직 칩(Die)

### [기능 개선] 원천강의 ↔ 메인 대시보드 상호 이동 시 마지막 페이지 & 스크롤 완벽 기억
- **메인 대시보드 (`index.html`)**: 마지막 조회 토픽(`Topic #009` 등), 서브탭 및 **본문 스크롤 위치**까지 `localStorage` 및 URL Hash(`#topic_009`)에 실시간 동기화. 상단 "159 원천 강의" 버튼 클릭 시 직전 포스트 해시(`#post-xxx`)를 달고 이동.
- **원천 강의 (`archive_159.html`)**: 마지막 조회 훈련과정 번호(`#post-351` 등), 대/소분류 카테고리 필터, **본문 스크롤 위치(ScrollTop)**를 실시간 자동 보존 및 복원. 상단 "메인 대시보드" 버튼 클릭 시 직전 토픽 해시(`#topic_xxx`)를 달고 이동.
- **캐시 방지 헤더(Cache-Control)** 완벽 주입으로 항상 최신 스크립트 실행 보장.

### [2026-10-04] Topic #015: Shallow Junction Depth Profile (접합 깊이 Xj, SIMS 농도 프로파일 & USJ 공정 물리)
- **추가 토픽**: `topic_015` (총 15개 토픽 누적)
- **카테고리**: 소자 물리 & 초미세 접합 (Device Physics & Junction)
- **내용**: 
  - Junction Depth (Xj)의 물리적 정의 (N(x) = Nsub 교차점)
  - 게이트 길이(Lg) 축소 시 Xj 스케일링이 필수적인 이유: 드레인 전계의 채널 하부 침투(DIBL) 및 펀치스루 원천 차단
  - 이상적인 직사각형(Box-like) 프로파일(표면 Rc 극소화 + 초가파른 접합 경사 Abruptness)과 현실의 TED(열확산) 꼬리 딜레마
  - 첨단 USJ(Ultra-Shallow Junction) 3대 공정 솔루션: PAI(비정질화) + Sub-keV 초저에너지 주입 + 밀리초 레이저 열처리(LSA/FLA)
- **신규 SVG 도해**: `generate_svg_diagram_16()` 추가
  - [좌측] 소자 단면 비교: 깊은 접합(DIBL 전계 침투/바닥 누설) vs Shallow Extension(전계 침투 차단/게이트 통제권 완벽 보존)
  - [우측] 깊이별 SIMS 도핑 농도 프로파일 곡선: 이상적 Box-like vs 첨단 USJ(레이저 열처리) vs 구형 RTA(TED 확산 꼬리) 1:1 비교
- **배포 동기화**: `build_encyclopedia.py` -> `prepare_deploy_files.py` -> `index.html` & `semiconductor2.html`
