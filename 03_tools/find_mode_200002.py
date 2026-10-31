import json

with open('02_corpus/ba-data-jp/DB/ScenarioModeExcelTable.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for r in d['DataList']:
    front = r.get('FrontScenarioGroupId', [])
    back = r.get('BackScenarioGroupId', [])
    if 200002 in front or 200002 in back or r.get('DisplayVolumeId') == '0' or r.get('VolumeId') == 6 or r.get('ModeType') == 'SpecialOperation':
        if 200002 in front or 200002 in back:
            print("MATCH 200002:")
            print(f"  ModeId={r.get('ModeId')}, ModeType={r.get('ModeType')}, SubType={r.get('SubType')}, DisplayVolumeId={r.get('DisplayVolumeId')}, VolumeId={r.get('VolumeId')}, ChapterId={r.get('ChapterId')}, EpisodeId={r.get('EpisodeId')}")
            print(f"  Front={front}, Back={back}")
