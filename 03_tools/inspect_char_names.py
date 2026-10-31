import json

with open('02_corpus/ba-data-jp/DB/ScenarioCharacterNameExcelTable.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print(f"Total character names: {len(d['DataList'])}")
for r in d['DataList'][:15]:
    print(r)
