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
    t = (title + " " + subcat).lower()
    
    # 1. 최신 기술 및 기업 (Tech & Market)
    if any(k in t for k in ['hbm', 'tsmc', '2nm', 'n2 공정', '18a', 'samsung vs. tsmc', '삼성 vs. tsmc', '시장 전망', '차세대 메모리] "processing-in-memory', 'pim']):
        if 'hbm' in t or 'pim' in t:
            return "최신 기술 및 기업", "HBM", "HBM & 차세대 메모리"
        elif any(k in t for k in ['tsmc', '2nm', 'n2', '18a', 'samsung vs. tsmc']):
            return "최신 기술 및 기업", "FND", "파운드리 & 선단공정"
        else:
            return "최신 기술 및 기업", "MKT", "기업 & 시장 동향"

    # 2. 반도체 8대 공정 (8 Major Processes - Pure Initials P, E, D, I, T, C, M, Y)
    # P : 포토 공정 (Photo)
    if any(k in t for k in ['포토', 'photo', 'litho', '노광', 'euv', 'arf', 'mask 3d', 'high-na', 'opc', 'psm']):
        return "반도체 8대 공정", "P", "포토 공정 (Photo)"
    # E : 식각 공정 (Etch)
    if any(k in t for k in ['식각', '에치', 'etch', '플라즈마', 'plasma', 'ale', 'rie', 'bosch']):
        return "반도체 8대 공정", "E", "식각 공정 (Etch)"
    # D : 박막 & 증착 공정 (Deposition)
    if any(k in t for k in ['증착', 'deposition', 'cvd', 'ald', 'pvd', 'sputter', '스퍼터링', 'passivation', 'encapsulation', '봉지 공정', 'high-k / low-k', 'plug w', 'si3n4', 'sio2 grown', '2차원 소재']):
        return "반도체 8대 공정", "D", "박막 & 증착 공정 (Deposition)"
    # I : 이온주입 공정 (Ion Implantation)
    if any(k in t for k in ['이온주입', 'ion implant', 'implant 공정', 'doping profile', 'stopping mechanism', 'shallow junction']):
        return "반도체 8대 공정", "I", "이온주입 공정 (Ion Implantation)"
    # T : 확산 & 열처리 공정 (Thermal)
    if any(k in t for k in ['diffusion 공정', '산화', '열산화', 'oxidation', 'anneal', '열처리']):
        return "반도체 8대 공정", "T", "확산 & 열처리 공정 (Thermal)"
    # C : CMP & 세정 공정 (Cleaning & CMP)
    if any(k in t for k in ['세정', 'cleaning', 'cmp', '평탄화', 'c&c']):
        return "반도체 8대 공정", "C", "CMP & 세정 공정 (Cleaning & CMP)"
    # M : 금속배선 & 패키징 (Metal & Packaging)
    if any(k in t for k in ['금속공정', '금속 공정', '메탈 공정', 'salicide', '살리사이드', 'schottky', 'ohmic', '쇼트키', '오믹', '패키징', 'tsv', 'electro migration', 'em', 'sm 저항성']):
        return "반도체 8대 공정", "M", "금속배선 & 패키징 (Metal & Packaging)"
    # Y : 수율 & 공정제어 (Yield & PCM)
    if any(k in t for k in ['수율', 'yield', 'pcm', 'process control', 'process corner', 'shmoo plot', '상관성 분석', 'in-line monitoring', 'cmos process flow', '불량사례', '불랑사례', '불량 사례', '공정 margin']):
        return "반도체 8대 공정", "Y", "수율 & 공정제어 (Yield & PCM)"

    # 3. 반도체 소자 (Devices - Compact Codes)
    # DRAM
    if any(k in t for k in ['dram', 'ddr', 'lpddr']):
        return "반도체 소자", "DRAM", "DRAM 메모리"
    # NAND
    if any(k in t for k in ['nand', '낸드', 'ctf', 'slc', 'mlc', 'tlc', '플로팅게이트', 'flash']):
        return "반도체 소자", "NAND", "NAND Flash 메모리"
    # GAA
    if any(k in t for k in ['finfet', 'gaa', 'gate-all-around']):
        return "반도체 소자", "GAA", "3D 트랜지스터 (FinFET/GAA)"
    # SCE
    if any(k in t for k in ['short channel', 'dibl', 'punch through', 'velocity saturation', 'gidl', 'hot carrier', 'subthreshold swing', 'ss 특성', 'channel이 짧아지면']):
        return "반도체 소자", "SCE", "단채널 효과 & 신뢰성"
    # PWR
    if any(k in t for k in ['전력반도체', 'power device', 'sic', 'gan', '화합물', 'pmic', 'cis', 'ccd', 't-con', 'ddi']):
        return "반도체 소자", "PWR", "전력반도체 & 특수소자"
    # MOS
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
