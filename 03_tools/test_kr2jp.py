import json

with open('02_corpus/ba-data-jp/DB/ScenarioCharacterNameExcelTable.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

kr2jp = {}
for r in d['DataList']:
    nkr = r.get('NameKR', '').strip()
    njp = r.get('NameJP', '').strip()
    if nkr and njp:
        kr2jp[nkr] = njp

print(f"Loaded {len(kr2jp)} unique KR->JP speaker mappings.")
test_names = ['아유무', '린', '모모카', '검은 양복', '무명의 사제', '총학생회장']
for n in test_names:
    print(f"  {n} -> {kr2jp.get(n, '(NOT FOUND)')}")
