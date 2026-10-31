import json, os, glob

print("Scanning ba-data-jp for all ScenarioScript tables:")
for folder in ['DB', 'Excel']:
    files = glob.glob(f"02_corpus/ba-data-jp/{folder}/ScenarioScript*.json")
    for f in sorted(files):
        sz = os.path.getsize(f) / (1024 * 1024)
        with open(f, 'r', encoding='utf-8') as fp:
            d = json.load(fp)
            cnt = len(d.get('DataList', []))
        print(f"  {f}: {cnt} rows, {sz:.2f} MB")
