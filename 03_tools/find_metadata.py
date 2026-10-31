import json, os, glob

print("Checking scenario mapping tables in ba-data-jp/DB:")
for f in sorted(glob.glob("02_corpus/ba-data-jp/DB/*Scenario*.json")):
    with open(f, 'r', encoding='utf-8') as fp:
        d = json.load(fp)
        cnt = len(d.get('DataList', []))
        first_row = d.get('DataList', [{}])[0] if cnt > 0 else {}
        keys = list(first_row.keys())[:8]
    print(f"  {os.path.basename(f)}: {cnt} rows, keys={keys}")
