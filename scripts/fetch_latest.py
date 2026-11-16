"""Discover the latest published Chinese lesson and persist it through the API."""
import json
from datetime import datetime
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

BASE = 'https://chinese-scrapper-1011934259293.asia-northeast3.run.app'
ROOT = 'https://www.chosun.com'
SEOUL = ZoneInfo('Asia/Seoul')


def read(url, payload=None, timeout=60):
    request = Request(url, data=json.dumps(payload).encode() if payload is not None else None,
                      headers={'Content-Type': 'application/json', 'User-Agent': 'ChineseLessonScheduler/1.0'})
    with urlopen(request, timeout=timeout) as response:
        return json.load(response)


def latest(items, today):
    candidates = []
    for item in items:
        path = item.get('canonical_url', '')
        url = ROOT + path if path.startswith('/') else path
        parsed = urlsplit(url)
        if parsed.scheme != 'https' or parsed.hostname != 'www.chosun.com' or parsed.username:
            continue
        if not parsed.path.startswith('/national/nie/chinese/'):
            continue
        published = datetime.fromisoformat(item['display_date'].replace('Z', '+00:00')).astimezone(SEOUL)
        if published.date() <= today:
            candidates.append((published, url))
    if not candidates:
        raise ValueError('No published Chinese lesson discovered')
    return max(candidates)[1]


def main():
    # Fail before expensive scraping if persistence is unavailable.
    read(BASE + '/readyz')
    query = {'includeSections': '/national/nie/chinese', 'includeContentTypes': 'story',
             'excludeContentTypes': 'gallery, video', 'size': 20, 'offset': 0}
    feed = read(ROOT + '/pf/api/v3/content/fetch/story-feed?' + urlencode({
        'query': json.dumps(query), '_website': 'chosun'}))
    url = latest(feed['content_elements'], datetime.now(SEOUL).date())
    result = read(BASE + '/api/scrape', {'url': url}, timeout=300)
    if not result.get('id') or not result.get('expression'):
        raise ValueError('Saved lesson does not contain an expression')
    print('Latest Chinese expression saved:', result['id'])


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        # Never print provider response bodies or connection details.
        raise SystemExit('Latest Chinese lesson fetch failed: ' + type(exc).__name__) from None
