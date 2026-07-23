import urllib.request
import re
import os

os.makedirs('images', exist_ok=True)

cookie_processor = urllib.request.HTTPCookieProcessor()
opener = urllib.request.build_opener(cookie_processor)
opener.addheaders = [
    ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'),
    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'),
    ('Referer', 'https://www.backyardoasispoolsga.com/')
]

pages = [
    'https://www.backyardoasispoolsga.com/',
    'https://www.backyardoasispoolsga.com/gallery',
    'https://www.backyardoasispoolsga.com/icf-pool-construction'
]

img_urls = []
for p in pages:
    try:
        html = opener.open(p).read().decode('utf-8', errors='ignore')
        matches = re.findall(r'https://lh3\.googleusercontent\.com/sitesv/[^\s"\'><\\]+', html)
        print(f"Found {len(matches)} matches on {p}")
        img_urls.extend(matches)
    except Exception as e:
        print('Error reading page:', p, e)

unique_urls = list(dict.fromkeys(img_urls))
print(f'Total {len(unique_urls)} unique image URLs found.')

successful_images = []
for idx, url in enumerate(unique_urls):
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.backyardoasispoolsga.com/'
        })
        filename = f'images/site_image_{idx+1}.jpg'
        with opener.open(req) as resp, open(filename, 'wb') as f:
            data = resp.read()
            if len(data) > 1000: # Only keep valid non-empty files
                f.write(data)
                successful_images.append(filename)
                print(f'Successfully saved {filename} ({len(data)} bytes)')
    except Exception as e:
        print(f'Failed downloading image {idx+1}: {e}')

print(f'Finished downloading {len(successful_images)} images!')
