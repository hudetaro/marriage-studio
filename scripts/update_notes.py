# noteのRSSから新着3本を notes.json に書き出す（GitHub Actions から毎日実行）
import json, re, urllib.request, xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

RSS = 'https://note.com/kekkon_fuku/rss'
req = urllib.request.Request(RSS, headers={'User-Agent': 'Mozilla/5.0 (notes-updater)'})
xml = urllib.request.urlopen(req, timeout=30).read()
root = ET.fromstring(xml)
ns = {'media': 'http://search.yahoo.com/mrss/'}
items = []
for it in root.iter('item'):
    title = re.sub(r'【婚活】\s*$', '', it.findtext('title', '')).strip()
    thumb = it.findtext('media:thumbnail', '', ns) or ''
    thumb = re.sub(r'\?width=\d+', '?width=400', thumb)
    d = parsedate_to_datetime(it.findtext('pubDate'))
    items.append({'title': title, 'url': it.findtext('link'), 'thumb': thumb, 'date': d.strftime('%Y.%m.%d')})
    if len(items) == 3:
        break
if len(items) == 3:
    with open('notes.json', 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=1)
    print('updated', [i['date'] for i in items])
