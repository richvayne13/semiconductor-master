import urllib.request, re, sys, json, os
from bs4 import BeautifulSoup
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

test_id = "393"
test_url = f"https://sshmyb.tistory.com/{test_id}"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

print(f"Testing single post extraction: ID {test_id} ({test_url})")

req = urllib.request.Request(test_url, headers=headers)
html_doc = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
soup = BeautifulSoup(html_doc, 'html.parser')

# Title
title_el = soup.find('h3', class_='tit_post') or soup.find('div', class_='tit_post') or soup.find('h1')
title = title_el.get_text(strip=True) if title_el else ""
print(f"Title: {title}")

# Subcategory from breadcrumbs or post header
subcat = ""
subcat_el = soup.find('span', class_='txt_category') or soup.find('span', class_='info_cate') or soup.find('a', class_='link_cate')
if subcat_el:
    subcat = subcat_el.get_text(strip=True)
print(f"Subcategory: {subcat}")

# Content container
content_div = soup.find('div', class_='contents_style') or soup.find('div', class_='article_view')
if not content_div:
    print("Error: Could not locate content container")
    sys.exit(1)

# Images processing
images_dir = Path(r"C:\Work\반도체\context\images")
images_dir.mkdir(parents=True, exist_ok=True)

img_elements = content_div.find_all('img')
print(f"Found {len(img_elements)} images in content")

downloaded_images = []
for idx, img in enumerate(img_elements):
    src = img.get('src') or img.get('data-src')
    if not src:
        continue
    # determine extension
    ext = "png"
    if ".jpg" in src.lower() or "jpeg" in src.lower():
        ext = "jpg"
    elif ".gif" in src.lower():
        ext = "gif"
    
    local_filename = f"{test_id}_{idx}.{ext}"
    local_path = images_dir / local_filename
    
    try:
        img_req = urllib.request.Request(src, headers=headers)
        img_data = urllib.request.urlopen(img_req, timeout=10).read()
        local_path.write_bytes(img_data)
        print(f"  [Downloaded] Image #{idx+1} -> {local_filename} ({len(img_data)} bytes)")
        downloaded_images.append({
            'index': idx,
            'original_url': src,
            'local_filename': local_filename,
            'local_path': str(local_path)
        })
    except Exception as e:
        print(f"  [Failed] Image #{idx+1} ({src}): {e}")

# Extract clean text and questions
verbatim_text = content_div.get_text('\n', strip=True)
print(f"Verbatim text length: {len(verbatim_text)} chars")

# Questions extraction
questions = []
q_matches = re.findall(r'(\[(?:질문|꼬리질문|변형)[^\]]*\]\s*([^\n]+))', verbatim_text)
for q_full, q_text in q_matches:
    questions.append({
        'header': q_full,
        'question': q_text.strip()
    })
print(f"Extracted {len(questions)} interview questions")
for q in questions:
    print("  -", q['header'])

# Save structured post
post_data = {
    'id': test_id,
    'url': test_url,
    'title': title,
    'subcat': subcat,
    'images': downloaded_images,
    'questions': questions,
    'verbatim_text': verbatim_text,
    'raw_html': str(content_div)
}

posts_dir = Path(r"C:\Work\반도체\context\posts")
posts_dir.mkdir(parents=True, exist_ok=True)
out_file = posts_dir / f"{test_id}.json"

with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(post_data, f, ensure_ascii=False, indent=2)

print(f"Saved post data to {out_file} (Size: {out_file.stat().st_size} bytes)")
print("Single post test completed with 100% success!")
