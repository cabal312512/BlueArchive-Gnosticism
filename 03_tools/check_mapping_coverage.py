import json, glob

# Collect all GroupIds
all_gids = set()
for fpath in glob.glob('02_corpus/ba-data-jp/DB/ScenarioScriptExcelTable*.json'):
    with open(fpath, 'r', encoding='utf-8') as f:
        d = json.load(f)
        for r in d.get('DataList', []):
            gid = r.get('GroupId')
            if gid:
                all_gids.add(gid)

print(f"Total unique GroupIds: {len(all_gids)}")

mapped_gids = {}

# 1. ScenarioMode (Main, Prologue, SpecialOperation, Sub, Mini)
with open('02_corpus/ba-data-jp/DB/ScenarioModeExcelTable.json', 'r', encoding='utf-8') as f:
    d = json.load(f)
for r in d['DataList']:
    mtype = r.get('ModeType')
    subtype = r.get('SubType', '')
    vol = r.get('VolumeId')
    disp_vol = r.get('DisplayVolumeId')
    chap = r.get('ChapterId')
    ep = r.get('EpisodeId')
    info = {
        'type': mtype,
        'series': subtype,
        'volume': disp_vol if disp_vol else vol,
        'chapter': chap,
        'episode': ep
    }
    for gid in r.get('FrontScenarioGroupId', []):
        mapped_gids[gid] = ('ScenarioMode', info)
    for gid in r.get('BackScenarioGroupId', []):
        mapped_gids[gid] = ('ScenarioMode_Back', info)

# 2. EventContentScenario
with open('02_corpus/ba-data-jp/DB/EventContentScenarioExcelTable.json', 'r', encoding='utf-8') as f:
    d = json.load(f)
for r in d['DataList']:
    eid = r.get('EventContentId')
    order = r.get('Order')
    for gid in r.get('ScenarioGroupId', []):
        mapped_gids[gid] = ('Event', {'event_id': eid, 'order': order})

# 3. AcademyFavorSchedule (Bond)
with open('02_corpus/ba-data-jp/DB/AcademyFavorScheduleExcelTable.json', 'r', encoding='utf-8') as f:
    d = json.load(f)
for r in d['DataList']:
    cid = r.get('CharacterId')
    rank = r.get('FavorRank')
    gid = r.get('ScenarioSriptGroupId')
    if gid:
        mapped_gids[gid] = ('Favor', {'character_id': cid, 'rank': rank})

# 4. Check unmapped
unmapped = all_gids - set(mapped_gids.keys())
print(f"Mapped GroupIds: {len(set(mapped_gids.keys()) & all_gids)} / {len(all_gids)}")
print(f"Unmapped GroupIds: {len(unmapped)}")
if unmapped:
    sample = sorted(list(unmapped))[:10]
    print(f"Sample unmapped: {sample}")
