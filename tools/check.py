"""Offline pre-publication checks, including stale HTML and broken subpath links."""
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
import tempfile
from urllib.parse import urlsplit, unquote
from xml.etree import ElementTree

import render
from snapshot import AREAS, OUTPUT, PLACES, SNAPSHOT

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.refs = []
        self.h1 = 0
        self.lang = None
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, f'Duplicate ID: {a["id"]}'
            self.ids.add(a['id'])
        if tag == 'html':
            self.lang = a.get('lang')
        if tag == 'h1':
            self.h1 += 1
        self.refs.extend(a[k] for k in ('src', 'href') if k in a)
        if tag in ('script', 'img', 'link') and ('src' in a or 'href' in a):
            assert not urlsplit(a.get('src', a.get('href', ''))).netloc, 'External asset'

def check_content():
    assert set(PLACES) == {'bobingen', 'augsburg'}
    cutoff = date.fromisoformat(SNAPSHOT['as_of'])
    for city, place in PLACES.items():
        items = place['updates']
        dates = [date.fromisoformat(row['date']) for row in items]
        assert 1 <= len(items) <= 3 and dates == sorted(dates, reverse=True), city
        assert len({r['id'] for r in items}) == len(items)
        assert max(dates) <= cutoff, city
        assert len({r['source']['url'] for r in items}) == len(items)
        expected = {'city', 'region', 'state', 'federal', 'europe'}
        if city == 'bobingen':
            expected.add('district')
        assert {r['id'] for r in place['levels']} == expected
        for level in place['levels']:
            for action in level.get('activities', []):
                if action.get('date'):
                    assert date.fromisoformat(action['date']) <= cutoff, action['title']
                    assert action.get('status') and action.get('sources'), action['title']
            if not level.get('members'):
                continue
            names = {m['name'] for m in level['members']}
            for action in level.get('activities', []):
                votes = action.get('votes', [])
                assert all(v['name'] in names and
                           (v.get('source_row', 0) > 1 or
                            (v.get('source_record') and v.get('voter_id'))) for v in votes)
                assert len({v['name'] for v in votes}) == len(votes)
    regions = AREAS['districts']
    assert {r['number'] for r in regions} == {f'{n:02d}' for n in range(1, 43)}
    assert len(regions) == 42 and len({r['name'] for r in regions}) == 42
    assert sum(r['constituency'] == 'east' for r in regions) == 24
    assert all(r['constituency'] in AREAS['constituencies'] for r in regions)

def check_output():
    pages = {p: Page(p) for p in OUTPUT.glob('*.html')}
    expected_pages = {name for city in PLACES for name in (render.home(city), render.representation(city), f'sources-{city}.html')}
    assert {p.name for p in pages} == expected_pages, 'Unexpected or missing published page'
    for path, page in pages.items():
        assert page.lang == 'en' and page.h1 == 1, path.name
        for ref in page.refs:
            url = urlsplit(ref)
            if url.scheme:
                assert url.scheme == 'https' and url.hostname, (path.name, ref)
                continue
            assert not url.netloc and not url.path.startswith('/'), (path.name, ref)
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            assert OUTPUT in target.parents and target.is_file(), (path.name, ref)
            if url.fragment and target in pages:
                assert unquote(url.fragment) in pages[target].ids, (path.name, ref)
    for city in PLACES:
        for suffix in ('.svg', '-story.svg'):
            ElementTree.parse(OUTPUT / 'assets' / (city + suffix))
    assert (OUTPUT / '.nojekyll').exists()
    # Catch data changes that were never compiled into docs/ before publishing.
    with tempfile.TemporaryDirectory() as temp:
        render.OUTPUT = Path(temp)
        (render.OUTPUT / 'assets').mkdir()
        try:
            render.render()
            for expected in render.OUTPUT.rglob('*'):
                if expected.is_file():
                    relative = expected.relative_to(render.OUTPUT)
                    assert expected.read_bytes() == (OUTPUT / relative).read_bytes(), (
                        str(relative) + ' is stale. Run python3 tools/render.py.')
        finally:
            render.OUTPUT = OUTPUT
    print(f'{len(pages)} current pages; references, local targets, maps and district mappings checked.')

if __name__ == '__main__':
    check_content()
    check_output()
