import json

with open('02_corpus/ba-data-jp/DB/ScenarioModeExcelTable.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

modes = d['DataList']
print(f"Total scenario modes: {len(modes)}")

by_type = {}
for m in modes:
    mtype = m.get('ModeType')
    vol = m.get('VolumeId')
    disp_vol = m.get('DisplayVolumeId')
    chap = m.get('ChapterId')
    ep = m.get('EpisodeId')
    key = (mtype, disp_vol, vol, chap)
    by_type.setdefault(key, []).append(ep)

print("\nAll Volumes & Chapters in ScenarioModeExcelTable:")
for (mtype, disp_vol, vol, chap), eps in sorted(by_type.items()):
    print(f"  ModeType={mtype:<16} DispVol={disp_vol:<3} Vol={vol:<3} Chap={chap:<3} | Episodes: {len(eps)} (min={min(eps)}, max={max(eps)})")
