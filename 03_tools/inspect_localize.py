import json

with open('02_corpus/ba-data-jp/Excel/LocalizeScenarioExcelTable.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print(f"Total LocalizeScenario rows: {len(d['DataList'])}")
for r in d['DataList'][:10]:
    print(r)
