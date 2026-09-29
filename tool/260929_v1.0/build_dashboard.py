import json, sys, os, html, shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

data_path = Path(r"C:\Work\반도체\context\processed_all_posts.json")
result_dir = Path(r"C:\Work\반도체\result\260929_v1.0")
result_root = Path(r"C:\Work\반도체\result")
images_src = Path(r"C:\Work\반도체\context\images")

result_dir.mkdir(parents=True, exist_ok=True)
images_dst = result_dir / "images"
images_dst_root = result_root / "images"

print("Copying images to result directories for local offline image viewing...")
if not images_dst.exists():
    shutil.copytree(images_src, images_dst)
if not images_dst_root.exists():
    shutil.copytree(images_src, images_dst_root)

print(f"Loaded processed data from {data_path}...")
with open(data_path, 'r', encoding='utf-8') as f:
    posts = json.load(f)

print(f"Total posts: {len(posts)}")

# Prepare posts data for embedding:
# To keep HTML performance blazing fast while preserving 100% verbatim text and images,
# we embed JSON into a <script> tag.
json_str = json.dumps(posts, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>반도체사관학교 159개 훈련과정 - CORE 면접대비 & 공정/소자 학습 대시보드</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-main: #f8fafc;
      --bg-sidebar: #ffffff;
      --bg-card: #ffffff;
      --border: #e2e8f0;
      --border-focus: #3b82f6;
      --text-main: #0f172a;
      --text-sub: #64748b;
      --text-muted: #94a3b8;
      --primary: #2563eb;
      --primary-light: #eff6ff;
      --primary-dark: #1d4ed8;
      
      --core-c-bg: #eff6ff;
      --core-c-border: #3b82f6;
      --core-c-text: #1d4ed8;
      
      --core-o-bg: #fefce8;
      --core-o-border: #eab308;
      --core-o-text: #a16207;
      
      --core-r-bg: #f0fdf4;
      --core-r-border: #22c55e;
      --core-r-text: #15803d;
      
      --core-e-bg: #faf5ff;
      --core-e-border: #a855f7;
      --core-e-text: #7e22ce;
      
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
      --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.07);
      --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.08);
      --radius: 10px;
    }

    body.dark-mode {
      --bg-main: #0b0f19;
      --bg-sidebar: #111827;
      --bg-card: #1e293b;
      --border: #334155;
      --border-focus: #60a5fa;
      --text-main: #f1f5f9;
      --text-sub: #94a3b8;
      --text-muted: #64748b;
      --primary: #3b82f6;
      --primary-light: #1e3a8a;
      --primary-dark: #60a5fa;
      
      --core-c-bg: rgba(37, 99, 235, 0.15);
      --core-c-border: #3b82f6;
      --core-c-text: #93c5fd;
      
      --core-o-bg: rgba(234, 179, 8, 0.15);
      --core-o-border: #eab308;
      --core-o-text: #fde047;
      
      --core-r-bg: rgba(34, 197, 94, 0.15);
      --core-r-border: #22c55e;
      --core-r-text: #86efac;
      
      --core-e-bg: rgba(168, 85, 247, 0.15);
      --core-e-border: #a855f7;
      --core-e-text: #d8b4fe;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
      background: var(--bg-main);
      color: var(--text-main);
      height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    /* Top Global Header */
    .top-bar {
      height: 58px;
      background: var(--bg-sidebar);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
      z-index: 20;
      flex-shrink: 0;
    }
    .brand-wrap {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-badge {
      background: linear-gradient(135deg, #2563eb, #7c3aed);
      color: #fff;
      font-size: 11px;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 6px;
      letter-spacing: 0.5px;
    }
    .brand-title {
      font-size: 16px;
      font-weight: 800;
      color: var(--text-main);
      letter-spacing: -0.3px;
    }
    .top-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .search-box {
      position: relative;
      width: 320px;
    }
    .search-box input {
      width: 100%;
      height: 36px;
      padding: 0 12px 0 34px;
      background: var(--bg-main);
      border: 1px solid var(--border);
      border-radius: 8px;
      font-size: 13px;
      color: var(--text-main);
      outline: none;
      transition: all 0.2s;
    }
    .search-box input:focus {
      border-color: var(--border-focus);
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
    }
    .search-icon {
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 14px;
    }

    .btn-top {
      height: 36px;
      padding: 0 12px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--bg-card);
      color: var(--text-main);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
    }
    .btn-top:hover {
      background: var(--border);
    }

    /* Main App Layout */
    .app-body {
      flex: 1;
      display: flex;
      overflow: hidden;
    }

    /* Sidebar */
    .sidebar {
      width: 380px;
      background: var(--bg-sidebar);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
    }

    .category-tabs {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 4px;
      padding: 10px;
      border-bottom: 1px solid var(--border);
      background: var(--bg-main);
    }
    .cat-tab-btn {
      padding: 8px 6px;
      border-radius: 6px;
      border: 1px solid transparent;
      background: var(--bg-sidebar);
      color: var(--text-sub);
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      text-align: center;
      transition: all 0.15s;
    }
    .cat-tab-btn.active {
      background: var(--primary);
      color: #ffffff;
      border-color: var(--primary);
      box-shadow: var(--shadow-sm);
    }

    .subcat-filter-bar {
      padding: 8px 12px;
      display: flex;
      gap: 6px;
      overflow-x: auto;
      border-bottom: 1px solid var(--border);
      white-space: nowrap;
      background: var(--bg-sidebar);
    }
    .subcat-chip {
      padding: 4px 10px;
      border-radius: 14px;
      background: var(--bg-main);
      border: 1px solid var(--border);
      font-size: 11px;
      font-weight: 600;
      color: var(--text-sub);
      cursor: pointer;
      transition: all 0.15s;
    }
    .subcat-chip.active {
      background: var(--primary-light);
      border-color: var(--primary);
      color: var(--primary);
    }

    .post-list-wrap {
      flex: 1;
      overflow-y: auto;
      padding: 8px;
    }
    .post-item {
      padding: 12px 14px;
      border-radius: 8px;
      margin-bottom: 6px;
      cursor: pointer;
      border: 1px solid transparent;
      background: var(--bg-card);
      transition: all 0.15s;
      position: relative;
    }
    .post-item:hover {
      border-color: var(--border);
      background: var(--bg-main);
      transform: translateY(-1px);
    }
    .post-item.active {
      border-color: var(--primary);
      background: var(--primary-light);
    }
    .post-item-meta {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 4px;
    }
    .post-item-subcat {
      font-size: 11px;
      font-weight: 700;
      color: var(--primary);
    }
    .post-item-id {
      font-size: 11px;
      color: var(--text-muted);
      font-family: 'JetBrains Mono', monospace;
    }
    .post-item-title {
      font-size: 13px;
      font-weight: 700;
      line-height: 1.4;
      color: var(--text-main);
      margin-bottom: 6px;
    }
    .post-item-badges {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      color: var(--text-sub);
    }
    .badge-q-count {
      background: rgba(37, 99, 235, 0.1);
      color: var(--primary);
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 700;
    }
    .badge-img-count {
      background: rgba(16, 185, 129, 0.1);
      color: #059669;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 700;
    }
    .badge-lock {
      background: rgba(239, 68, 68, 0.1);
      color: #dc2626;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 700;
    }

    /* Content Area */
    .content-area {
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      background: var(--bg-main);
    }

    .content-header-sticky {
      position: sticky;
      top: 0;
      background: var(--bg-sidebar);
      border-bottom: 1px solid var(--border);
      padding: 16px 28px;
      z-index: 10;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: var(--shadow-sm);
    }
    .post-header-info {
      flex: 1;
    }
    .post-header-tag {
      font-size: 12px;
      font-weight: 800;
      color: var(--primary);
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .post-header-title {
      font-size: 20px;
      font-weight: 800;
      letter-spacing: -0.5px;
      line-height: 1.3;
      color: var(--text-main);
    }
    .post-header-controls {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .timer-badge {
      display: flex;
      align-items: center;
      gap: 6px;
      background: var(--bg-main);
      border: 1px solid var(--border);
      padding: 6px 12px;
      border-radius: 8px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 14px;
      font-weight: 700;
      color: var(--primary);
    }
    .btn-timer {
      background: var(--primary);
      color: #fff;
      border: none;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
    }

    .main-scroll-view {
      padding: 24px 28px 60px 28px;
      max-width: 1080px;
      margin: 0 auto;
      width: 100%;
    }

    /* CORE Grid */
    .section-label {
      font-size: 13px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--text-sub);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .core-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
      margin-bottom: 28px;
    }
    .core-card {
      border-radius: var(--radius);
      padding: 18px 20px;
      border: 1px solid;
      box-shadow: var(--shadow-sm);
    }
    .core-card.c {
      background: var(--core-c-bg);
      border-color: var(--core-c-border);
    }
    .core-card.o {
      background: var(--core-o-bg);
      border-color: var(--core-o-border);
    }
    .core-card.r {
      background: var(--core-r-bg);
      border-color: var(--core-r-border);
    }
    .core-card.e {
      background: var(--core-e-bg);
      border-color: var(--core-e-border);
    }

    .core-title {
      font-size: 13px;
      font-weight: 800;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .core-card.c .core-title { color: var(--core-c-text); }
    .core-card.o .core-title { color: var(--core-o-text); }
    .core-card.r .core-title { color: var(--core-r-text); }
    .core-card.e .core-title { color: var(--core-e-text); }

    .core-body {
      font-size: 14px;
      line-height: 1.6;
      color: var(--text-main);
      font-weight: 500;
    }

    /* Interview Q&A Section */
    .qa-section {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 20px;
      margin-bottom: 28px;
      box-shadow: var(--shadow-sm);
    }
    .qa-item {
      padding: 12px 14px;
      border-left: 3px solid var(--primary);
      background: var(--bg-main);
      border-radius: 0 8px 8px 0;
      margin-bottom: 10px;
    }
    .qa-header {
      font-size: 13px;
      font-weight: 800;
      color: var(--primary);
      margin-bottom: 4px;
    }
    .qa-question {
      font-size: 14px;
      font-weight: 700;
      color: var(--text-main);
    }

    /* Verbatim Section */
    .verbatim-section {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 24px;
      box-shadow: var(--shadow-sm);
    }
    .verbatim-content {
      font-size: 15px;
      line-height: 1.8;
      color: var(--text-main);
      word-break: break-word;
    }
    .verbatim-content p {
      margin-bottom: 16px;
    }
    .verbatim-image-box {
      margin: 24px 0;
      text-align: center;
      background: var(--bg-main);
      padding: 12px;
      border-radius: 8px;
      border: 1px solid var(--border);
    }
    .verbatim-image-box img {
      max-width: 100%;
      height: auto;
      border-radius: 6px;
      box-shadow: var(--shadow-sm);
    }
    .img-caption {
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 6px;
    }

    .protected-box {
      padding: 40px;
      text-align: center;
      background: var(--bg-main);
      border-radius: 8px;
      color: var(--text-sub);
      font-size: 15px;
      font-weight: 600;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
  </style>
</head>
<body>

  <!-- Top Navigation Header -->
  <header class="top-bar">
    <div class="brand-wrap">
      <span class="brand-badge">CORE 면접 마스터</span>
      <h1 class="brand-title">딴딴's 반도체사관학교 159 훈련과정</h1>
    </div>

    <div class="top-actions">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" id="globalSearchInput" placeholder="공정, 소자, 기술 키워드 통합 검색...">
      </div>
      <button class="btn-top" id="themeToggleBtn" onclick="toggleTheme()">🌓 테마 전환</button>
      <button class="btn-top" onclick="window.open('https://sshmyb.tistory.com/category/%EB%B0%98%EB%8F%84%EC%B2%B4%EC%82%AC%EA%B4%80%ED%95%99%EA%B5%90%20%ED%9B%88%EB%A0%A8%EA%B3%BC%EC%A0%95', '_blank')">🌐 원본 블로그</button>
    </div>
  </header>

  <!-- Main Body Layout -->
  <div class="app-body">
    
    <!-- Sidebar -->
    <aside class="sidebar">
      <!-- 4 Main Category Tabs -->
      <div class="category-tabs">
        <button class="cat-tab-btn active" onclick="setMainCategory('전체')">전체 보기 (159)</button>
        <button class="cat-tab-btn" onclick="setMainCategory('반도체 8대 공정')">반도체 8대 공정</button>
        <button class="cat-tab-btn" onclick="setMainCategory('반도체 소자')">반도체 소자</button>
        <button class="cat-tab-btn" onclick="setMainCategory('최신 기술 및 기업')">최신 기술 & 기업</button>
      </div>

      <!-- Subcategory Horizontal Filter -->
      <div class="subcat-filter-bar" id="subcatFilterBar">
        <span class="subcat-chip active" onclick="setSubCategory('전체')">전체 세부공정</span>
      </div>

      <!-- Post List -->
      <div class="post-list-wrap" id="postListContainer">
        <!-- Rendered by JavaScript -->
      </div>
    </aside>

    <!-- Main Content Reader -->
    <main class="content-area" id="contentArea">
      <!-- Sticky Post Header -->
      <div class="content-header-sticky">
        <div class="post-header-info">
          <div class="post-header-tag" id="viewPostTag">
            <span id="viewPostMainCat">🚀 반도체 8대 공정</span> • <span id="viewPostSubCat">포토 공정</span>
          </div>
          <h2 class="post-header-title" id="viewPostTitle">포스트 제목</h2>
        </div>
        <div class="post-header-controls">
          <div class="timer-badge">
            ⏱️ <span id="timerDisplay">00:00</span>
          </div>
          <button class="btn-timer" id="timerStartBtn" onclick="toggleTimer()">30초 답변 연습</button>
          <button class="btn-top" id="openOriginalBtn" onclick="openOriginalUrl()">🔗 원본 글 보기</button>
        </div>
      </div>

      <!-- Scrollable Viewer -->
      <div class="main-scroll-view">
        
        <!-- CORE Framework Section -->
        <div class="section-label">⚡ CORE 면접관 30초/1분 답변 치트키</div>
        <div class="core-grid">
          <div class="core-card c">
            <div class="core-title">📌 C (Concept - 개념 정의)</div>
            <div class="core-body" id="viewCoreC">개념 정의 내용</div>
          </div>
          <div class="core-card o">
            <div class="core-title">💡 O (Origin/Background - 도입 배경)</div>
            <div class="core-body" id="viewCoreO">도입 배경 내용</div>
          </div>
          <div class="core-card r">
            <div class="core-title">⚙️ R (Principle/Mechanism - 작동 원리)</div>
            <div class="core-body" id="viewCoreR">작동 원리 내용</div>
          </div>
          <div class="core-card e">
            <div class="core-title">🎯 E (Effect/Application - 공정 효과 및 한계)</div>
            <div class="core-body" id="viewCoreE">공정 효과 및 한계 내용</div>
          </div>
        </div>

        <!-- Interview Q&A Section -->
        <div class="qa-section" id="viewQaSection">
          <div class="section-label">🎙️ 실전 면접 예상 질문 & 꼬리질문 포인트</div>
          <div id="viewQaList">
            <!-- Questions rendered here -->
          </div>
        </div>

        <!-- Full Verbatim & Diagram Section -->
        <div class="section-label">📖 원문 전문 및 고화질 도해 다이어그램 뷰어</div>
        <div class="verbatim-section">
          <div class="verbatim-content" id="viewVerbatimText">
            <!-- Full verbatim text and images rendered here -->
          </div>
        </div>

      </div>
    </main>

  </div>

  <!-- Embedded 159 Posts Data -->
  <script>
    const ALL_POSTS = """ + json_str + """;

    let currentMainCat = '전체';
    let currentSubCat = '전체';
    let currentPostId = ALL_POSTS[0].id;
    let searchQuery = '';

    // Timer state
    let timerInterval = null;
    let timerSeconds = 30;
    let timerRunning = false;

    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }

    function init() {
      renderSubcategories();
      renderPostList();
      selectPost(currentPostId);

      document.getElementById('globalSearchInput').addEventListener('input', (e) => {
        searchQuery = e.target.value.trim().toLowerCase();
        renderPostList();
        const filtered = getFilteredPosts();
        if (filtered.length > 0 && !filtered.find(p => String(p.id) === String(currentPostId))) {
          selectPost(filtered[0].id);
        }
      });
    }

    function toggleTheme() {
      document.body.classList.toggle('dark-mode');
    }

    function setMainCategory(cat) {
      currentMainCat = cat;
      currentSubCat = '전체';
      document.querySelectorAll('.cat-tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.textContent.includes(cat) || (cat === '전체' && btn.textContent.includes('전체')));
      });
      renderSubcategories();
      renderPostList();
      const filtered = getFilteredPosts();
      if (filtered.length > 0) {
        selectPost(filtered[0].id);
      }
    }

    function setSubCategory(sub) {
      currentSubCat = sub;
      document.querySelectorAll('.subcat-chip').forEach(chip => {
        chip.classList.toggle('active', chip.textContent === sub || (sub === '전체' && chip.textContent.includes('전체')));
      });
      renderPostList();
      const filtered = getFilteredPosts();
      if (filtered.length > 0) {
        selectPost(filtered[0].id);
      }
    }

    function getFilteredPosts() {
      return ALL_POSTS.filter(p => {
        if (currentMainCat !== '전체' && p.main_category !== currentMainCat) return false;
        if (currentSubCat !== '전체' && p.sub_category !== currentSubCat) return false;
        if (searchQuery) {
          const matchTitle = p.title.toLowerCase().includes(searchQuery);
          const matchCore = (p.core.c + p.core.o + p.core.r + p.core.e).toLowerCase().includes(searchQuery);
          const matchText = p.verbatim_text.toLowerCase().includes(searchQuery);
          if (!matchTitle && !matchCore && !matchText) return false;
        }
        return true;
      });
    }

    function renderSubcategories() {
      const container = document.getElementById('subcatFilterBar');
      let relevantPosts = ALL_POSTS;
      if (currentMainCat !== '전체') {
        relevantPosts = ALL_POSTS.filter(p => p.main_category === currentMainCat);
      }
      const subcats = Array.from(new Set(relevantPosts.map(p => p.sub_category))).filter(Boolean);
      
      let html = `<span class="subcat-chip ${currentSubCat === '전체' ? 'active' : ''}" onclick="setSubCategory('전체')">전체 (${relevantPosts.length})</span>`;
      subcats.forEach(sub => {
        const count = relevantPosts.filter(p => p.sub_category === sub).length;
        html += `<span class="subcat-chip ${currentSubCat === sub ? 'active' : ''}" onclick="setSubCategory('${sub}')">${sub} (${count})</span>`;
      });
      container.innerHTML = html;
    }

    function renderPostList() {
      const container = document.getElementById('postListContainer');
      const filtered = getFilteredPosts();
      
      if (filtered.length === 0) {
        container.innerHTML = '<div style="padding: 30px; text-align: center; color: var(--text-muted); font-size: 13px;">일치하는 훈련과정이 없습니다.</div>';
        return;
      }

      container.innerHTML = filtered.map(p => {
        const isActive = (String(p.id) === String(currentPostId));
        const qCount = p.questions ? p.questions.length : 0;
        const imgCount = p.images ? p.images.length : 0;
        return `
          <div class="post-item ${isActive ? 'active' : ''}" data-id="${p.id}" onclick="selectPost('${p.id}')">
            <div class="post-item-meta">
              <span class="post-item-subcat">${escapeHtml(p.sub_category)}</span>
              <span class="post-item-id">#${p.id}</span>
            </div>
            <div class="post-item-title">${escapeHtml(p.title)}</div>
            <div class="post-item-badges">
              ${p.is_protected ? '<span class="badge-lock">🔒 보호글</span>' : ''}
              ${qCount > 0 ? `<span class="badge-q-count">🎙️ 면접Q ${qCount}</span>` : ''}
              ${imgCount > 0 ? `<span class="badge-img-count">🖼️ 도해 ${imgCount}</span>` : ''}
            </div>
          </div>
        `;
      }).join('');
    }

    function selectPost(id) {
      currentPostId = id;
      const post = ALL_POSTS.find(p => String(p.id) === String(id));
      if (!post) return;

      // Update Header
      document.getElementById('viewPostMainCat').textContent = '🚀 ' + post.main_category;
      document.getElementById('viewPostSubCat').textContent = post.sub_category;
      document.getElementById('viewPostTitle').textContent = post.title;

      // Update CORE
      document.getElementById('viewCoreC').textContent = post.core.c;
      document.getElementById('viewCoreO').textContent = post.core.o;
      document.getElementById('viewCoreR').textContent = post.core.r;
      document.getElementById('viewCoreE').textContent = post.core.e;

      // Update QA
      const qaContainer = document.getElementById('viewQaSection');
      const qaList = document.getElementById('viewQaList');
      if (post.questions && post.questions.length > 0) {
        qaContainer.style.display = 'block';
        qaList.innerHTML = post.questions.map(q => `
          <div class="qa-item">
            <div class="qa-header">${escapeHtml(q.header)}</div>
            <div class="qa-question">${escapeHtml(q.question)}</div>
          </div>
        `).join('');
      } else {
        qaContainer.style.display = 'none';
      }

      // Update Verbatim & Images
      const verbatimContainer = document.getElementById('viewVerbatimText');
      if (post.is_protected) {
        verbatimContainer.innerHTML = `<div class="protected-box">🔒 본 게시글은 작성자에 의해 비밀번호로 보호되어 있는 비공개 훈련과정입니다.<br><br><a href="${post.url}" target="_blank" style="color: var(--primary); text-decoration: underline;">원문 블로그에서 비밀번호 입력하고 보기</a></div>`;
      } else {
        // Format text with paragraph breaks and embed images at top / inline
        let textLines = post.verbatim_text.split('\\n');
        let textHtml = textLines.filter(l => l.trim()).map(l => `<p>${escapeHtml(l)}</p>`).join('');
        
        // Add images
        let imagesHtml = '';
        if (post.images && post.images.length > 0) {
          imagesHtml = '<div style="margin: 20px 0;">' + post.images.map(img => `
            <div class="verbatim-image-box">
              <img src="images/${img.local_filename}" onerror="this.src='${img.original_url}'" alt="도해 다이어그램" loading="lazy">
              <div class="img-caption">도해 다이어그램: ${img.local_filename} (원본 링크 연동)</div>
            </div>
          `).join('') + '</div>';
        }
        verbatimContainer.innerHTML = imagesHtml + textHtml;
      }

      // Re-render post item active state
      document.querySelectorAll('.post-item').forEach(el => {
        el.classList.toggle('active', el.getAttribute('data-id') === String(id));
      });

      // Scroll content area to top
      const scrollArea = document.querySelector('.main-scroll-view');
      if (scrollArea) scrollArea.scrollTop = 0;

      // Reset timer
      resetTimer();
    }

    function openOriginalUrl() {
      const post = ALL_POSTS.find(p => p.id === currentPostId);
      if (post) window.open(post.url, '_blank');
    }

    // Timer functions
    function toggleTimer() {
      if (timerRunning) {
        clearInterval(timerInterval);
        timerRunning = false;
        document.getElementById('timerStartBtn').textContent = '30초 답변 재시작';
      } else {
        timerSeconds = 30;
        timerRunning = true;
        document.getElementById('timerStartBtn').textContent = '정지';
        updateTimerDisplay();
        timerInterval = setInterval(() => {
          timerSeconds--;
          updateTimerDisplay();
          if (timerSeconds <= 0) {
            clearInterval(timerInterval);
            timerRunning = false;
            document.getElementById('timerStartBtn').textContent = '완료 (다시 연습)';
            alert('⏰ 30초 스피치 시간이 종료되었습니다!');
          }
        }, 1000);
      }
    }

    function resetTimer() {
      clearInterval(timerInterval);
      timerRunning = false;
      timerSeconds = 30;
      updateTimerDisplay();
      document.getElementById('timerStartBtn').textContent = '30초 답변 연습';
    }

    function updateTimerDisplay() {
      const min = String(Math.floor(timerSeconds / 60)).padStart(2, '0');
      const sec = String(timerSeconds % 60).padStart(2, '0');
      document.getElementById('timerDisplay').textContent = `${min}:${sec}`;
    }

    window.addEventListener('DOMContentLoaded', init);
  </script>
</body>
</html>
"""

# Save to result/260929_v1.0/index.html
out_html_v1 = result_dir / "index.html"
with open(out_html_v1, 'w', encoding='utf-8') as f:
    f.write(html_template)
print(f"Generated dashboard HTML: {out_html_v1} (Size: {out_html_v1.stat().st_size} bytes)")

# Also save to result/index.html (root distribution)
out_html_root = result_root / "index.html"
with open(out_html_root, 'w', encoding='utf-8') as f:
    f.write(html_template)
print(f"Generated root distribution HTML: {out_html_root} (Size: {out_html_root.stat().st_size} bytes)")

# Pair with run.bat in tool/260929_v1.0/
run_bat_path = Path(r"C:\Work\반도체\tool\260929_v1.0\run.bat")
run_bat_content = """@echo off
chcp 65001 > nul
setlocal

echo ======================================================================
echo  [반도체 159개 훈련과정 CORE 면접 대시보드 재생성 파이프라인]
echo ======================================================================
echo.

set "TOOL_DIR=%~dp0"
set "BASE_DIR=%TOOL_DIR%..\\..\\"

echo [1/3] 신규 포스트 수집 및 이미지 다운로드 확인 중...
python "%TOOL_DIR%crawler_all.py"

echo [2/3] CORE 프레임워크 및 카테고리 매핑 중...
python "%TOOL_DIR%core_builder.py"

echo [3/3] 대시보드 HTML 빌드 및 이미지 동기화 중...
python "%TOOL_DIR%build_dashboard.py"

echo.
echo ======================================================================
echo  빌드 완료! 브라우저에서 아래 대시보드를 실행합니다:
echo  %BASE_DIR%result\\index.html
echo ======================================================================
start "" "%BASE_DIR%result\\index.html"
pause
"""

with open(run_bat_path, 'w', encoding='utf-8') as f:
    f.write(run_bat_content)
print(f"Created paired run.bat: {run_bat_path}")

print("Dashboard build and pairing completed with 100% success!")
