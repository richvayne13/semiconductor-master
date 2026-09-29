import urllib.request, re, sys, json, os, time
from bs4 import BeautifulSoup
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

catalog_path = Path(r"C:\Work\반도체\context\post_catalog.json")
posts_dir = Path(r"C:\Work\반도체\context\posts")
images_dir = Path(r"C:\Work\반도체\context\images")

posts_dir.mkdir(parents=True, exist_ok=True)
images_dir.mkdir(parents=True, exist_ok=True)

with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

print(f"Loaded {len(catalog)} posts from catalog.")

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def process_post(item):
    post_id = item['id']
    post_url = item['url']
    out_file = posts_dir / f"{post_id}.json"
    
    # Skip if already downloaded and has content
    if out_file.exists() and out_file.stat().st_size > 1000:
        try:
            with open(out_file, 'r', encoding='utf-8') as check_fp:
                cached = json.load(check_fp)
                if cached.get('verbatim_text'):
                    return {'id': post_id, 'status': 'cached', 'images': len(cached.get('images', []))}
        except Exception:
            pass

    for attempt in range(3):
        try:
            req = urllib.request.Request(post_url, headers=headers)
            html_doc = urllib.request.urlopen(req, timeout=12).read().decode('utf-8')
            soup = BeautifulSoup(html_doc, 'html.parser')

            # Title
            title_el = soup.find('h3', class_='tit_post') or soup.find('div', class_='tit_post') or soup.find('h1')
            title = title_el.get_text(strip=True) if title_el else item['title']

            # Subcategory
            subcat = item.get('subcat', '')
            subcat_el = soup.find('span', class_='txt_category') or soup.find('span', class_='info_cate') or soup.find('a', class_='link_cate')
            if subcat_el and not subcat:
                subcat = subcat_el.get_text(strip=True)

            # Content container
            content_div = soup.find('div', class_='contents_style') or soup.find('div', class_='article_view')
            if not content_div:
                content_div = soup.find('div', class_='entry-content') or soup.find('div', class_='area_view')

            if not content_div:
                return {'id': post_id, 'status': 'error', 'msg': 'No content div found'}

            # Images
            downloaded_images = []
            img_elements = content_div.find_all('img')
            for idx, img in enumerate(img_elements):
                src = img.get('src') or img.get('data-src')
                if not src:
                    continue
                # skip external ads/trackers
                if 'daumcdn.net/tistory_admin' in src or 'adservice' in src or 'google' in src:
                    continue

                ext = "png"
                if ".jpg" in src.lower() or "jpeg" in src.lower():
                    ext = "jpg"
                elif ".gif" in src.lower():
                    ext = "gif"

                local_filename = f"{post_id}_{idx}.{ext}"
                local_path = images_dir / local_filename

                if not local_path.exists() or local_path.stat().st_size == 0:
                    try:
                        img_req = urllib.request.Request(src, headers=headers)
                        img_data = urllib.request.urlopen(img_req, timeout=10).read()
                        local_path.write_bytes(img_data)
                    except Exception as ie:
                        pass

                downloaded_images.append({
                    'index': idx,
                    'original_url': src,
                    'local_filename': local_filename,
                    'local_path': str(local_path),
                    'exists': local_path.exists() and local_path.stat().st_size > 0
                })

            # Verbatim text
            verbatim_text = content_div.get_text('\n', strip=True)

            # Questions extraction
            questions = []
            q_matches = re.findall(r'(\[(?:질문|꼬리질문|변형)[^\]]*\]\s*([^\n]+))', verbatim_text)
            for q_full, q_text in q_matches:
                questions.append({
                    'header': q_full,
                    'question': q_text.strip()
                })

            post_data = {
                'id': post_id,
                'url': post_url,
                'title': title,
                'subcat': subcat,
                'images': downloaded_images,
                'questions': questions,
                'verbatim_text': verbatim_text,
                'raw_html': str(content_div)
            }

            with open(out_file, 'w', encoding='utf-8') as f:
                json.dump(post_data, f, ensure_ascii=False, indent=2)

            return {'id': post_id, 'status': 'success', 'images': len(downloaded_images), 'title': title}

        except Exception as e:
            if attempt == 2:
                return {'id': post_id, 'status': 'error', 'msg': str(e)}
            time.sleep(1.0)

print("Starting multithreaded crawling with 6 workers...")
results = []
start_t = time.time()

with ThreadPoolExecutor(max_workers=6) as executor:
    future_to_post = {executor.submit(process_post, item): item for item in catalog}
    completed_count = 0
    for future in as_completed(future_to_post):
        completed_count += 1
        res = future.result()
        results.append(res)
        if completed_count % 10 == 0 or completed_count == len(catalog):
            print(f"Progress: [{completed_count}/{len(catalog)}] posts processed ({(time.time()-start_t):.1f}s)")

success_cnt = sum(1 for r in results if r['status'] in ('success', 'cached'))
cached_cnt = sum(1 for r in results if r['status'] == 'cached')
error_cnt = sum(1 for r in results if r['status'] == 'error')
total_images = sum(r.get('images', 0) for r in results)

print(f"\n==========================================")
print(f"Crawling Summary:")
print(f"Total Posts: {len(catalog)}")
print(f"Successfully Crawled: {success_cnt} (Cached: {cached_cnt})")
print(f"Errors: {error_cnt}")
print(f"Total Images Saved: {total_images}")
print(f"Elapsed Time: {(time.time()-start_t):.1f}s")
print(f"==========================================")
