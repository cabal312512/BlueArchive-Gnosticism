import json

fpath = '02_corpus/ba-data-jp/DB/ScenarioScriptExcelTable1.json'
with open(fpath, 'r', encoding='utf-8') as f:
    d = json.load(f)

datalist = d.get('DataList', [])
for idx, row in enumerate(datalist):
    if '史上最年少での就任' in row.get('TextJp', ''):
        print(f"Match found at index {idx}:")
        start = max(0, idx - 10)
        end = min(len(datalist), idx + 12)
        for i in range(start, end):
            r = datalist[i]
            prefix = ">> " if i == idx else "   "
            gid = r.get('GroupId')
            kr = r.get('ScriptKr', '').replace('\n', ' ')
            jp = r.get('TextJp', '').replace('\n', ' ')
            print(f"{prefix}[{i}] GID={gid} | KR={kr} | JP={jp}")
