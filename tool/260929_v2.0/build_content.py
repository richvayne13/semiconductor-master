import json, sys, re, os
from pathlib import Path
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

posts_dir = Path(r"C:\Work\반도체\context\posts")
catalog_path = Path(r"C:\Work\반도체\context\post_catalog.json")
output_path = Path(r"C:\Work\반도체\context\processed_all_posts_v2.json")

with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

print(f"Loaded {len(catalog)} posts from catalog.")

def classify_post(title, subcat):
    raw = (title + " " + subcat).strip()
    t = raw.lower()

    # --- Step 1: Explicit bracket prefixes & major series prefixes ---
    # 1.1 [증착공정] or 증착 관련 시리즈
    if any(k in raw for k in ['[증착공정]', '[증착 공정]', '증착공정', '증착 공정']):
        return "반도체 8대 공정", "D", "박막 & 증착 공정 (Deposition)"
        
    # 1.2 [식각공정] or 식각/에치 관련 시리즈
    if any(k in raw for k in ['[식각공정]', '[식각 공정]', '식각공정', '에치공정', '에치 공정']):
        return "반도체 8대 공정", "E", "식각 공정 (Etch)"

    # 1.3 [포토공정] or 포토 관련 시리즈
    if any(k in raw for k in ['[포토공정]', '[포토 공정]', '포토공정', '포토 공정']):
        return "반도체 8대 공정", "P", "포토 공정 (Photo)"

    # 1.4 [이온주입 공정]
    if any(k in raw for k in ['[이온주입 공정]', '[이온주입]', '이온주입 공정', '이온주입']):
        return "반도체 8대 공정", "I", "이온주입 공정 (Ion Implantation)"

    # 1.5 [세정 공정] / [평탄화 공정] / C&C
    if any(k in raw for k in ['[세정 공정]', '[세정]', '[평탄화 공정]', '세정 공정', '세정공정', 'cmp 공정', 'c&c']):
        return "반도체 8대 공정", "C", "CMP & 세정 공정 (Cleaning & CMP)"

    # 1.6 [금속공정] / [금속 공정] / 메탈 공정 / 패키징
    if any(k in raw for k in ['[금속공정]', '[금속 공정]', '메탈 공정', '금속 공정', '[패키징 공정]']):
        return "반도체 8대 공정", "M", "금속배선 & 패키징 (Metal & Packaging)"

    # 1.7 [Diffusion 공정] / 확산
    if any(k in raw for k in ['diffusion 공정', '확산 공정']):
        return "반도체 8대 공정", "T", "확산 & 열처리 공정 (Thermal)"

    # 1.8 [Short Channel Effect]
    if 'short channel effect' in t:
        return "반도체 소자", "SCE", "단채널 효과 & 신뢰성"

    # 1.9 [DRAM] (단, HBM 제외)
    if 'hbm' not in t and any(k in t for k in ['[dram #1]', '[dram #4]', '3d dram', '[ddr & lpddr]']):
        return "반도체 소자", "DRAM", "DRAM 메모리"

    # 1.10 [NAND Flash]
    if any(k in t for k in ['nand flash', '낸드플래시', '[nand']):
        return "반도체 소자", "NAND", "NAND Flash 메모리"

    # --- Step 2: 최신 기술 및 기업 (HBM, 선단공정/파운드리) ---
    if any(k in t for k in ['hbm', 'pim', 'processing-in-memory']):
        return "최신 기술 및 기업", "HBM", "HBM & 차세대 메모리"
    if any(k in t for k in ['tsmc', '2nm', 'n2 공정', '18a', 'samsung vs. tsmc', '삼성 vs. tsmc', '3nm 경쟁력']):
        return "최신 기술 및 기업", "FND", "파운드리 & 선단공정"

    # --- Step 3: 플라즈마 시리즈 (식각 관련) ---
    if any(k in raw for k in ['플라즈마, 3편으로 끝낸다', '플라즈마 (Plasma) 기초부터 심화까지']):
        return "반도체 8대 공정", "E", "식각 공정 (Etch)"

    # --- Step 4: 수율 및 공정 제어 (Yield & PCM) ---
    if any(k in t for k in ['shmoo plot', '상관성 분석', 'in-line monitoring', 'pcm', 'process control', 'process corner', 'corner margin', '수율', 'yield', '공정 margin', 'cmos process flow']):
        return "반도체 8대 공정", "Y", "수율 & 공정제어 (Yield & PCM)"

    # --- Step 5: 반도체 8대 공정 키워드 매칭 ---
    # 포토 공정 (P)
    if any(k in t for k in ['포토', 'photo', 'litho', '노광', 'euv', 'arf', 'mask 3d', 'high-na', 'opc', 'psm', 'photoresist']):
        return "반도체 8대 공정", "P", "포토 공정 (Photo)"
    # 박막 & 증착 공정 (D)
    if any(k in t for k in ['증착', 'deposition', 'cvd', 'ald', 'pvd', 'sputter', '스퍼터링', 'passivation', 'encapsulation', '봉지 공정', 'high-k / low-k', 'plug w', 'si3n4', 'sio2 grown', '2차원 소재']):
        return "반도체 8대 공정", "D", "박막 & 증착 공정 (Deposition)"
    # 식각 공정 (E)
    if any(k in t for k in ['식각', '에치', 'etch', '플라즈마', 'plasma', 'ale', 'rie', 'bosch']):
        return "반도체 8대 공정", "E", "식각 공정 (Etch)"
    # 이온주입 공정 (I)
    if any(k in t for k in ['이온주입', 'ion implant', 'implant 공정', 'doping profile', 'stopping mechanism', 'shallow junction']):
        return "반도체 8대 공정", "I", "이온주입 공정 (Ion Implantation)"
    # 확산 & 열처리 공정 (T)
    if any(k in t for k in ['diffusion', '산화', '열산화', 'oxidation', 'anneal', '열처리']):
        return "반도체 8대 공정", "T", "확산 & 열처리 공정 (Thermal)"
    # CMP & 세정 공정 (C)
    if any(k in t for k in ['세정', 'cleaning', 'cmp', '평탄화']):
        return "반도체 8대 공정", "C", "CMP & 세정 공정 (Cleaning & CMP)"
    # 금속배선 & 패키징 (M)
    if any(k in t for k in ['salicide', '살리사이드', 'schottky', 'ohmic', '쇼트키', '오믹', '패키징', 'tsv']):
        return "반도체 8대 공정", "M", "금속배선 & 패키징 (Metal & Packaging)"

    # --- Step 6: 반도체 소자 키워드 매칭 ---
    if any(k in t for k in ['dram', 'ddr', 'lpddr']):
        return "반도체 소자", "DRAM", "DRAM 메모리"
    if any(k in t for k in ['nand', '낸드', 'ctf', 'slc', 'mlc', 'tlc', '플로팅게이트', 'flash']):
        return "반도체 소자", "NAND", "NAND Flash 메모리"
    if any(k in t for k in ['finfet', 'gaa', 'gate-all-around']):
        return "반도체 소자", "GAA", "3D 트랜지스터 (FinFET/GAA)"
    if any(k in t for k in ['short channel', 'dibl', 'punch through', 'velocity saturation', 'gidl', 'hot carrier', 'subthreshold swing', 'ss 특성', 'channel이 짧아지면']):
        return "반도체 소자", "SCE", "단채널 효과 & 신뢰성"
    if any(k in t for k in ['전력반도체', 'power device', 'sic', 'gan', '화합물', 'pmic', 'cis', 'ccd', 't-con', 'ddi', '디스플레이']):
        return "반도체 소자", "PWR", "전력반도체 & 특수소자"
    if any(k in t for k in ['mosfet', 'mos capacitor', 'threshold voltage', 'body effect', '출력특성', 'power current', 'dynamic/static power', 'hkmg', 'fd-soi', 'soi 기술', 'leakage current', 'i-mos', 't-fet', 'nc-fet', 'suspended fet', '메모리반도체 용어', '시스템반도체 용어', 'xrd', 'nbti', 'pbti', 'hci', 'lcr 미터', '커패시턴스 측정']):
        return "반도체 소자", "MOS", "MOSFET 기초 & 소자물리"

    return "반도체 8대 공정", "기타", "공정 일반 & 종합"

def clean_and_interleave_html(raw_html, images_list, post_id):
    if not raw_html or not raw_html.strip():
        return ""
    
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    # Remove unwanted scripts, styles, trackers, and ad elements
    for bad in soup.find_all(['script', 'style', 'iframe', 'form']):
        bad.decompose()
    for bad in soup.find_all(class_=['container_postbtn', 'revenue_unit_wrap', 'tag_trail', 'another_category', 'comment_box']):
        bad.decompose()
        
    # Find all actual article images
    content_imgs = [img for img in soup.find_all('img') if not any(x in (img.get('src') or '') for x in ['no-image-v1', 'tistory_admin', 't1.daumcdn.net/tistory_admin'])]
    
    for idx, img in enumerate(content_imgs):
        if idx < len(images_list):
            img_meta = images_list[idx]
            local_fn = img_meta.get('local_filename', f"{post_id}_{idx}.png")
            orig_url = img_meta.get('original_url', img.get('src', ''))
        else:
            local_fn = f"{post_id}_{idx}.png"
            orig_url = img.get('src', '')
            
        img['src'] = f"images/{local_fn}"
        img['onerror'] = f"this.src='{orig_url}'"
        img['loading'] = "lazy"
        img['alt'] = f"도해 다이어그램 ({local_fn})"
        
        # Remove responsive distortion attributes
        img.attrs.pop('srcset', None)
        img.attrs.pop('data-origin-width', None)
        img.attrs.pop('data-origin-height', None)
        img.attrs.pop('width', None)
        img.attrs.pop('height', None)
        
        # Add clean responsive styling
        img['style'] = "max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 8px; box-shadow: 0 4px 14px rgba(0,0,0,0.08);"
        
    return str(soup)

processed_posts = []

for item in catalog:
    post_id = str(item['id'])
    post_file = posts_dir / f"{post_id}.json"
    
    main_cat, sub_code, sub_name = classify_post(item['title'], item.get('subcat', ''))
    
    if not post_file.exists():
        # Protected or missing post
        processed_posts.append({
            "id": post_id,
            "url": item['url'],
            "title": item['title'],
            "main_category": main_cat,
            "sub_category": sub_code,
            "sub_category_name": sub_name,
            "is_protected": True,
            "images": [],
            "questions": [],
            "content_html": f'<div class="protected-box">🔒 본 훈련과정(#{post_id})은 작성자에 의해 비밀번호로 보호되어 있는 비공개 글입니다.<br><br><a href="{item["url"]}" target="_blank" class="btn-top" style="display:inline-block; margin-top:12px;">원문 블로그에서 비밀번호 입력하고 보기</a></div>',
            "verbatim_text": "본 게시글은 작성자에 의해 비밀번호로 보호되어 있습니다."
        })
        continue
        
    with open(post_file, 'r', encoding='utf-8') as f:
        pdata = json.load(f)
        
    is_protected = pdata.get('is_protected', False)
    images_list = pdata.get('images', [])
    raw_html = pdata.get('raw_html', '')
    
    if is_protected or not raw_html:
        content_html = f'<div class="protected-box">🔒 본 훈련과정(#{post_id})은 작성자에 의해 비밀번호로 보호되어 있는 비공개 글입니다.<br><br><a href="{item["url"]}" target="_blank" class="btn-top" style="display:inline-block; margin-top:12px;">원문 블로그에서 비밀번호 입력하고 보기</a></div>'
    else:
        content_html = clean_and_interleave_html(raw_html, images_list, post_id)
        
    processed_posts.append({
        "id": post_id,
        "url": item['url'],
        "title": item['title'],
        "main_category": main_cat,
        "sub_category": sub_code,
        "sub_category_name": sub_name,
        "is_protected": is_protected,
        "images": images_list,
        "questions": pdata.get('questions', []),
        "content_html": content_html,
        "verbatim_text": pdata.get('verbatim_text', '')
    })

print(f"Processed all {len(processed_posts)} posts.")

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(processed_posts, f, ensure_ascii=False, indent=2)

print(f"Saved processed posts to {output_path} (Size: {output_path.stat().st_size} bytes)")
