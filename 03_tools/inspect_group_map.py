import json, glob

group_to_info = {}

# 1. Main / Special / Sub / Mini / Prologue
with open('02_corpus/ba-data-jp/DB/ScenarioModeExcelTable.json', 'r', encoding='utf-8') as f:
    d = json.load(f)
for r in d['DataList']:
    mtype = r.get('ModeType', '')
    subtype = r.get('SubType', '')
    vol = r.get('VolumeId', 0)
    disp_vol = r.get('DisplayVolumeId', '')
    chap = r.get('ChapterId', 0)
    ep = r.get('EpisodeId', 0)
    
    vol_str = f"Vol.{vol}"
    if disp_vol:
        vol_str = f"Part2_Vol.{disp_vol}"
    if mtype == 'SpecialOperation':
        vol_str = f"EX_Decagrammaton_Vol.{vol}"
    elif mtype == 'Prologue':
        vol_str = f"Prologue_{subtype}"
    elif mtype == 'Sub':
        vol_str = f"Sub_{vol}"
    elif mtype == 'Mini':
        vol_str = f"Mini_{vol}"

    for gid in r.get('FrontScenarioGroupId', []):
        group_to_info[gid] = {'category': mtype, 'volume': vol_str, 'chapter': f"Ch.{chap}", 'episode': f"Ep.{ep}"}
    for gid in r.get('BackScenarioGroupId', []):
        group_to_info[gid] = {'category': mtype, 'volume': vol_str, 'chapter': f"Ch.{chap}", 'episode': f"Ep.{ep}_Back"}

print(f"Mapped {len(group_to_info)} groups from ScenarioModeExcelTable.")

# 2. Event Scenarios
with open('02_corpus/ba-data-jp/DB/EventContentScenarioExcelTable.json', 'r', encoding='utf-8') as f:
    d = json.load(f)
for r in d['DataList']:
    eid = r.get('EventContentId', 0)
    order = r.get('Order', 0)
    gid = r.get('ReplayDisplayGroup', 0)
    # let's see fields
    # we will inspect fields of EventContentScenario
