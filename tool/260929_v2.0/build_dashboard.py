import json, sys, os, html, shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

data_path = Path(r"C:\Work\반도체\context\processed_all_posts_v2.json")
result_v2 = Path(r"C:\Work\반도체\result\260929_v2.0")
result_root = Path(r"C:\Work\반도체\result")
workspace_root = Path(r"C:\Work\반도체")
images_src = Path(r"C:\Work\반도체\context\images")

result_v2.mkdir(parents=True, exist_ok=True)
images_dst_v2 = result_v2 / "images"
images_dst_root = result_root / "images"
images_dst_ws = workspace_root / "images"

print("Syncing images across result and workspace root for offline and GitHub Pages...")
if not images_dst_v2.exists():
    shutil.copytree(images_src, images_dst_v2)
if not images_dst_root.exists():
    shutil.copytree(images_src, images_dst_root)
if not images_dst_ws.exists():
    shutil.copytree(images_src, images_dst_ws)

print(f"Loaded processed data from {data_path}...")
with open(data_path, 'r', encoding='utf-8') as f:
    posts = json.load(f)

print(f"Total posts: {len(posts)}")
json_str = json.dumps(posts, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>반도체사관학교 159개 훈련과정 - 반도체 8대공정 & 소자/기술 마스터 대시보드</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-main: #f8fafc;
      --bg-sidebar: #ffffff;
      --bg-card: #ffffff;
      --border: #e2e8f0;
      --border-focus: #2563eb;
      --text-main: #0f172a;
      --text-sub: #475569;
      --text-muted: #94a3b8;
      --primary: #2563eb;
      --primary-light: #eff6ff;
      --primary-dark: #1d4ed8;
      
      --accent-p: #0284c7;  /* Photo - Sky Blue */
      --accent-e: #ea580c;  /* Etch - Orange */
      --accent-d: #8b5cf6;  /* Deposition - Purple */
      --accent-i: #059669;  /* Implant - Emerald */
      --accent-t: #dc2626;  /* Thermal - Red */
      --accent-c: #0d9488;  /* CMP/Cleaning - Teal */
      --accent-m: #d97706;  /* Metal - Amber */
      --accent-y: #4f46e5;  /* Yield - Indigo */
      
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
      --text-sub: #cbd5e1;
      --text-muted: #64748b;
      --primary: #3b82f6;
      --primary-light: #1e3a8a;
      --primary-dark: #60a5fa;
      
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
      --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.4);
      --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.5);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
      background-color: var(--bg-main);
      color: var(--text-main);
      line-height: 1.6;
      overflow: hidden;
      height: 100vh;
      display: flex;
      flex-direction: column;
    }

    /* Top Bar Header */
    .top-bar {
      height: 60px;
      background: var(--bg-sidebar);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      flex-shrink: 0;
      z-index: 100;
      box-shadow: var(--shadow-sm);
    }

    .brand-wrap {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-badge {
      background: linear-gradient(135deg, #2563eb, #1d4ed8);
      color: #ffffff;
      font-size: 11px;
      font-weight: 800;
      padding: 4px 9px;
      border-radius: 6px;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }
    .brand-title {
      font-size: 17px;
      font-weight: 700;
      letter-spacing: -0.4px;
      color: var(--text-main);
    }

    .top-actions {
      display: flex;
      align-items: center;
      gap: 14px;
    }
    .search-box {
      position: relative;
      width: 320px;
    }
    .search-box input {
      width: 100%;
      height: 38px;
      padding: 0 14px 0 38px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--bg-main);
      color: var(--text-main);
      font-size: 13px;
      outline: none;
      transition: all 0.2s;
    }
    .search-box input:focus {
      border-color: var(--border-focus);
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
      background: var(--bg-sidebar);
    }
    .search-icon {
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 14px;
      color: var(--text-muted);
      pointer-events: none;
    }

    .btn-top {
      height: 36px;
      padding: 0 14px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--bg-sidebar);
      color: var(--text-main);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
      text-decoration: none;
    }
    .btn-top:hover {
      background: var(--primary-light);
      border-color: var(--primary);
      color: var(--primary);
    }

    /* App Layout */
    .app-body {
      flex: 1;
      display: flex;
      overflow: hidden;
      position: relative;
    }

    /* Sidebar */
    .sidebar {
      width: 390px;
      background: var(--bg-sidebar);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
    }

    /* Category Tabs */
    .category-tabs {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 6px;
      padding: 12px 14px 8px;
      background: var(--bg-sidebar);
      border-bottom: 1px solid var(--border);
    }
    .cat-tab-btn {
      padding: 9px 8px;
      border: 1px solid var(--border);
      background: var(--bg-main);
      color: var(--text-sub);
      font-size: 12px;
      font-weight: 700;
      border-radius: 7px;
      cursor: pointer;
      transition: all 0.2s;
      text-align: center;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .cat-tab-btn:hover {
      border-color: var(--primary);
      color: var(--primary);
    }
    .cat-tab-btn.active {
      background: var(--primary);
      color: #ffffff;
      border-color: var(--primary);
      box-shadow: 0 2px 4px rgba(37, 99, 235, 0.25);
    }

    /* Subcategory Chips */
    .subcat-filter-bar {
      display: flex;
      gap: 6px;
      padding: 8px 12px;
      overflow-x: auto;
      border-bottom: 1px solid var(--border);
      background: var(--bg-sidebar);
      flex-shrink: 0;
    }
    .subcat-filter-bar::-webkit-scrollbar { height: 4px; }
    .subcat-filter-bar::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

    .subcat-chip {
      padding: 4px 10px;
      font-size: 11px;
      font-weight: 600;
      border-radius: 14px;
      background: var(--bg-main);
      color: var(--text-sub);
      border: 1px solid var(--border);
      white-space: nowrap;
      cursor: pointer;
      transition: all 0.15s;
    }
    .subcat-chip:hover {
      border-color: var(--primary);
      color: var(--primary);
    }
    .subcat-chip.active {
      background: var(--primary-light);
      border-color: var(--primary);
      color: var(--primary);
      font-weight: 700;
    }

    /* Post List */
    .post-list-wrap {
      flex: 1;
      overflow-y: auto;
      padding: 8px 10px;
    }
    .post-item {
      padding: 12px 14px;
      margin-bottom: 8px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--bg-card);
      cursor: pointer;
      transition: all 0.15s;
    }
    .post-item:hover {
      border-color: var(--border-focus);
      transform: translateY(-1px);
      box-shadow: var(--shadow-sm);
    }
    .post-item.active {
      border-color: var(--primary);
      background: var(--primary-light);
      box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
    }
    body.dark-mode .post-item.active {
      background: rgba(59, 130, 246, 0.15);
    }

    .post-item-meta {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 6px;
    }
    .post-item-subcat {
      font-size: 11px;
      font-weight: 700;
      color: var(--primary);
      padding: 2px 7px;
      background: rgba(37, 99, 235, 0.08);
      border-radius: 4px;
      border: 1px solid rgba(37, 99, 235, 0.2);
    }
    .post-item-id {
      font-size: 11px;
      font-weight: 600;
      color: var(--text-muted);
      font-family: 'JetBrains Mono', monospace;
    }
    .post-item-title {
      font-size: 13px;
      font-weight: 600;
      line-height: 1.45;
      color: var(--text-main);
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .post-item-badges {
      display: flex;
      align-items: center;
      gap: 6px;
      margin-top: 8px;
    }
    .badge-q-count {
      font-size: 11px;
      font-weight: 600;
      color: #059669;
      background: #ecfdf5;
      border: 1px solid #a7f3d0;
      padding: 1px 6px;
      border-radius: 4px;
    }
    body.dark-mode .badge-q-count {
      background: rgba(16, 185, 129, 0.15);
      border-color: #059669;
      color: #6ee7b7;
    }
    .badge-img-count {
      font-size: 11px;
      font-weight: 600;
      color: #7c3aed;
      background: #f5f3ff;
      border: 1px solid #ddd6fe;
      padding: 1px 6px;
      border-radius: 4px;
    }
    body.dark-mode .badge-img-count {
      background: rgba(139, 92, 246, 0.15);
      border-color: #8b5cf6;
      color: #c4b5fd;
    }
    .badge-lock {
      font-size: 11px;
      font-weight: 600;
      color: #e11d48;
      background: #fff1f2;
      border: 1px solid #fecdd3;
      padding: 1px 6px;
      border-radius: 4px;
    }

    /* Main Content Area */
    .content-area {
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      background: var(--bg-main);
    }

    /* Sticky Post Header */
    .content-header-sticky {
      background: var(--bg-sidebar);
      border-bottom: 1px solid var(--border);
      padding: 16px 28px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
      flex-shrink: 0;
      box-shadow: var(--shadow-sm);
    }
    .post-header-info {
      flex: 1;
      min-width: 0;
    }
    .post-header-tag {
      font-size: 12px;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .post-header-title {
      font-size: 20px;
      font-weight: 800;
      line-height: 1.35;
      color: var(--text-main);
      letter-spacing: -0.4px;
      word-break: keep-all;
    }
    .post-header-controls {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-shrink: 0;
    }
    .timer-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      background: var(--bg-main);
      border: 1px solid var(--border);
      border-radius: 8px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 14px;
      font-weight: 700;
      color: var(--text-main);
    }
    .btn-timer {
      padding: 8px 14px;
      border: none;
      border-radius: 8px;
      background: var(--primary);
      color: #ffffff;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s;
    }
    .btn-timer:hover {
      background: var(--primary-dark);
    }

    /* Scrollable Viewer */
    .main-scroll-view {
      flex: 1;
      overflow-y: auto;
      padding: 28px 36px;
    }

    /* Interview Q&A Section */
    .qa-section {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 20px 24px;
      margin-bottom: 28px;
      box-shadow: var(--shadow-sm);
    }
    .section-label {
      font-size: 15px;
      font-weight: 800;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 16px;
    }
    .qa-item {
      background: var(--bg-main);
      border: 1px solid var(--border);
      border-left: 4px solid var(--primary);
      border-radius: 6px;
      padding: 12px 16px;
      margin-bottom: 10px;
      transition: all 0.2s;
    }
    .qa-item:hover {
      border-color: var(--primary);
      box-shadow: var(--shadow-sm);
    }
    .qa-header {
      font-size: 14px;
      font-weight: 700;
      color: var(--primary-dark);
      margin-bottom: 4px;
    }
    body.dark-mode .qa-header {
      color: #93c5fd;
    }
    .qa-question {
      font-size: 14px;
      color: var(--text-main);
      line-height: 1.5;
    }

    /* Article Reading Container (Interleaved Exact Flow) */
    .article-container {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 36px 40px;
      box-shadow: var(--shadow-sm);
      margin-bottom: 40px;
    }

    .article-body {
      font-size: 15.5px;
      line-height: 1.85;
      color: var(--text-main);
      letter-spacing: -0.015em;
    }

    .article-body p {
      margin-bottom: 18px;
      word-break: keep-all;
    }

    .article-body h2, .article-body h3, .article-body h4 {
      margin-top: 32px;
      margin-bottom: 14px;
      font-weight: 800;
      color: var(--text-main);
      letter-spacing: -0.3px;
    }
    .article-body h2 {
      font-size: 20px;
      padding-bottom: 8px;
      border-bottom: 2px solid var(--border);
    }
    .article-body h3 {
      font-size: 17px;
      color: var(--primary-dark);
    }
    body.dark-mode .article-body h3 {
      color: #93c5fd;
    }

    .article-body blockquote {
      margin: 20px 0;
      padding: 16px 20px;
      background: var(--bg-main);
      border-left: 4px solid var(--primary);
      border-radius: 0 8px 8px 0;
      color: var(--text-sub);
      font-size: 15px;
      line-height: 1.75;
    }
    body.dark-mode .article-body blockquote {
      background: rgba(30, 41, 59, 0.7);
    }

    .article-body figure {
      margin: 24px 0;
      text-align: center;
    }
    .article-body img {
      max-width: 100% !important;
      height: auto !important;
      display: block;
      margin: 20px auto;
      border-radius: 8px;
      box-shadow: 0 4px 14px rgba(0,0,0,0.08);
      border: 1px solid var(--border);
    }
    body.dark-mode .article-body img {
      box-shadow: 0 4px 14px rgba(0,0,0,0.4);
    }

    .article-body figcaption {
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 8px;
      font-weight: 500;
    }

    .article-body hr {
      border: none;
      height: 1px;
      background: var(--border);
      margin: 28px 0;
    }

    .article-body table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
      font-size: 14px;
    }
    .article-body th, .article-body td {
      border: 1px solid var(--border);
      padding: 10px 14px;
      text-align: left;
    }
    .article-body th {
      background: var(--bg-main);
      font-weight: 700;
    }

    .protected-box {
      padding: 48px 24px;
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
      <span class="brand-badge">반도체 159 마스터</span>
      <h1 class="brand-title">딴딴's 반도체사관학교 159 훈련과정</h1>
    </div>

    <div class="top-actions">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" id="globalSearchInput" placeholder="[P], [E], [D], 공정, 소자 키워드 통합 검색...">
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
            <span id="viewPostMainCat">🚀 반도체 8대 공정</span> • <span id="viewPostSubCat">[P] 포토 공정</span>
          </div>
          <h2 class="post-header-title" id="viewPostTitle">포스트 제목</h2>
        </div>
        <div class="post-header-controls">
          <div class="timer-badge">
            ⏱️ <span id="timerDisplay">00:30</span>
          </div>
          <button class="btn-timer" id="timerStartBtn" onclick="toggleTimer()">30초 답변 연습</button>
          <button class="btn-top" id="openOriginalBtn" onclick="openOriginalUrl()">🔗 원본 글 보기</button>
        </div>
      </div>

      <!-- Scrollable Viewer -->
      <div class="main-scroll-view">
        
        <!-- Interview Q&A Section -->
        <div class="qa-section" id="viewQaSection" style="display: none;">
          <div class="section-label">🎙️ 실전 면접 기출 및 예상 질문</div>
          <div id="viewQaList">
            <!-- Questions rendered here -->
          </div>
        </div>

        <!-- Full Verbatim Article & Interleaved Diagrams Section -->
        <div class="section-label">📖 원문 전문 및 기술 도해 다이어그램 뷰어</div>
        <div class="article-container">
          <div class="article-body" id="viewArticleBody">
            <!-- Interleaved exact flow rendered here -->
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
          const matchSub = p.sub_category.toLowerCase().includes(searchQuery);
          const matchText = p.verbatim_text.toLowerCase().includes(searchQuery);
          if (!matchTitle && !matchSub && !matchText) return false;
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

      // Update Interleaved Article Body
      const articleBody = document.getElementById('viewArticleBody');
      if (post.is_protected) {
        articleBody.innerHTML = post.content_html;
      } else {
        articleBody.innerHTML = post.content_html;
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

# Save to result/260929_v2.0/index.html
out_html_v2 = result_v2 / "index.html"
with open(out_html_v2, 'w', encoding='utf-8') as f:
    f.write(html_template)
print(f"Generated v2.0 dashboard HTML: {out_html_v2} (Size: {out_html_v2.stat().st_size} bytes)")

# Save to result/index.html
out_html_root = result_root / "index.html"
with open(out_html_root, 'w', encoding='utf-8') as f:
    f.write(html_template)
print(f"Generated root distribution HTML: {out_html_root} (Size: {out_html_root.stat().st_size} bytes)")

# Save to C:\Work\반도체\index.html (for GitHub Pages root)
out_html_ws = workspace_root / "index.html"
with open(out_html_ws, 'w', encoding='utf-8') as f:
    f.write(html_template)
print(f"Generated workspace root HTML (GitHub Pages): {out_html_ws} (Size: {out_html_ws.stat().st_size} bytes)")

# Pair with run.bat in tool/260929_v2.0/
run_bat_path = Path(r"C:\Work\반도체\tool\260929_v2.0\run.bat")
run_bat_content = """@echo off
chcp 65001 > nul
setlocal

echo ======================================================================
echo  [반도체 159 훈련과정 원문인라인 도해 대시보드 v2.0 재생성 파이프라인]
echo ======================================================================
echo.

set "TOOL_DIR=%~dp0"
set "BASE_DIR=%TOOL_DIR%..\\..\\"

echo [1/2] 원문 도해-텍스트 인라인 결합 및 영문 코드 분류 중...
python "%TOOL_DIR%build_content.py"

echo [2/2] v2.0 대시보드 HTML 빌드 및 이미지 동기화 중...
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

print("Dashboard v2.0 build and pairing completed with 100% success!")
