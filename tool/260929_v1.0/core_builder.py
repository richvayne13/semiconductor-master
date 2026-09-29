import json, re, sys, os
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

posts_dir = Path(r"C:\Work\반도체\context\posts")
catalog_path = Path(r"C:\Work\반도체\context\post_catalog.json")

with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

print(f"Analyzing {len(catalog)} posts for CORE structuring and categorization...")

def classify_post(title, subcat, text):
    t = (title + " " + subcat).lower()
    
    # 1. 최신 기술 및 기업 (Tech & Market)
    if any(k in t for k in ['hbm', 'tsmc', '2nm', 'n2 공정', '18a', 'samsung vs. tsmc', '삼성 vs. tsmc', '시장 전망', '차세대 메모리] "processing-in-memory', 'pim']):
        if 'hbm' in t or 'pim' in t:
            return "최신 기술 및 기업", "HBM & 차세대 메모리"
        elif any(k in t for k in ['tsmc', '2nm', 'n2', '18a', 'samsung vs. tsmc']):
            return "최신 기술 및 기업", "파운드리 & 선단공정"
        else:
            return "최신 기술 및 기업", "기업 & 글로벌 시장 동향"

    # 2. 반도체 8대 공정 (Title-first precision matching)
    # 포토
    if any(k in t for k in ['포토', 'photo', 'litho', '노광', 'euv', 'arf', 'mask 3d', 'high-na', 'opc', 'psm']):
        return "반도체 8대 공정", "포토 공정 (Photo Lithography)"
    # 식각
    if any(k in t for k in ['식각', '에치', 'etch', '플라즈마', 'plasma', 'ale', 'rie', 'bosch']):
        return "반도체 8대 공정", "식각 공정 (Etch & Plasma)"
    # 증착/박막
    if any(k in t for k in ['증착', 'deposition', 'cvd', 'ald', 'pvd', 'sputter', '스퍼터링', 'passivation', 'encapsulation', '봉지 공정', 'high-k / low-k', 'plug w', 'si3n4', 'sio2 grown', '2차원 소재']):
        return "반도체 8대 공정", "박막 & 증착 공정 (Thin Film / CVD / ALD)"
    # 이온주입
    if any(k in t for k in ['이온주입', 'ion implant', 'implant 공정', 'doping profile', 'stopping mechanism', 'shallow junction']):
        return "반도체 8대 공정", "이온주입 공정 (Ion Implantation)"
    # 확산 및 열처리
    if any(k in t for k in ['diffusion 공정', '산화', '열산화', 'oxidation', 'anneal', '열처리']):
        return "반도체 8대 공정", "확산 & 열처리 공정 (Oxidation / Thermal)"
    # CMP 및 세정
    if any(k in t for k in ['세정', 'cleaning', 'cmp', '평탄화', 'c&c']):
        return "반도체 8대 공정", "CMP & 세정 공정 (C&C / Planarization)"
    # 금속배선 및 패키징
    if any(k in t for k in ['금속공정', '금속 공정', '메탈 공정', 'salicide', '살리사이드', 'schottky', 'ohmic', '쇼트키', '오믹', '패키징', 'tsv', 'electro migration', 'em', 'sm 저항성']):
        return "반도체 8대 공정", "금속배선 & 패키징 (Metallization & Packaging)"
    # 공정제어 및 수율/불량 분석
    if any(k in t for k in ['수율', 'yield', 'pcm', 'process control', 'process corner', 'shmoo plot', '상관성 분석', 'in-line monitoring', 'cmos process flow', '불량사례', '불랑사례', '불량 사례', '공정 margin']):
        return "반도체 8대 공정", "공정 제어 & 수율/불량 분석 (Yield & PCM)"

    # 3. 반도체 소자
    # DRAM
    if any(k in t for k in ['dram', 'ddr', 'lpddr']):
        return "반도체 소자", "DRAM 메모리"
    # NAND Flash
    if any(k in t for k in ['nand', '낸드', 'ctf', 'slc', 'mlc', 'tlc', '플로팅게이트', 'flash']):
        return "반도체 소자", "NAND Flash 메모리"
    # 3D 트랜지스터 (FinFET/GAA)
    if any(k in t for k in ['finfet', 'gaa', 'gate-all-around']):
        return "반도체 소자", "3D 트랜지스터 (FinFET/GAA)"
    # 단채널 효과 (SCE)
    if any(k in t for k in ['short channel', 'dibl', 'punch through', 'velocity saturation', 'gidl', 'hot carrier', 'subthreshold swing', 'ss 특성', 'channel이 짧아지면']):
        return "반도체 소자", "단채널 효과 (SCE) & 신뢰성"
    # 전력반도체 및 센서/디스플레이
    if any(k in t for k in ['전력반도체', 'power device', 'sic', 'gan', '화합물', 'pmic', 'cis', 'ccd', 't-con', 'ddi']):
        return "반도체 소자", "차세대 전력 & 특수 소자 (SiC/GaN/PMIC)"
    # MOSFET 기초 및 특성
    if any(k in t for k in ['mosfet', 'mos capacitor', 'threshold voltage', 'body effect', '출력특성', 'power current', 'dynamic/static power', 'hkmg', 'fd-soi', 'soi 기술', 'leakage current', 'i-mos', 't-fet', 'nc-fet', 'suspended fet', '메모리반도체 용어', '시스템반도체 용어', 'xrd', 'nbti', 'pbti', 'hci', 'lcr 미터', '커패시턴스 측정']):
        return "반도체 소자", "MOSFET 기초 & 소자 물리"
        
    return "반도체 8대 공정", "공정 일반 & 종합"

def extract_core_from_text(title, text):
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # 1. Concept: look for early definition or title reformulation
    c_candidates = []
    o_candidates = []
    r_candidates = []
    e_candidates = []
    
    for l in lines[:25]:
        if any(kw in l for kw in ['이란', '의미합니다', '정의할 수', '정의합니다', '역할을 합니다', '기술입니다', '공정입니다', '소자입니다', '말합니다']):
            c_candidates.append(l)
        elif any(kw in l for kw in ['배경', '한계', '문제점', '이유는', '필요성', '기존', '도입', '단점']):
            o_candidates.append(l)
            
    for l in lines[10:]:
        if any(kw in l for kw in ['원리', '메커니즘', '반응식', '과정', '스텝', '원자', '플라즈마', '전자', '캐리어', '전압', '공식']):
            if len(r_candidates) < 4: r_candidates.append(l)
        if any(kw in l for kw in ['효과', '장점', '수율', '개선', '감소', '향상', '극복', '과제', 'challenge', '한계점']):
            if len(e_candidates) < 3: e_candidates.append(l)

    c_text = " ".join(c_candidates[:2]) if c_candidates else f"{title}에 대한 핵심 기술 및 기본 개념입니다."
    o_text = " ".join(o_candidates[:2]) if o_candidates else "기존 공정/소자의 물리적 한계를 극복하고 초미세 패턴 및 고성능을 구현하기 위해 도입되었습니다."
    r_text = " ".join(r_candidates[:3]) if r_candidates else "도메인 물리/화학적 상호작용 및 전계/에너지 제어를 통해 작동 메커니즘이 구현됩니다."
    e_text = " ".join(e_candidates[:2]) if e_candidates else "공정 산포 억제, 수율 향상 및 디바이스 동작 신뢰성 확보에 기여합니다."
    
    return c_text, o_text, r_text, e_text

processed_posts = []

for item in catalog:
    post_id = item['id']
    post_file = posts_dir / f"{post_id}.json"
    
    if post_file.exists():
        with open(post_file, 'r', encoding='utf-8') as pf:
            data = json.load(pf)
        
        title = data.get('title', item['title'])
        text = data.get('verbatim_text', '')
        subcat = data.get('subcat', item.get('subcat', ''))
        
        main_cat, sub_cat = classify_post(title, subcat, text)
        c, o, r, e = extract_core_from_text(title, text)
        
        processed_posts.append({
            'id': post_id,
            'url': item['url'],
            'title': title,
            'main_category': main_cat,
            'sub_category': sub_cat,
            'is_protected': False,
            'core': {
                'c': c,
                'o': o,
                'r': r,
                'e': e
            },
            'questions': data.get('questions', []),
            'images': data.get('images', []),
            'verbatim_text': text,
            'raw_html': data.get('raw_html', '')
        })
    else:
        # Protected posts (e.g. 194, 191, 190, 189, 109)
        title = item['title']
        main_cat, sub_cat = classify_post(title, item.get('subcat', ''), '')
        processed_posts.append({
            'id': post_id,
            'url': item['url'],
            'title': title,
            'main_category': main_cat,
            'sub_category': sub_cat,
            'is_protected': True,
            'core': {
                'c': f"[{title}] 원문은 작성자에 의해 비밀번호로 보호된 비공개 훈련과정입니다.",
                'o': "심화 훈련 및 사관학교 전용 콘텐츠로 보호 설정되어 있습니다.",
                'r': "비밀번호 보호 글로 본문 텍스트가 암호화되어 있습니다.",
                'e': "관련 공정 및 소자의 심화 학습 주제로 참고하시기 바랍니다."
            },
            'questions': [],
            'images': [],
            'verbatim_text': "본 게시글은 작성자에 의해 비밀번호로 보호되어 있는 비공개 훈련과정입니다.",
            'raw_html': "<div class='protected-box'>🔒 본 게시글은 작성자에 의해 비밀번호로 보호되어 있는 비공개 글입니다.</div>"
        })

print(f"Processed {len(processed_posts)} posts.")

# Category breakdown statistics
cat_stats = {}
for p in processed_posts:
    mc = p['main_category']
    sc = p['sub_category']
    key = f"{mc} > {sc}"
    cat_stats[key] = cat_stats.get(key, 0) + 1

print("\n--- Categorization Breakdown ---")
for k, v in sorted(cat_stats.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v} posts")

out_file = Path(r"C:\Work\반도체\context\processed_all_posts.json")
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(processed_posts, f, ensure_ascii=False, indent=2)

print(f"\nSaved structured posts dataset to {out_file} (Size: {out_file.stat().st_size} bytes)")
