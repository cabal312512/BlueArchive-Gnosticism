import json

with open('02_corpus/ba-data-jp/DB/ScenarioModeExcelTable.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print(f"Total rows in ScenarioModeExcelTable: {len(d['DataList'])}")
for r in d['DataList'][:15]:
    print(r)

print("\nDistinct ModeTypes:")
print(set(r.get('ModeType') for r in d['DataList']))

print("\nDistinct VolumeIds:")
print(set(r.get('VolumeId') for r in d['DataList']))

print("\nDistinct DisplayVolumeIds:")
print(set(r.get('DisplayVolumeId') for r in d['DataList']))
