import json, glob

for fpath in glob.glob('02_corpus/ba-data-jp/Excel/Localize*.json'):
    with open(fpath, 'r', encoding='utf-8') as f:
        d = json.load(f)
        for r in d.get('DataList', []):
            jp = r.get('Jp', '')
            if 'デカグラマトン' in jp or '花咲く' in jp or 'アーモンド' in jp:
                print(f"FOUND in {fpath}: {r}")
