"""One-time, content-preserving publication formatting of the author's manuscript."""
raise SystemExit('第34轮一次性格式化脚本已封存；当前论文已有作者新修改，禁止从旧存档重建覆盖。')
from pathlib import Path
import hashlib
import json
import re
import sqlite3

ROOT=Path(__file__).resolve().parents[1]
ORIGINAL=ROOT/'08_review_queue/archive/user_manuscript_2026-11-01_original.md'
EXPECTED='0d57f889a03e49723529c2493ac9451ea00bb72906f876083aa2eb0d0e7cbaaf'
assert hashlib.sha256(ORIGINAL.read_bytes()).hexdigest()==EXPECTED
raw=ORIGINAL.read_text(encoding='utf-8')
body,notes=raw.split('## 注释与游戏引文定位',1)
definitions=dict(re.findall(r'^\[\^([^\]]+)\]:\s*(.*)$',notes,re.M))
changes=[]
def normalize(s):
    pairs=[
      ('《约翰秘传》（Apocryphon of John, ', 'Apocryphon of John（'),
      ('《约翰秘传》（Apocryphon of John）','Apocryphon of John'),
      ('《三部论》（*Tripartite Tractate*）','Tripartite Tractate'),
      ('《三部论》（Tripartite Tractate）','Tripartite Tractate'),
      ('“第九处（The Ninth）”','“The Ninth”'),
      ('索菲亚（Sophia）','Sophia'),('光之洞见（Luminous Epinoia）','Luminous Epinoia'),
      ('神性火花（Divine Spark）','Divine Spark'),('神圣火花（Divine Spark）','Divine Spark'),
      ('执政官（Archons）','Archons'),('命运”（Heimarmene）','Heimarmene”'),
      ('力量（Power / Dynamis）','Power / Dynamis'),('灵（Pneuma）','Pneuma'),
      ('光环（Halo）','Halo'),('属魂（Psychic）','Psychic'),
      ('属灵（Pneumatic/Divine Spark）','Pneumatic / Divine Spark'),
      ('受造界心智（Psyche）','Psyche'),('至高界（Pleroma）','Pleroma'),
      ('十字神名（Decagrammaton）','Decagrammaton'),('四字神名（Tetragrammaton）','Tetragrammaton'),
      ('卡巴拉（Kabbalah）','Kabbalah'),('生命之树（Tree of Life）','Tree of Life'),
      ('《传道书》','Ecclesiastes'),('《约翰福音》','John'),('《旧约》','Old Testament'),('圣经','Bible'),
      ('《约翰秘传》','Apocryphon of John'),('《三部论》','Tripartite Tractate'),
      ('诺斯底主义','Gnostic'),('诺斯底','Gnostic'),('灵知主义','Gnostic'),('灵知传统','Gnostic传统'),
      ('索菲亚','Sophia'),('亚当','Adam'),('执政官','Archons'),('造物主','Demiurge'),
      ('神性火花','Divine Spark'),('神圣火花','Divine Spark'),('光之碎片','Light Fragments'),
      ('十字神名','Decagrammaton'),('生命之树','Tree of Life'),('十个原质','十个Sefirot'),
      ('米迦勒','Michael'),('加百列','Gabriel'),('乌列尔','Uriel'),('巴力','Baal'),
      ('彼列','Belial'),('别西卜','Beelzebub'),
    ]
    for old,new in pairs:s=s.replace(old,new)
    # The author's follow-up permits correcting Gnostic/Gnosis by context.
    # All manuscript occurrences name the religious tradition, not gnosis itself.
    s=re.sub(r'(?<![A-Za-z])Gnostic(?![A-Za-z])','Gnosticism',s)
    return s

expected_body=normalize(body)
oldurl='file:///F:/Blue%20Archive%20Project%20Gnosis/06_comparative_analysis/gnostic_atlas/index.html'
expected_body=expected_body.replace(oldurl,'[图谱](06_comparative_analysis/gnostic_atlas/index.html)')
s=expected_body
# Existing author heading lacks Markdown syntax; wording is untouched.
s=re.sub(r'^十二、', '## 十二、',s,flags=re.M)
# Consistent subordinate numbering: 2.1, 2.2, etc. Main headings remain author's Chinese numbers.
section=0
out=[]
for line in s.splitlines():
    if line.startswith('## ') and re.match(r'## [一二三四五六七八九十]+、',line):section+=1
    line=re.sub(r'^### (\d+)\. ',lambda m:f'### {section}.{m[1]} ',line)
    out.append(line.rstrip())
s='\n'.join(out)+'\n'
# Two inline primary quotations become blockquotes; preserve every original word/punctuation.
for quotation in ['“用度量、节期与时序束缚所有人，使其全都在锁链之中充当顺从的工具”',
                  '“Power will descend upon every person, for without it no one could stand.”']:
    assert s.count(quotation)==1
    s=s.replace(quotation,'\n\n> '+quotation+'\n\n')
# Collapse excess blank lines only. Abstract label becomes a normal heading.
s=re.sub(r'^\*\*摘要\*\*[^\S\n]*$','## 摘要',s,flags=re.M)
s=re.sub(r'(?<!\n)\n(?=#{2,3} )','\n\n',s)
s=re.sub(r'^(#{1,3} [^\n]+)\n(?!\n)',r'\1\n\n',s,flags=re.M)
s=re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+','\n\n',s)
glossary_line='[术语说明：Gnosticism名词与文献](GNOSTIC_GLOSSARY.md)'
s=re.sub(r'(^\*\*关键词\*\*[^\n]*\n)',r'\1\n'+glossary_line+'\n',s,count=1,flags=re.M)

# Move the technical bibliography item to the private-detail companion, keeping public edition info.
technical_line=next(l for l in s.splitlines() if l.startswith('5. 本项目固定日文游戏语料快照'))
s=s.replace(technical_line,'5. 游戏引文采用日文文本，附中文工作译文。原始文本及技术索引见[引文索引](01_sources/paper_citation_index.md)。')
definitions={k:normalize(v) for k,v in definitions.items()}
definitions['P4']=definitions['P4'].replace('原典重点校核见本项目04_evidence/gnostic_primary_cards.md GN-04／GN-05。','')
definitions['T1']='《伊甸条约篇》第4章章标题：为被遗忘诸神而作的Kyrie。'
definitions['T2']='《伊甸条约篇》第4章第23、24话标题：为少女们而作的Kyrie（1）、（2）。'

c=sqlite3.connect(f'file:{(ROOT/"02_corpus/story_index.db").as_posix()}?mode=ro',uri=True);c.row_factory=sqlite3.Row
speech_kinds=('named_dialogue','choice_text','unnamed_text','quiz_question_and_choices','hidden_label_text')
def speech(r):return r['text_kind'] in speech_kinds
groups={}
def group_rows(g):
    if g not in groups:groups[g]=[dict(x) for x in c.execute('select * from dialogues where group_id=? order by group_row',(g,))]
    return groups[g]
def human_location(row):
    g=row['group_id'];rs=group_rows(g)
    # Human-readable scene anchors for replay segments without a verified numbered episode alias.
    if g==10052195:
        a=186009;label='特殊作战·Decagrammaton篇第3章，爱丽丝、凯伊与柔和的声音交谈的场景（从“终于抵达这里了呢”起）'
    elif g==10052050:
        a=182923;label='特殊作战·Decagrammaton篇第3章，凯伊与奥尔交谈的场景（从奥尔认出“钥匙”起）'
    elif g==10021016:
        a=165642;label='最终篇，普雷纳帕特斯世界的回忆：无名祭司接触白子的场景（从祭司谈色彩与死之神接触起）'
    elif g==10021022:
        a=165824;label='最终篇，普雷纳帕特斯世界的回忆：祭司与老师对话的场景（从祭司谈色彩接触箱之主起）'
    else:
        a=rs[0]['id'];v=row['volume'];ch=row['chapter'].replace('章','章');ep=row['episode'].replace('話','话')
        if v.startswith('最終篇'):label=f'主线第1部·最终篇，{ch}{ep}'
        elif 'プロローグ' in v:label=('主线第2部·序章' if '第2部' in v else '主线第1部·序章')+f'，{ch}{ep}'
        elif v.startswith('特殊作戦'):label=f'特殊作战·Decagrammaton篇，{ch}{ep}'
        else:label=v.replace('第3篇_エデン条約編','主线第1部·第3篇《伊甸条约篇》').replace('第1篇_対策委員会編','主线第1部·第1篇《对策委员会篇》')+f'，{ch}{ep}'
    ordinal=sum(speech(x) and x['id']>=a and x['group_row']<=row['group_row'] for x in rs)
    return f'{label}，第{ordinal}条对白。',ordinal,a

# Single numeric sequence, first occurrence order, GitHub-native superscript footnotes.
used=list(dict.fromkeys(re.findall(r'\[\^([^\]]+)\]',s)))
number={k:i+1 for i,k in enumerate(used)}
assert all(k in definitions for k in used)
technical=[];public=[]
for key in used:
    n=number[key]
    if key.startswith('G'):
        row=dict(c.execute('select * from dialogues where id=?',(int(key[1:]),)).fetchone())
        loc,ordinal,anchor=human_location(row)
        technical.append({'number':n,'old_key':key,'public_location':loc,'ordinal':ordinal,'count_from_id':anchor,**row})
        value=loc
    else:value=definitions[key]
    public.append(f'[^{n}]: {value}')
s=re.sub(r'\[\^([^\]]+)\]',lambda m:f'[^{number[m[1]]}]',s)
s+='\n## 注释\n\n台词序号按所注明场景中的对白、选项与叙述顺序计数，不计标题、场景名和演出指令；一条发言内的换行不另计。\n\n'+'\n\n'.join(public)+'\n'

def canonical(t):
    t=t.split('## 原典、版本与资料')[0]
    t=t.replace(glossary_line,'')
    t=re.sub(r'\[\^[^\]]+\]','',t)
    t=re.sub(r'^### \d+(?:\.\d+)?\.?(?=\s)','###',t,flags=re.M)
    t=t.replace('## 摘要','摘要')
    return re.sub(r'[\s#>*_`]+','',t)
assert canonical(s)==canonical(expected_body),'Protected author text differs beyond permitted terminology/formatting.'
assert not re.search(r'(?:file:///|[A-Z]:[\\/]|DataList|schema v2|\[\^[GPT]\d)',s)

target=ROOT/'gnostic_correspondence_full.md'
target.write_text(s,encoding='utf-8')
index=['# 论文引文技术索引','','[返回论文](../gnostic_correspondence_full.md)','','本文件保存论文数字注释与原始语料的对应，供复核使用。论文正文以作者2026-11-01重写稿为准。', '',
       '原始数据提交：`3428d2a0943bdfe7d6453adfcb06676509972b02`。台词顺序计数规则与论文注释一致；未核定话数的重编片段采用可识别场景起句定位。','',
       '## 原始技术说明','',technical_line,'','## 游戏引文','',
       '| 论文注释 | 阅读位置 | 原索引 | 源表 | DataList行 | 场景内原始行 |','| --- | --- | --- | --- | --- | --- |']
for x in technical:index.append(f'| {x["number"]} | {x["public_location"]} | `{x["old_key"]}` / Group `{x["group_id"]}` | `{x["source_file"]}` | {x["source_row"]} | {x["group_row"]} |')
index+=['','## 原稿注释原貌','','以下保留作者稿原有技术定位；数字对应以本页上表为准。','']
index += [f'- `{k}`：{v}' for k,v in dict(re.findall(r'^\[\^([^\]]+)\]:\s*(.*)$',notes,re.M)).items()]
(ROOT/'01_sources/paper_citation_index.md').write_text('\n'.join(index)+'\n',encoding='utf-8')
(ROOT/'01_sources/paper_citation_index.json').write_text(json.dumps({'author_original_sha256':EXPECTED,'footnote_map':number,'game_records':technical,'original_technical_paragraph':technical_line,'counted_text_kinds':speech_kinds},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
validation={'author_original_sha256':EXPECTED,'protected_body_preserved_after_authorized_normalization':True,'footnotes':len(used),'game_notes':len(technical),'unused_original_notes':[k for k in definitions if k not in used],'bibliography_technical_item_relocated':True,'local_absolute_paths_in_paper':False}
(ROOT/'01_sources/paper_format_validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(validation,ensure_ascii=False))
