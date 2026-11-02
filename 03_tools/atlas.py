"""Inspect or export the standalone atlas without regenerating or overwriting it."""
from pathlib import Path
import argparse
import json
import re

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = ROOT / 'gnostic_atlas.html'


def read_embedded(path=DEFAULT, element_id='atlas-data'):
    text = Path(path).read_text(encoding='utf-8')
    match = re.search(r'<script id="' + re.escape(element_id) + r'"[^>]*>(.*?)</script>', text, re.S)
    if not match:
        raise ValueError(f'Missing embedded data: {element_id}')
    return json.loads(match[1])


def validate(path=DEFAULT):
    text = Path(path).read_text(encoding='utf-8')
    data = read_embedded(path)
    translations = read_embedded(path, 'atlas-languages')
    assert set(translations) == {'en', 'ja', 'ko'}
    original_strings = set()

    def walk(value):
        if isinstance(value, str) and re.search(r'[\u3400-\u9fff]', value):
            original_strings.add(value)
        elif isinstance(value, list):
            for item in value:
                walk(item)
        elif isinstance(value, dict):
            for item in value.values():
                walk(item)

    walk(data)
    for language, mapping in translations.items():
        assert original_strings <= mapping.keys(), f'Incomplete language: {language}'
        assert all(isinstance(v, str) and v.strip() for v in mapping.values())
        assert not any(re.search(r'ZX\d{3}', v) for v in mapping.values()), language
    ids = {n['id'] for n in data['nodes']}
    assert len(ids) == len(data['nodes'])
    for edge in data['edges']:
        assert edge['from_id'] in ids and edge['to_id'] in ids
        assert edge['source'] in data['sources']
    assert not re.search(r'<(?:script|img)\b[^>]*\bsrc\s*=|<link\b[^>]*\bhref\s*=', text, re.I)
    assert not re.search(r'\b(?:fetch|XMLHttpRequest)\s*\(', text)
    return {'systems': len(data['systems']), 'nodes': len(ids), 'edges': len(data['edges']),
            'translated_strings_per_language': len(original_strings), 'languages': ['zh', 'en', 'ja', 'ko'],
            'bytes': Path(path).stat().st_size, 'self_contained': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--html', type=Path, default=DEFAULT)
    parser.add_argument('--export', type=Path, help='Export original Chinese data to a new JSON file')
    args = parser.parse_args()
    result = validate(args.html)
    if args.export:
        with args.export.open('x', encoding='utf-8') as handle:
            json.dump(read_embedded(args.html), handle, ensure_ascii=False, indent=2)
            handle.write('\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
