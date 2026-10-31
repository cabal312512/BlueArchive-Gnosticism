"""Build a self-contained, source-separated Gnostic cosmology reference."""
from pathlib import Path
import json, re, csv, copy

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'06_comparative_analysis'/'gnostic_atlas'
OUT.mkdir(parents=True,exist_ok=True)
SOURCES={
 'AJ':{'title':'Apocryphon of John · four-manuscript Synopsis','url':'https://www.rexresearch1.com/DeadSeaScrolls/ApocryphonJohnSynopsisWaldstein.pdf','edition':'Waldstein / Wisse 1995; NHC II,1; III,1; IV,1; BG 8502,2'},
 'AJW':{'title':'Apocryphon of John · composite English translation','url':'https://www.earlychristianwritings.com/text/apocryphonjohn.html','edition':'Frederik Wisse; composite translation, not a fifth manuscript'},
 'IR':{'title':'Irenaeus · Against Heresies I','url':'https://www.newadvent.org/fathers/0103.htm','edition':'Roberts / Rambaut, Ante-Nicene Fathers 1; hostile external report'},
 'HA':{'title':'Hypostasis of the Archons','url':'https://www.earlychristianwritings.com/text/archons.html','edition':'NHC II,4; Bullard / Layton'},
 'OW':{'title':'On the Origin of the World','url':'https://www.earlychristianwritings.com/text/originworld.html','edition':'NHC II,5; Bethge / Layton and collaborators'},
 'TT':{'title':'Tripartite Tractate','url':'https://www.earlychristianwritings.com/text/tripartite.html','edition':'NHC I,5; Attridge / Mueller'},
 'VE':{'title':'A Valentinian Exposition','url':'https://www.earlychristianwritings.com/text/valentinian.html','edition':'NHC XI,2; Turner; mirror has an erroneous Zostrianos subheading'},
 'TP':{'title':'Trimorphic Protennoia','url':'https://www.earlychristianwritings.com/text/trimorphic.html','edition':'NHC XIII,1; Turner'},
 'EG':{'title':'Holy Book of the Great Invisible Spirit','url':'https://www.earlychristianwritings.com/text/greatspirit.html','edition':'NHC III,2 / IV,2; Böhlig / Wisse; Coptic Gospel of the Egyptians'},
 'EUG':{'title':'Eugnostos the Blessed','url':'https://www.earlychristianwritings.com/text/eugnostos.html','edition':'NHC III,3 / V,1; Parrott'},
 'SJC':{'title':'Sophia of Jesus Christ','url':'https://www.earlychristianwritings.com/text/sophia.html','edition':'NHC III,4 / BG 8502,3; Parrott'},
 'ALL':{'title':'Allogenes','url':'https://www.earlychristianwritings.com/text/allogenes.html','edition':'NHC XI,3; Turner / Wintermute'},
 'ZOS':{'title':'Zostrianos','url':'https://www.earlychristianwritings.com/text/zostrianos.html','edition':'NHC VIII,1; Sieber; major lacunae retained'},
 'PS':{'title':'Pistis Sophia','url':'https://iapsop.com/ssoc/1921__mead___pistis_sophia.pdf','edition':'Askew Codex; G. R. S. Mead, revised 1921; scheme pp. l–li is editorial'},
 'FL':{'title':'Ptolemy · Letter to Flora','url':'https://www.earlychristianwritings.com/text/flora.html','edition':'Preserved in Epiphanius, Panarion 33.3–7'},
 'HI':{'title':'Hippolytus · Refutation VII','url':'https://www.newadvent.org/fathers/050107.htm','edition':'External report, VII.20–27 in standard numbering; New Advent VII.8–15 headings'},
 'TUR':{'title':'Turner · Sethian Gnosticism and the Platonic Tradition','url':'https://www.pulaval.com/livres/sethian-gnosticism-and-the-platonic-tradition-bcnh-etudes-6','edition':'2001; consulted 2006 second printing; especially pp. 57–92, 499–588'},
 'GT':{'title':'Gospel of Truth','url':'https://www.earlychristianwritings.com/text/gospeltruth.html','edition':'NHC I,3 / XII,2; Attridge / MacRae'},
}
systems=[]; nodes=[]
def system(sid,title,tradition,subtitle,source,flow,notes):
    d=dict(id=sid,title=title,tradition=tradition,subtitle=subtitle,source=source,flow=flow,notes=notes);systems.append(d);return sid
def node(sid,key,name,tier,kind,role,parent='',aliases='',source=None,locator='',notes='',detail=False):
    d=dict(id=sid+'-'+key,system=sid,key=key,name=name,tier=tier,kind=kind,role=role,parent=(sid+'-'+parent if parent else ''),aliases=[a.strip() for a in aliases.split('|') if a.strip()],source=source or next(s['source'] for s in systems if s['id']==sid),locator=locator,notes=notes,detail=detail)
    nodes.append(d);return d
def row(sid,tier,parent,items,kind='神圣存在',source=None,locator='',detail=False):
    for key,name,role in items:node(sid,key,name,tier,kind,role,parent,source=source,locator=locator,detail=detail)

aj=system('aj','Apocryphon of John','Sethian','主视图 · long recension · NHC II / IV','AJ',[
 ('本源与显现','不可言说的Invisible Spirit通过其Thought显现；Barbelo及神圣属性构成上界展开。'),
 ('上界秩序','Autogenes与Four Luminaries组织神圣领域；Adamas、Seth及其seed分别有归属。'),
 ('失衡与世界','Sophia独自生育Yaldabaoth；后者生成下层权能、模仿上界组织世界。'),
 ('人的构成','Archons造人的身体；母之力量进入Adam，人的认知超过造物者，引发压制。'),
 ('救赎与归返','Luminous Epinoia帮助认识来源；Spirit与Counterfeit Spirit构成不同方向；长本末尾Pronoia以Five Seals唤醒。')],
 ['主视图是项目所用、结构较完整的long recension，不表示Gnosticism存在唯一正统。','Pleroma是神圣整体／领域；Aeon既可表示存在也可表示领域，不是统一的官阶。','十二个随侍Aeons是Four Luminaries各三项的组列，不是所有神圣存在的总人口。'])
node(aj,'monad','Invisible Spirit',0,'本源','自足、不可命名的最高本源；其他存在的来源',aliases='Monad|Father of All|Virgin Spirit',locator='NHC II,1 2,26–4,19')
node(aj,'barbelo','Barbelo',1,'神圣存在／领域','本源的First Thought、形象及万有之胎；Mother–Father','monad','Pronoia|First Thought|Mother–Father|Ennoia',locator='4,19–6,10')
row(aj,2,'barbelo',[('foreknow','Foreknowledge','与Barbelo同立的神圣属性'),('incorrupt','Incorruptibility','不朽性'),('life','Eternal Life','永恒生命'),('truth','Truth','长本中完成Pentad的第四项')],kind='属性／Aeon',locator='4,26–6,10; Synopsis 9–13')
node(aj,'autogenes','Autogenes–Christ',3,'神圣存在','Barbelo与Invisible Spirit所显现的独生之光，组织神圣领域','barbelo','Self-Generated|Christ|Only-Begotten',locator='6,10–7,30')
row(aj,3,'autogenes',[('nous','Nous','与Christ同工的Mind'),('will','Will','神圣意志'),('word','Word','与Will、Mind共同作用')],kind='同工／属性',locator='6,20–7,30',detail=True)
lights=[('harmozel','Harmozel','Armozel','Grace|Truth|Form'),('oroiael','Oroiael','Oriel|Oriael','Conception|Perception|Memory'),('daveithe','Daveithe','Daveithai|Daveithae','Understanding|Love|Idea'),('eleleth','Eleleth','','Perfection|Peace|Wisdom')]
for key,name,alias,attrs in lights:
    node(aj,key,name,4,'Luminary／Aeon','Four Luminaries之一；神圣群体的居所与组织者','autogenes',alias,locator='7,30–9,24; Synopsis 19–23')
    for k,a in enumerate(attrs.split('|')):node(aj,key+str(k),a,5,'随侍Aeon',name+'所随侍三项之一；四组共十二项',key,locator='7,30–8,28',detail=True)
row(aj,6,'harmozel',[('adamas','Pigera-Adamas','Perfect Man；上界人之原型，不是下界泥土身体')],locator='8,28–9,11')
node(aj,'seth','Seth',6,'神圣人祖','Adamas之子，安置在第二Luminary领域','oroiael',locator='9,11–14')
node(aj,'seed','Seed of Seth',6,'群体','在第三Luminary领域；与saints关联','daveithe',aliases='Immovable Race',locator='9,14–17')
node(aj,'repentant','Repentant Souls',6,'群体','先不认识Pleroma、后来悔悟的灵魂，归第四Luminary领域','eleleth',locator='9,17–24')
node(aj,'sophia','Sophia',7,'Aeon','独自行动导致不如预期的生育，继而悔悟补救','eleleth','Sophia of the Epinoia',locator='9,25–10,19; 13,13–14,13',notes='叙事接在十二Aeons之后；Wisdom与Sophia有词义关联，不能因此把所有使用Wisdom的名号无条件合并。归于Eleleth一侧的理解亦见TP与Turner；不是其明确编号为第十二的句子。')
node(aj,'yald','Yaldabaoth',8,'Chief Archon／Demiurge','携母之力量而生，误认自己为唯一神，建立下层秩序','sophia','Yaltabaoth|Ialdabaoth|Saklas|Samael|Chief Begetter',locator='10,1–13,13')
node(aj,'twelve','Twelve Authorities',9,'下层群体','十二权能；七位配置于天，五位配置于深渊','yald',locator='10,26–11,22')
names='Athoth|Harmas|Kalila-Oumbri|Yabel|Adonaiou|Cain|Abel|Abrisene|Yobel|Armoupieel|Melceir-Adonein|Belias'.split('|')
for i,name in enumerate(names):node(aj,'authority'+str(i),name,9,'Authority','十二权能名单第'+str(i+1)+'项','twelve',aliases='Sabaoth' if i==4 else '',locator='10,26–11,22',detail=True)
node(aj,'seven','Seven Powers',10,'下层群体','七个兽面权能及对应属性；与前面的十二名单分开保存','yald',locator='11,23–12,25')
for i,(name,role) in enumerate(zip('Athoth|Eloaiou|Astaphaios|Yao|Sabaoth|Adonin|Sabbede'.split('|'),['羊面；Goodness','驴面；Foreknowledge','鬣狗面；Divinity','七头蛇面；Lordship','龙／蛇面；Kingdom','猴面；Envy','火焰面；Understanding'])):node(aj,'power'+str(i),name,10,'Power',role,'seven',locator='11,23–12,25',detail=True)
node(aj,'body','Body-Making Angels',11,'群体','分工制作人的身体与感官；详见名号表附录','yald',locator='14,13–19,14',notes='365是文本给出的总数，不代表正文逐一列出365个名字。')
node(aj,'adam','Adam',12,'下界人','Archons造形，母之力量被吹入后获得生命与更高认知','body',locator='19,15–20,8',notes='与上界Pigera-Adamas分开。')
node(aj,'epinoia','Luminous Epinoia',12,'帮助者／内在启示','由上界派出，帮助Adam、修正母亲缺陷；隐藏于人之中','barbelo','Epinoia of Light|Life',locator='20,9–29',notes='与Pronoia、Sophia存在关联，不能将所有相关称号在所有文本中直接视为完全同一实体。')
row(aj,13,'adam',[('eve','Eve','与生命、认识及Epinoia显现相关的下界女性'),('earthseth','Earthly Seth','Adam在认识上界形象后所生；与上界原型关联'),('spirit','Spirit of Life','上界援助与认识的力量'),('counterfeit','Counterfeit Spirit','下层控制的仿冒Spirit，与欲望、遗忘相连'),('fate','Heimarmene','由下层权能施行的命运束缚')],kind='人／力量／机制',locator='20,29–28,32')
node(aj,'return','Awakening / Five Seals',14,'救赎过程','Pronoia进入黑暗、唤醒受束缚者，施以Five Seals；回归神圣来源','epinoia',locator='30,11–31,25',notes='这是长本结尾，不直接作为短本共有段落。')

short=copy.deepcopy(next(s for s in systems if s['id']=='aj'));short.update(id='ajshort',title='Apocryphon of John · short',subtitle='short recension · NHC III / BG',notes=['与长本共享主结构，不能把短本当成另一个完全不同宗教。','Barbelo的Pentad配列、下层名字与数量措辞、帮助者段落均须逐栏看；长本身体名录及末尾Pronoia长段不完整同见于短本。','BG与III也有差别；共同图只画共有骨架，具体差异在版本表。']);systems.append(short)
for n in list(nodes):
    if n['system']=='aj' and not n['detail'] and n['key'] not in ['truth','body','return']:
        d=copy.deepcopy(n);d['system']='ajshort';d['id']=d['id'].replace('aj-','ajshort-',1);d['parent']=d['parent'].replace('aj-','ajshort-',1);d['locator']='NHC III,1 / BG 8502,2; Synopsis对应栏';nodes.append(d)
node('ajshort','return','Revelation / Return',14,'救赎过程','由Spirit与认识帮助归返；不添加长本末尾完整颂歌','epinoia',locator='短本末段，Synopsis 77–85')

v=system('val','Valentinian · Ptolemaic','Valentinian','主对照 · Irenaeus I.1–8','IR',[
 ('Pleroma展开','Bythos–Sige、Nous–Aletheia、Logos–Zoe、Anthropos–Ecclesia构成Ogdoad；再出Decad与Duodecad，共三十。'),('失衡与分界','Sophia追求认识Father而失衡；Horos使其恢复，排出其Enthymesis／passion。'),('下界形成','外在Achamoth经Christ与Soter的不同帮助而形成；产生psychic Demiurge及神性seed。'),('人的构成','material、psychic、pneumatic是不同构成／类型；神性seed并不等同一位三十名单中的Aeon。'),('最终归返','Achamoth与Soter结合，pneumatic seed进入Pleroma，psychic得中间安息，matter被消除。')],['三十＝8＋10＋12；Sophia是Duodecad末项，十二不是总数。','内部Sophia与外在Achamoth不能在此版本抹成一个位置。','Demiurge不是通用等同Devil的称号；不同Valentinian材料对其评价有差异。'])
base=[('bythos','Bythos','最高深渊／Father','Proarche|Propator'),('sige','Sige','与Bythos同在的Silence','Ennoia|Charis'),('nous','Nous','理解Father的Monogenes','Monogenes'),('aletheia','Aletheia','Truth，与Nous配对',''),('logos','Logos','Word，与Zoe配对',''),('zoe','Zoe','Life，与Logos配对',''),('anthropos','Anthropos','上界Man，与Ecclesia配对',''),('ecclesia','Ecclesia','上界Assembly，与Anthropos配对','')]
for i,(key,name,role,alias) in enumerate(base):node(v,key,name,i//2,'Ogdoad · Aeon',role,'' if i<2 else ['bythos','bythos','nous','nous','logos','logos'][i-2],alias,locator='I.1.1')
decad='Bythius|Mixis|Ageratos|Henosis|Autophyes|Hedone|Acinetos|Syncrasis|Monogenes|Macaria'.split('|')
duodecad='Paracletus|Pistis|Patricos|Elpis|Metricos|Agape|Ainos|Synesis|Ecclesiasticus|Macariotes|Theletos|Sophia'.split('|')
for group,names,parent,tier in [('Decad',decad,'logos',4),('Duodecad',duodecad,'anthropos',5)]:
    for i,name in enumerate(names):node(v,group.lower()+str(i),name,tier,group+' · Aeon','配对：'+names[i+1 if i%2==0 else i-1]+'；'+group+'第'+str(i+1)+'项',parent,locator='I.1.2–3',detail=True)
node(v,'sophia','Sophia',6,'Pleroma内Aeon','Duodecad最末、与Theletos配对；失衡后由Horos恢复','anthropos',locator='I.2.2–4',notes='与上方完整名单中的Sophia是同一位，此卡为叙事展开，不另计入三十。')
row(v,6,'nous',[('horos','Horos','限定、维持并分离；也称Stauros等'),('christ','Christ','与Holy Spirit共同使Pleroma稳定'),('holyspirit','Holy Spirit','教导感谢、平等与安息')],locator='I.2.4–6')
node(v,'soter','Soter / Jesus',7,'Pleroma共同成果','全体Aeons共同贡献所成，参与Achamoth完善与最终结合','christ','Common Fruit|Paraclete',locator='I.2.6; I.4; I.7')
node(v,'achamoth','Achamoth',8,'Pleroma外Sophia相关存在','被排出的Enthymesis及passion；居中间处，孕育Demiurge及seed','sophia','Lower Sophia|Enthymesis',locator='I.4–5',notes='不是Pleroma内Sophia整个人被永久驱逐的简单版本。')
node(v,'demiurge','Demiurge',9,'psychic造物者','不知上界而受Achamoth间接推动，建七天与世界','achamoth','Metropator|Apator|Hebdomas',locator='I.5.1–4')
row(v,10,'demiurge',[('heavens','Seven Heavens','下界宇宙组织'),('cosmocrator','Cosmocrator / Devil','与Demiurge区别的邪恶统治者')],kind='领域／统治者',locator='I.5.2–4')
row(v,11,'achamoth',[('pneumatic','Pneumatic Seed','来自Achamoth的spiritual成分，借下界生长'),('psychic','Psychic','介于spirit与matter的soul成分／类型'),('hylic','Hylic / Material','由passion而来的物质成分')],kind='人的构成／类型',locator='I.5–6')
node(v,'restoration','Restoration',12,'最终归返','pneumatic seed与天使配偶进入Pleroma；psychic居中间处，matter消除','soter',locator='I.7.1')

h=system('ha','Hypostasis of the Archons','Sethian-related','NHC II,4','HA',[('上界与下层','Incorruptibility与Pistis Sophia位于Archons之上；低层Chief Ruler无知。'),('人的形成','Archons照水中形象造Adam；Spirit与Eve的启示使其苏醒。'),('反抗与援助','Norea拒绝统治者，呼求援助，Eleleth解释她的root。'),('秩序内部分化','Sabaoth悔悟而被Sophia、Zoe提升；Yaldabaoth嫉妒而产生Death。'),('终局','True Man与Spirit of Truth揭示并解除下层统治。')],['此处Sabaoth的提升不能套到所有同名版本。','Eleleth既是Four Luminaries之一，也是Norea的揭示者。'])
row(h,0,'',[('incorrupt','Incorruptibility','高于混沌权能的神圣领域／力量'),('spirit','Invisible Spirit','Four Luminaries所侍立的本源')],kind='本源／上界',locator='86,20–87,20; 93,8–94,2')
node(h,'sophia','Pistis Sophia',1,'神圣存在','下层生成与秩序纠正的上界参与者','incorrupt',locator='94,4–95,13')
node(h,'zoe','Zoe',2,'Sophia之女','揭斥并制约Yaldabaoth，教导被提升的Sabaoth','sophia',locator='95,1–96,3')
node(h,'yald','Yaldabaoth',3,'Chief Ruler','无知统治者，被更高力量揭穿','sophia','Samael|Sakla',locator='94,4–95,13')
node(h,'archons','Archons',4,'群体','造下界人的形体并试图支配','yald',locator='87,23–93,7')
node(h,'sabaoth','Sabaoth',4,'悔悟的下层后裔','谴责父亲与matter，获提升至第七天并受Zoe教导','yald',locator='95,13–96,3')
node(h,'death','Death',5,'毁坏力量','Yaldabaoth嫉妒后出现，与其后裔作用于下界','yald',locator='96,3–17')
row(h,6,'archons',[('adam','Adam','下界人，接受来自上界的生命与启示'),('eve','Eve / Spiritual Woman','唤醒Adam；与被统治者追逐的形体有别'),('seth','Seth','人类神圣谱系的相关祖先'),('norea','Norea','不受Archons支配，呼求上界揭示其root'),('noah','Noah','洪水叙事中的人物')],kind='人／神圣女性',locator='87,23–93,7')
node(h,'eleleth','Eleleth',7,'Luminary／帮助者','救援Norea，解释其不朽来源与下层生成','spirit',locator='93,8–94,2')
node(h,'return','True Man / Spirit of Truth',8,'终局揭示','末期显明真理、解除Archons的统治','incorrupt',locator='96,17–97,23')

o=system('ow','On the Origin of the World','Sethian-related','NHC II,5','OW',[('起源','文本反对把Chaos当作绝对开端，以高界的shadow说明低层来源。'),('低层生成','Pistis Sophia、shadow、matter与Yaldabaoth形成相连，Yaldabaoth组织七天。'),('两种统治','Sabaoth悔悟获提升并建设上界范型的形象；父亲产生嫉妒及毁坏力量。'),('人的生成','上界形象与多次造人过程并置；Adam、Eve、Eros、植物与动物起源各有说明。'),('终局','揭露统治者无知，世界及Chaos的旧结构被消除。')],['七位名单包括首位Yaldabaoth；不要改写成Yaldabaoth之外另七位。','这里的Pronoia、Sophia也被用于下层权能的女性名号，不能凭同名就与上界同一。'])
row(o,0,'',[('light','Immortal Realm','先于Chaos的神圣来源'),('pistis','Pistis Sophia','意志、显现与纠正下界的关键存在')],kind='上界',locator='97,24–99,20')
node(o,'shadow','Shadow / Matter / Chaos',1,'生成阶段','低层的shadow凝成matter与Chaos；不是最高原点','light',locator='98,11–100,13')
node(o,'yald','Yaldabaoth',2,'Prime Parent','七位低层权能之首，组织各天与其众多从属','shadow','Samael',locator='100,1–102,25')
for i,(name,female) in enumerate(zip(['Yaldabaoth','Yao','Sabaoth','Adonaios','Elaios','Oraios','Astaphaios'],['Pronoia / Sambathas','Lordship','Deity','Kingship','Jealousy','Wealth','Sophia'])):node(o,'seven'+str(i),name,3,'Seven Forces','相应女性名号：'+female,'yald',locator='101,24–102,25',detail=True)
node(o,'sabaoth','Sabaoth',4,'悔悟与提升','受Pistis提升并受Zoe教导，居高于Chaos诸神的位置','pistis',locator='103,32–106,19')
node(o,'zoe','Zoe',4,'教导者','Pistis之女，教导Sabaoth高界事物','pistis',locator='104,26–105,16')
row(o,5,'sabaoth',[('israel','Israel','Sabaoth所造firstborn，名义为见神之人'),('jesusimage','Jesus Christ · image','模仿更高Savior的形象，不可直接并为最高者'),('church','Assembly of Angels','数以万计的从属、cherubim、seraphim及诸语言的管理者')],locator='105,16–106,19')
row(o,6,'yald',[('death','Death','由嫉妒等作用产生的破坏力量'),('eros','Eros','与欲望、美和自然界生成相连')],kind='作用力',locator='106–109')
row(o,7,'light',[('adamlight','Adam of Light','高界形象，影响低层造人'),('adamearth','Earthly Adam','下层造形与生命参与的对象'),('eve','Eve','显明与生命的参与者')],kind='人之形态',locator='107–118')
node(o,'end','Consummation',8,'终局','下层旧秩序、Chaos及其力量不能永久维持','light',locator='125–127')

t=system('tt','Tripartite Tractate','Valentinian','NHC I,5','TT',[('神圣整体','Father、Son及Church共同解释神圣整体；不提供封闭的三十个名字表。'),('偏离','Logos试图超越共同秩序，产生不足的likenesses，随后转向与祈求。'),('修正与组织','Savior帮助Logos；Logos区分right／left并以Demiurge作手与口组织下界。'),('人类三分','pneumatic、psychic、hylic三类构成，随对Savior的反应呈现。'),('归返','救赎是整体的复归、结合及安息；三种构成结局不同。')],['承担偏离与补救核心叙事的是Logos，不可直接将原文名字改成Sophia。','Demiurge不知高界但被Logos用于安排，不是另一文本全部邪恶行为的自动复制。'])
row(t,0,'',[('father','Father','不可把握的神圣整体之根'),('son','Son','Father自我启示，与Father不可分'),('church','Church / Totalities','神圣Aeons的共同整体')],locator='I.1–5')
node(t,'aeons','Aeons',1,'开放群体','神圣展开，文本不封闭列为三十或十二个个体','father',locator='I.5')
node(t,'logos','Logos',2,'Aeon','偏离共同秩序后转向，成为下界的组织与修正者','aeons',locator='I.6–9')
node(t,'savior','Savior',3,'帮助者','回应祈求，使Logos得以认识并重新组织','son',locator='I.8–9')
row(t,4,'logos',[('right','Right / Psychic','由较好转向与thought所形成的秩序'),('left','Left / Hylic','由arrogant thought及likeness而来的不足秩序'),('spiritual','Spiritual Seed','救赎安排中的更高成分')],kind='秩序／构成',locator='I.9–12')
node(t,'demiurge','Demiurge',5,'造物安排者','被Logos用作手与口，组织并说出下界事物','right','Father|King|Judge|Law',locator='I.11–12')
row(t,6,'logos',[('man','Mankind','三种essential types，并非每人等于一个Aeon'),('pneumatic','Pneumatic','如light from light，立即回应Savior'),('psychic','Psychic','通过教导、faith与hope回应'),('hylic','Hylic','排斥揭示，走向消解')],kind='人类构成／类型',locator='II–III; sections 13–14')
node(t,'return','Restoration / Union',7,'归返','由Savior使整体复归与结合','savior',locator='III.15–16')

a=system('plat','Allogenes / Zostrianos','Platonizing Sethian','神圣层次与上升路径 · 两文本并列','ALL',[('最高原则','Invisible Spirit超越being与普通认知；Triple-Powered One连接最高原则与神圣展开。'),('真实存在领域','Barbelo Aeon分Kalyptos、Protophanes、Autogenes三重结构。'),('上升','从较低领域经认知、baptism或静观抵达Autogenes，再向Protophanes、Kalyptos及超越认知的来源推进。'),('人的位置','上升者改变认知与存在状态，不等于被分配为一个名单中的神。')],['这是两文本的对照骨架；Triple-Powered One的关系并不完全相同。','Allogenes偏静观，Zostrianos含更繁复的baptism及低层中介领域；具体出处逐卡区别。','不能把这里三重Barbelo直接倒写为AJ四抄本逐字共有的结构。'])
node(a,'spirit','Invisible Spirit',0,'超越本源','超越存在与知识对象',source='ALL',locator='XI,3 61–67')
node(a,'triple','Triple-Powered One',1,'超越力量','与Existence、Vitality、Mentality／Blessedness的三重展开有关','spirit',source='ALL',locator='XI,3 49–51; 58–61',notes='不同文本可视为最高原则之力量、其展开或通向Barbelo的中介；不是跨文本固定的一位次级神。')
node(a,'barbelo','Barbelo Aeon',2,'神圣整体／领域','真实存在领域的三重结构','triple',source='TUR',locator='pp. 531–556')
row(a,3,'barbelo',[('kalyptos','Kalyptos','隐藏、统一的最高相'),('protophanes','Protophanes','首次显现、noetic展开'),('autogenes','Autogenes','自生及较具体的神圣个体展开')],kind='Barbelo三重相',source='ALL',locator='XI,3 45–57; ZOS VIII,1 24–25')
row(a,4,'autogenes',[('lights','Four Luminaries','Autogenes领域的神圣光与秩序'),('perfect','Perfect Individuals','神圣个体，不是统一固定人数')],kind='神圣群体',source='ZOS',locator='VIII,1 24–25; 61–63')
row(a,5,'autogenes',[('repent','Repentance','Zostrianos较低的上升中介'),('sojourn','Sojourn','中介居留领域'),('copies','Aeonic Copies','真实领域的较低对应'),('atmosphere','Atmospheric Realm','较低宇宙与更高领域间的位置')],kind='中介领域',source='ZOS',locator='VIII,1 8–25')
row(a,6,'barbelo',[('youel','Youel','Allogenes的启示、教导者'),('allogenes','Allogenes','接受启示与静观上升的人'),('zostrianos','Zostrianos','经baptisms与教导上升的人'),('aphredon','Aphredon','Zostrianos中的启示者'),('authrounios','Authrounios','Zostrianos中的启示者')],kind='启示者／上升者',source='ALL',locator='ALL XI,3; ZOS VIII,1',detail=True)

e=system('eug','Eugnostos / Sophia of Jesus Christ','Related cosmologies','多重神圣Man与Sophia · 不同于三十名单','EUG',[('本源','Unbegotten Forefather与Self-Father展开神圣来源。'),('神圣谱系','Immortal Man、Son of Man、Savior及其不同Sophia配偶形成多重神圣结构。'),('众多展开','六对androgynous powers形成十二项，继而七十二、三百六十；下界时间对应其模型。'),('启示','Eugnostos以书信说明；Sophia of Jesus Christ以Savior向门徒的问答重述，并加入低层失衡与救援。')],['文本有多个Sophia名号，不是每次出现都必指AJ失误者。','同不朽领域内部可以有权能与关系差别，“都在Pleroma”不自动等于完全同一层级。','两文本高度相关但不同；SJC另有自己的叙事框架，不能只换书名。'])
node(e,'forefather','Unbegotten Forefather',0,'本源','无名、不可量、无始的来源',aliases='He-Who-Is|Father of the Universe',locator='EUG beginning')
node(e,'selffather','Self-Father',1,'自我显现','本源之自我观看与第一显现','forefather','Self-Begetter',locator='EUG first principles')
node(e,'immortal','Immortal Man',2,'神圣Man','神圣力量、divinity及kingdom的原型','selffather','Perfect Mind|First Man',locator='EUG Immortal Man section')
node(e,'sophia1','All-wise Begettress Sophia',2,'配偶／女性相','与Immortal Man相应的女性名号','immortal',locator='EUG Immortal Man section')
node(e,'sonman','Son of Man',3,'神圣后继','与Sophia配偶共同显出Savior之光','immortal','First Begetter',locator='EUG Son of Man section')
node(e,'savior','Savior',4,'神圣光／后继','与Pistis Sophia共同展开六对spiritual beings','sonman','Begetter of All',locator='EUG six androgynous beings')
node(e,'pistis','Pistis Sophia',4,'配偶／女性相','Savior相应的女性名号','savior','Sophia All-Begettress',locator='EUG six androgynous beings')
for i,(male,female) in enumerate(zip('Unbegotten|Self-begotten|Begetter|First Begetter|All-begetter|Arch-begetter'.split('|'),'All-wise Sophia|All-Mother Sophia|All-Begettress Sophia|First Begettress Sophia|Love Sophia|Pistis Sophia'.split('|'))):node(e,'pair'+str(i),male+' / '+female,5,'Androgynous Pair','六对之第'+str(i+1)+'对；十二名号不是宇宙全部神圣者','savior',locator='EUG six androgynous beings',detail=True)
row(e,6,'savior',[('72','Seventy-two Powers','十二powers的进一步展开'),('360','Three Hundred Sixty Powers','七十二各五项，形成时间模型'),('innumerable','Innumerable Angels','与hours、moments对应，非封闭人数')],kind='群体',locator='EUG numerical expansion')
node(e,'sjc','Savior as Revealer',7,'SJC启示角色','向门徒解释来源、生成与归返','savior',source='SJC',locator='SJC dialogue as a whole',notes='SJC包含Sophia及其drop、低层领域的叙述；不同于EUG单纯谱系信函。')

tp=system('tp','Trimorphic Protennoia','Sethian','NHC XIII,1','TP',[('本源之Thought','Protennoia自述为Father的Thought、Barbelo及普遍内在的生命。'),('世界与控制','Yaldabaoth窃取力量，制造模仿真实Aeons的下层秩序。'),('三重下降','Thought／Voice、Speech、Word展开启示，进入受束缚者之中。'),('救赎','唤醒自身成员，以Five Seals归于Light。')],['与AJ Pronoia末尾段有紧密关系，但不能简单删除文本差别。','神圣存在普遍内在的语言并不要求所有人分别对应一个专名Aeon。'])
node(tp,'father','Invisible Spirit',0,'本源','Protennoia所显现的来源',locator='XIII,1 35–39')
node(tp,'protennoia','Protennoia',1,'神圣Thought','以三重形式行动，遍在其成员之中','father','Barbelo|Thought of the Father',locator='35–50')
row(tp,2,'protennoia',[('voice','Thought / Voice','第一种启示表达'),('speech','Speech','第二种启示表达'),('word','Word / Logos','第三种启示表达')],kind='显现方式',locator='35–50')
node(tp,'yald','Yaldabaoth',3,'下层统治者','夺取力量并生成仿制秩序','protennoia','Saklas|Samael',locator='39–42')
node(tp,'epinoia','Epinoia of Light',3,'神圣力量','与Sophia、被夺取的力量及秩序修正相连','protennoia',locator='39–41')
node(tp,'members','Members / Sons of Light',4,'群体','下降启示所唤醒的对象','protennoia',locator='35–50')
node(tp,'seals','Five Seals',5,'救赎仪式','赋予knowledge并归于Light','members',locator='48–50')

eg=system('eg','Holy Book of the Great Invisible Spirit','Sethian','Coptic Gospel of the Egyptians · NHC III / IV','EG',[('神圣三重','Great Invisible Spirit、Father／Mother／Son、Barbelo与Doxomedon等描述宏大的神圣展开。'),('神圣人祖','Adamas、Great Seth及其seed与Four Luminaries形成关系。'),('低层生成','Sophia、Sakla和Nebruel及十二天使组织下层世界。'),('救赎与仪式','Great Seth关怀其seed，经启示、baptism与Five Seals使其受保护并归返。')],['不是Greek Gospel of the Egyptians，二者已在下载核验中分开。','此文本的Sakla与Nebruel相互配合；不得先将所有下层名号都合并为一个人。'])
node(eg,'spirit','Great Invisible Spirit',0,'本源','不可言说、无标记的光之来源',locator='III,2 40–42')
row(eg,1,'spirit',[('father','Father','三重神圣展开之一'),('mother','Mother / Barbelon','神圣Mother、virginal Barbelon'),('son','Son','三重神圣展开之一'),('doxomedon','Domedon Doxomedon','Aeon of aeons及诸powers之光')],locator='40–44')
row(eg,2,'son',[('autogenes','Autogenes','自生的神圣存在'),('triple','Thrice-Male Child','神圣三重child名号'),('youel','Youel','神圣揭示与child相关存在'),('esephech','Esephech','持有荣耀、child of child')],locator='44–50')
node(eg,'adamas','Adamas',3,'神圣Man','来自Light的上界人祖','autogenes',locator='49–50')
node(eg,'seth','Great Seth',4,'神圣人祖／救援者','为seed寻求居所并参与其救援','adamas',locator='50–65')
row(eg,5,'autogenes',[('lights','Four Luminaries','神圣居所与seed所处秩序'),('seed','Seed of Great Seth','救援及仪式所关涉的群体')],kind='领域／群体',locator='51–56')
node(eg,'sophia','Sophia',6,'神圣生成参与者','与低层出现的过程相关','lights',locator='56–58')
row(eg,7,'sophia',[('sakla','Sakla','下层大天使，与Nebruel共同生成'),('nebruel','Nebruel','与Sakla协作的great demon')],kind='下层生成者',locator='57–58')
node(eg,'twelve','Twelve Angels / Aeons',8,'下层群体','各自统辖其world；名单不同于AJ其他版本','sakla',locator='58–59')
egnames='Athoth|Harmas|Galila|Yobel|Adonaios / Sabaoth|Cain|Abel|Akiressina|Yubel|Harmoupiael|Archir-Adonin|Belias'.split('|')
for i,name in enumerate(egnames):node(eg,'ruler'+str(i),name,8,'Angel','十二名列第'+str(i+1)+'项','twelve',locator='58–59',detail=True)
row(eg,9,'seed',[('jesseus','Yesseus Mazareus Yessedekeus','living water及baptism相关'),('ministers','Gamaliel / Gabriel / Samblo / Abrasax','Four Luminaries的ministers'),('waters','Micheus / Michar / Mnesinous','truth之泉与水的服务者'),('seals','Five Seals','保护与启示的baptism仪式')],kind='仪式角色／过程',locator='64–67')

ps=system('ps','Pistis Sophia','Askew Codex','独立体系 · Mead 1921','PS',[('最高领域','Ineffable、First Mystery及其spaces，不能与AJ逐层直接对换。'),('Light-world','Treasury of Light、Region of Right及Midst，包含独立的管理者和引导者。'),('低层领域','Thirteenth Aeon及十二Aeons属于混合light／matter的宇宙区域；Aeon在此主要是领域。'),('Sophia经历','Pistis Sophia受Authades及其lion-faced power压迫，落入Chaos，悔悟并获Jesus救援。'),('人的归途','灵魂受命运及counterfeiting spirit等影响，经mysteries、净化与知识得以升向Light。')],['图层顺序参考Mead导论pp. l–li；它是译者的整理图，不冒充抄本原生目录。','Pistis Sophia文本内部不同部分亦有层次差别；不与AJ Sophia或Valentinian Achamoth直接合并。','Great Invisible是第十三Aeon的名号，不能凭名字同一就当最高Ineffable。'])
node(ps,'ineffable','Ineffable',0,'最高本源','超越Light-world诸层',locator='Mead intro pp. l–li; books I–II')
node(ps,'first','First Mystery',1,'最高Mystery','与最高spaces及Jesus启示身份相关','ineffable',locator='ch. 1–2; 84–96')
row(ps,2,'first',[('treasury','Treasury of Light','Light-world的重要领域'),('right','Region of the Right','较高Light-world区域'),('midst','Region of the Midst','与Right、Treasury区别的区域')],kind='领域',locator='intro pp. l–li; ch. 7–8; 84–96')
row(ps,3,'treasury',[('jeu','Jeu','组织与管理Light、baptism相关的神圣角色'),('melch','Melchizedek','light的接收与净化相关角色'),('virgin','Virgin of Light','与灵魂判定、净化及安排有关'),('sabaothgood','Sabaoth the Good','较高来源的名号，不与所有Sabaoth混同')],kind='Light-world角色',locator='books I–IV',detail=True)
node(ps,'thirteenth','Thirteenth Aeon',4,'混合宇宙领域','Pistis Sophia原先所在，低于其所追求的Light','midst',locator='ch. 29–31')
row(ps,5,'thirteenth',[('greatinvisible','Great Invisible','第十三Aeon的相关源头名号'),('24','Twenty-four Invisibles','Pistis Sophia的相关同伴／emanations'),('sophia','Pistis Sophia','渴望更高Light、受压迫并求援'),('authades','Authades / Self-Willed','压迫Sophia的Triple-Powered角色')],kind='领域内存在／群体',locator='ch. 30–31')
node(ps,'lion','Lion-faced Power',6,'压迫力量','Authades的emanation，以假light诱引并夺取力量','authades',locator='ch. 30–31')
row(ps,7,'thirteenth',[('twelve','Twelve Aeons','低层宇宙领域及其Archons'),('fate','Heimarmene / Sphere','灵魂受其安排的命运及星体领域'),('chaos','Chaos','Sophia受困、悔悟并获援之处'),('dark','Outer Darkness','惩罚及下层限制的区域')],kind='领域／机制',locator='intro pp. l–li; books I–IV')
node(ps,'jesus','Jesus / Savior',8,'救援与启示者','援救Sophia并向门徒传授mysteries','first','Aberamentho',locator='ch. 1–2; 30–82; 136ff')
node(ps,'mysteries','Mysteries / Ascent',9,'人的归途','通过mysteries、净化及认识脱离下层束缚','jesus',locator='books II–IV')

b=system('basil','Basilides · Irenaeus','Basilidian report','Irenaeus I.24 · 与Hippolytus分开','IR',[('上界','Unborn Father依次生Nous、Logos、Phronesis、Sophia与Dynamis。'),('世界','powers与angels层层产生365 heavens；最低层建立可见世界。'),('救赎','Christ作为Nous被派遣，使人通过认识脱离造物权能；报告含特殊受难替代叙述。')],['这是Irenaeus的外部转述，不是Basilides本人完整著作。','Abraxas在此与365相关；不直接等同其他Sethian文本的Abrasax。'])
prev=''
for i,(key,name,role) in enumerate([('father','Unborn Father','最高来源'),('nous','Nous','Father首生，Christ相关'),('logos','Logos','从Nous而生'),('phronesis','Phronesis','从Logos而生'),('sophia','Sophia / Dynamis','wisdom与power，生成下级powers'),('angels','Powers / Angels','逐层产生heavens'),('365','365 Heavens','层层生成的宇宙'),('abraxas','Abraxas','365数值相关的chief名号'),('world','Visible World','最低天的angels所组织'),('christ','Christ / Nous','由Father派出，传授解脱性knowledge')]):
    node(b,key,name,i,'存在／领域',role,prev,locator='I.24.3–7');prev=key
b2=system('basilhip','Basilides · Hippolytus','Basilidian report','Refutation VII · 另一种组织','HI',[('本源与种子','Non-Existent God、World Seed与三重Sonship解释宇宙。'),('两位Archons','Great Archon及其Son组织Ogdoad；另一Archon组织Hebdomad。'),('启示','Gospel经更高Sonship与诸Son向下传，统治者认识更高者。'),('恢复','各种成分归于适当本性与位置，Great Ignorance终止错误的越界欲求。')],['不是把Irenaeus名单换几个名字：两报告的整体生成方式不同。'])
row(b2,0,'',[('god','Non-Existent God','超越可称谓存在的最高来源'),('seed','World Seed / Panspermia','宇宙诸成分潜在的种子')],kind='本源／根源',locator='New Advent VII.8–10')
row(b2,1,'seed',[('son1','First Sonship','轻而立即上升'),('son2','Second Sonship','借Holy Spirit上升'),('son3','Third Sonship','留于seed，等待净化与回归')],kind='Sonship',locator='VII.10')
row(b2,2,'seed',[('great','Great Archon / Ogdoad','上层宇宙的统治者'),('second','Second Archon / Hebdomad','七天秩序的统治者'),('spirit','Holy Spirit / Limitary Spirit','连接并限定较高与宇宙层次')],kind='统治者／中介',locator='VII.10–14')
node(b2,'sons','Sons of the Archons',3,'教导者','比各自父亲更明智，传递更高启示','great',locator='VII.11–14')
node(b2,'gospel','Gospel / Restoration',4,'救赎过程','知识向下传递，各成分归其本性','son3',locator='VII.13–15')

irb=system('irbarb','Barbelo report · Irenaeus','Barbelo-related','Against Heresies I.29','IR',[('神圣展开','Father、Barbelos及其请求的powers构成展开。'),('Christ与Autogenes','报告中二者在叙事上有区别，不能按AJ直接同一。'),('人祖与Sophia','Adamas与Gnosis相关；Sophia／Prunicus产生Chief Ruler。'),('下界','Chief Ruler与Arrogance生成passions，误认为自己唯一。')],['这是与AJ近似却不相同的外部报告；四灯拼写及配列不同。'])
row(irb,0,'',[('father','Unnameable Father','最高来源'),('barbelo','Barbelos / Ennoia','Father自我揭示的对象')],locator='I.29.1')
row(irb,1,'barbelo',[('powers','Prognosis / Aphtharsia / Zoe Aionios','神圣属性'),('christ','Christ','受Father膏立之light'),('nous','Nous / Logos','同工及配对相关')],locator='I.29.1')
node(irb,'auto','Autogenes / Aletheia',2,'配对','由Ennoia与Logos发出，与Aletheia配对','barbelo',locator='I.29.2')
row(irb,3,'auto',[('lights','Armogenes / Raguel / David / Eleleth','四个Luminaries及相应powers'),('adamas','Adamas / Gnosis','上界人祖及认识的配对')],locator='I.29.2–3')
node(irb,'sophia','Sophia / Prunicus',4,'神圣存在','寻找配偶、向下行动后生Chief Ruler','auto',locator='I.29.4')
node(irb,'chief','Chief Ruler',5,'下界造物者','造下界并与Arrogance相合产生诸passions','sophia',locator='I.29.4')

op=system('ophite','Ophite-related report','Irenaeus report','Against Heresies I.30','IR',[('上界','First Man、Son of Man、First Woman及Christ构成最高关系。'),('Sophia与物质','Sophia／Prunicus向下进入waters而受束缚，随后脱离。'),('七位生成','Yaldabaoth到Astaphaeus是相继生成的七代，不是完全同级的七名下属。'),('人及救援','神性light进入人；Sophia持续对抗下层限制，最终回收light。')],['标题Ophites / Sethians是传述分类，不等同现代Sethian所有文本。','Sophia在此的上下关系不同于AJ及Valentinian。'])
row(op,0,'',[('first','First Man','Father of All及第一light'),('son','Son of Man','第二Man'),('woman','First Woman / Holy Spirit','高界女性，参与Christ生成'),('christ','Christ','上界第三male之light')],locator='I.30.1–2')
node(op,'sophia','Sophia / Prunicus',1,'下行神圣power','First Woman相关之light向下，生Yaldabaoth并援助人','woman',locator='I.30.3–4')
prev='sophia'
for i,name in enumerate(['Yaldabaoth','Iao','Sabaoth','Adoneus','Eloeus','Oreus','Astaphaeus']):node(op,'r'+str(i),name,2+i,'七代统治者','依次生成的第'+str(i+1)+'位',prev,locator='I.30.4–5');prev='r'+str(i)
row(op,9,'sophia',[('human','Adam / Eve / Seth / Norea','light与认识所保护的人类谱系'),('return','Gathering of Light','神性light最终聚合归返')],kind='人类／终局',locator='I.30.6–14')

vf=system('valvar','Valentinian variations','Valentinian','Valentinus / Secundus / Letter to Flora / Exposition','IR',[('Valentinus报告','最初四项为Arrhetus–Sige、Pater–Aletheia；不能当Ptolemaic名单只有一种。'),('Secundus报告','初始Ogdoad分right／left tetrads；失落者来自其fruits。'),('Exposition','Horos有分离、巩固、赋形、赋实体等四种作用；并非只两个作用。'),('Letter to Flora','最高Perfect God、居中的just Demiurge、evil adversary有清楚区分。')],['这些是同一大传统内部各材料的差异，不是全部历史分支的完整人物传记。'])
row(vf,0,'',[('valentinus','Valentinus · Arrhetus / Sige','不可言说与Silence的最初Dyad'),('pater','Pater / Aletheia','Valentinus报告中的第二Dyad'),('secundus','Secundus · Light / Darkness','初始Ogdoad的right／left tetrads')],kind='变体结构',locator='I.11.1–2')
node(vf,'horoi','Two Horoi',1,'边界powers','一者分Father与Aeons，一者分mother与Pleroma','valentinus',locator='I.11.1')
node(vf,'limit','Horos / Limit',2,'VE中的边界power','分离、巩固、赋形及赋实体四作用',source='VE',locator='XI,2 25–28')
node(vf,'perfect','Perfect God',3,'Flora中的最高神','善且不生的Father',source='FL',locator='Panarion 33.7')
node(vf,'demiurge','Demiurge',4,'Flora中的中间者','生成、较低、公正的造物者，与Devil区别','perfect',source='FL',locator='33.7')
node(vf,'devil','Devil / Adversary',5,'Flora中的邪恶对立者','低于Demiurge的毁坏与不义','demiurge',source='FL',locator='33.7')

gt=system('gt','Gospel of Truth','Valentinian-related','NHC I,3 · 以认识与Father为中心','GT',[('来源与遗忘','未认识Father引发fear、anguish与Error；不是必须配齐固定神谱。'),('启示','Jesus揭示Father，呼唤名字，使不知自身者认识自身来源。'),('归返','knowledge消除deficiency，复归Father的fullness与rest。')],['Error不是自动等同另一篇的Yaldabaoth；没有出现固定三十Aeon名单。'])
row(gt,0,'',[('father','Father','万有来源及安息之所'),('name','Name / Son','Father之名与Son的启示关系')],kind='本源／显现',locator='NHC I,3 16–18; 38–40')
node(gt,'error','Error',1,'不足的作用','不认识Father而来的混乱与塑形','father',locator='17–19')
node(gt,'jesus','Jesus / Savior',2,'启示者','以认识揭示Father，召唤属于他的名字','father',locator='18–24')
node(gt,'rest','Knowledge / Rest',3,'归返','不再受deficiency支配，安息于Father','jesus',locator='24–43')

GLOSSARY=[
 ('Monad','最高一者的称法；在不同文本不必都作为原生专名出现。不是某位普通Aeon的官衔。'),('Pleroma','神圣fullness／整体及其领域。可以包含内部生成差别，不等于一排所有成员完全同级。'),('Aeon / Aeons','可指神圣存在、其领域、时代或宇宙区域；须按文本及位置判断。不存在全Gnosticism统一总数。'),('Emanation','来源的展开；不同文本用生育、Thought、Light、Word等方式叙述，不一律是物理生殖。'),('Syzygy','相应的配对；可为male／female等关系，不应不加解释直接当现代婚姻。'),('Demiurge','制造／组织世界的角色名称；与Yaldabaoth常重合但不跨传统自动同一。'),('Archon / Archons','统治者及其powers；既可为首领，也可指下属群体，数量与名单各版本不同。'),('Ogdoad / Decad / Duodecad','八／十／十二的组列。可数存在也可指领域；不同文本不可只凭数字对齐。'),('Pronoia / Protennoia / Ennoia','Providence、First Thought、Thought等相关表达；在特定文本可连到Barbelo，不全局强制同一。'),('Epinoia','insight／reflective thought；Luminous Epinoia是AJ帮助者。与Sophia、Life等有交叠但须分文本。'),('Pneuma / Psyche / Hyle','spirit／soul／matter；对应pneumatic／psychic／hylic并非所有文本都同样分人。'),('Gnosis','使人认识神圣来源及自身处境的knowledge；与revealer、仪式、生活和归返相连。'),('Divine Spark','本项目比较用的概括术语：个体中的神性来源／成分。不是各原典统一采用的专名，也不推出每个人就是某位Aeon。'),('Heimarmene','宇宙命运与限制机制；不必每篇都同一拟人化对象。'),('Five Seals','部分Sethian文本的baptism／启示救赎语言；不能自动套给任何出现五的设定。'),('Kenoma / Hysterema','缺乏、空缺及Pleroma外不足状态的相关词；不把它们当作各篇都用的统一地图标签。')]
VARIANTS=[
 ('AJ · long / short','II / IV与III / BG','共有神圣生成、Sophia、下层造物、人类与启示骨架；措辞、权能名单、身体名录和末尾Pronoia段存在差异。','AJ'),
 ('AJ · Barbelo Pentad','Truth / Ennoia','长本明确Truth，短本相关配列采用Ennoia／Thought语言；不能复制一张表后声称逐字相同。','AJ'),
 ('AJ · Luminaries','Harmozel / Armozel; Oroiael / Oriel; Daveithe / Daveithai','异拼不自动表示不同神；不同传述如Irenaeus I.29还改变配列和名称。','AJ'),
 ('Aeons数量','AJ四组三项；Valentinian 8＋10＋12；EUG六对及72／360；PS宇宙区域','不同层的局部数字，不能化约为只有十二个Aeons。','IR'),
 ('Sophia位置','AJ / Valentinian / EUG / PS','可为失衡者、Pleroma内Aeon与外在Achamoth的相关来源、多个配偶称号、或第十三Aeon的受困者。','TUR'),
 ('Christ / Autogenes','AJ 与 Irenaeus I.29','AJ紧密相连；I.29按先后叙述区分，不应跨版本自动合并。','IR'),
 ('Demiurge评价','AJ / Flora / TT','敌对与无知、公正的中间者、被Logos用来组织下界，是不同材料给出的不同功能组合。','FL'),
 ('Sabaoth','AJ名单 / HA / OW','名字可在不同下层清单出现；HA与OW明确写悔悟与提升，不能被永久邪恶的统一定义覆盖。','HA'),
 ('Samael','AJ 与 Irenaeus I.30','AJ列为Chief Archon别名；I.30还把它用于serpent名号，必须区分来源。','IR'),
 ('Basilides报告','Irenaeus I.24 / Hippolytus VII','365天与顺次powers的结构，对照non-existent God、seed、三Sonship与两大Archons；不将两报告合成一套。','HI'),
 ('同属Pleroma','共同神圣来源 ≠ 完全同一内部层级','容纳Sophia、其他神圣存在与群体，不要求每个群体占一位专名Aeon的名额。','TUR')]

# Retain the named body-makers as a subordinate reference, not as divine peers.
ANATOMY=[]
raw=ROOT/'01_sources/gnostic_readings/downloads/AJ-W.txt'
if raw.exists():
    text=re.sub(r'\s+',' ',raw.read_text(encoding='utf-8'))
    start=text.index('Eteraphaope-Abron created his head');end=text.index('And those who were appointed over all of these',start)
    chunk=text[start:end]
    for fragment in chunk.split(';'):
        fragment=fragment.strip(' .\"')
        match=re.match(r'([A-Z][A-Za-z-]+)(?: \(created\))?(?: created)?[, ]+(.*)',fragment)
        if match:
            name,part=match.groups()
            ANATOMY.append(dict(name=name,function=part,system='aj',source='AJW',locator='NHC II,1 15–18; body-making catalogue',category='下界body-maker；不是Pleroma内Aeon'))

BODY_EXTRA='''Zathoth|造形诸灵之统辖者
Armas|造形诸灵之统辖者
Kalila|造形诸灵之统辖者
Jabel|造形诸灵之统辖者
Sabaoth|造形诸灵之统辖者
Cain|造形诸灵之统辖者
Abel|造形诸灵之统辖者
Diolimodraza|头部的活动
Yammeax|颈部的活动
Yakouib|右肩的活动
Verton|左肩的活动
Oudidi|右手的活动
Arbao|左手的活动
Lampno|右手手指的活动
Leekaphar|左手手指的活动
Barbar|右乳部的活动
Imae|左乳部的活动
Pisandriaptes|胸部的活动
Koade|右肩关节的活动
Odeor|左肩关节的活动
Asphixix|右肋部的活动
Synogchouta|左肋部的活动
Arouph|腹部的活动
Sabalo|子宫的活动
Charcharb|右大腿的活动
Chthaon|左大腿的活动
Bathinoth|生殖器的活动
Choux|右腿的活动
Charcha|左腿的活动
Aroer|右胫骨部的活动
Toechtha|左胫骨部的活动
Aol|右膝部的活动
Charaner|左膝部的活动
Bastan|右脚的活动
Archentechtha|右脚脚趾的活动
Marephnounth|左脚的活动
Abrana|左脚脚趾的活动
Michael|统辖身体诸活动的七者之一
Ouriel|统辖身体诸活动的七者之一
Asmenedas|统辖身体诸活动的七者之一
Saphasatoel|统辖身体诸活动的七者之一
Aarmouriam|统辖身体诸活动的七者之一
Richram|统辖身体诸活动的七者之一
Amiorps|统辖身体诸活动的七者之一
Archendekta|感官
Deitharbathas|接收／感受
Oummaa|想象
Aachiaram|组合
Riaramnacho|整体冲动
Phloxopha|热
Oroorrothos|冷
Erimacho|干
Athuro|湿
Onorthochrasaei|诸身体作用之母，matter
Ephememphi|快乐相关的chief demon
Yoko|欲望相关的chief demon
Nenentophni|悲伤相关的chief demon
Blaomen|恐惧相关的chief demon
Aesthesis-Ouch-Epi-Ptoe|四种情绪chief demons之母
Anaro|material soul之首及对其真实性质的认识'''
for line in BODY_EXTRA.splitlines():
    name,function=line.split('|');ANATOMY.append(dict(name=name,function=function,system='aj',source='AJW',locator='NHC II,1 17–19; lower powers catalogue',category='下界身体／感官／passions，不是Pleroma内Aeon'))
parts={'head':'头','brain':'脑','eye':'眼','ear':'耳','nose':'鼻','lips':'唇','teeth':'牙齿','molars':'臼齿','tonsils':'扁桃体','uvula':'悬雍垂','neck':'颈','vertebrae':'椎骨','throat':'咽喉','shoulder':'肩','elbow':'肘','underarm':'腋下','hand':'手','fingers':'手指','nails':'指甲','breast':'乳部','shoulder joint':'肩关节','belly':'腹部','navel':'脐','abdomen':'腹部','ribs':'肋部','hip':'髋','marrow':'骨髓','bones':'骨骼','stomach':'胃','heart':'心脏','lungs':'肺','liver':'肝','spleen':'脾','intestines':'肠','kidneys':'肾','sinews':'筋腱','spine of the body':'脊柱','veins':'静脉','arteries':'动脉','all the flesh':'全身肉体','buttock':'臀部','penis':'阴茎','testicles':'睾丸','genitals':'生殖器','thigh':'大腿','kidney':'肾','leg':'腿','shin-bone':'胫骨','knee':'膝','foot':'脚','toes':'脚趾'}
for entry in ANATOMY:
    original=entry['function']
    if original=='-':entry['function']='职司文字残缺，未补全'
    elif re.search('[a-z]',original):
        t=re.sub(r'^(?:the|his|its) ','',original)
        qualifier='右' if t.startswith('right ') else '左' if t.startswith('left ') else ''
        t=re.sub(r'^(?:right|left) ','',t);uncertain='（原译存疑）' if '(?)' in t else '';t=t.replace(' (?)','')
        if t in parts:entry['function']=qualifier+parts[t]+uncertain
        elif t=='fingers of the right hand':entry['function']='右手手指'
        elif t=='fingers of the left hand':entry['function']='左手手指'
        elif t=='nails of the hands':entry['function']='手指甲'
        elif t=='nails of the feet':entry['function']='脚趾甲'
        elif t=='theirs are the breaths which are in all the limbs':entry['function']='四肢中的气息'
        elif t=='kidneys of the right leg':entry['function']='右腿之肾（保留原译异常）'

# Separate the two Platonizing witnesses rather than display a blended genealogy.
old=next(s for s in systems if s['id']=='plat')
position=systems.index(old);systems.remove(old)
plat_nodes=[n for n in nodes if n['system']=='plat'];nodes[:]=[n for n in nodes if n['system']!='plat']
for offset,(sid,title,source,exclude) in enumerate([
 ('allogenes','Allogenes','ALL',{'repent','sojourn','copies','atmosphere','zostrianos','aphredon','authrounios','lights','perfect'}),
 ('zostrianos','Zostrianos','ZOS',{'youel','allogenes'})]):
    s=copy.deepcopy(old);s.update(id=sid,title=title,source=source,subtitle='NHC XI,3 · 静观与启示' if sid=='allogenes' else 'NHC VIII,1 · baptisms与上升')
    s['notes']+=['本页保留本篇结构；相邻页面可对照另一文本。'];systems.insert(position+offset,s)
    for item in plat_nodes:
        if item['key'] not in exclude:
            n=copy.deepcopy(item);n['id']=sid+'-'+n['key'];n['system']=sid;n['parent']=n['parent'].replace('plat-',sid+'-',1)
            if n['source'] not in ('TUR',):n['source']=source
            nodes.append(n)

SOURCES.update({
 'MARS':dict(title='Marsanes',url='https://www.earlychristianwritings.com/text/marsanes.html',edition='NHC X,1; Birger A. Pearson; extensive lacunae'),
 'NOREA':dict(title='Thought of Norea',url='https://www.earlychristianwritings.com/text/norea.html',edition='NHC IX,2; Giversen / Pearson'),
 'AA':dict(title='Apocalypse of Adam',url='https://www.earlychristianwritings.com/text/adam.html',edition='NHC V,5; MacRae'),
 'MELCH':dict(title='Melchizedek',url='https://www.earlychristianwritings.com/text/melchizedek.html',edition='NHC IX,1; Giversen / Pearson'),
})
m=system('mars','Marsanes','Platonizing Sethian','NHC X,1 · Thirteen Seals','MARS',[
 ('本源与神圣层次','不可名状的最高原则、Silent One与Invisible Spirit的区分出现在残损文本中；不能无缺文地重建。'),
 ('十三Seals','文本按seals讨论物质、非物质、神圣及超越层次，关联其认知把握。'),
 ('宇宙与灵魂','同时讨论宇宙、soul、字母声音及其power，不只是神谱。'),
 ('归返','通过认知诸层及其符号结构，获得稳定与rest。')],['这是现存残损文本的结构；没有用猜出的名字补齐缺文。','Seals不是十三位Aeons的名单。'])
row(m,0,'',[('highest','Unknowable Highest Principle','文本涉及高于一般可知对象的来源'),('silent','Silent One','超越神圣展开的相关名号'),('invisible','Invisible Spirit','与Silent One及其展开相连的层次')],kind='本源相关名号',locator='X,1 2–5; Turner pp. 557–588')
row(m,1,'invisible',[('triple','Triple-Powered One','神圣力量的三重关系'),('barbelo','Barbelo Aeon','神圣认知领域'),('autogenes','Autogenes','自生的神圣展开')],locator='X,1 4–10')
row(m,2,'barbelo',[('seals','Thirteen Seals','从物质到超越的认知标记'),('soul','Soul','被讨论及转换的对象'),('letters','Letters / Sounds / Powers','语言、声音及宇宙关系的符号性讨论')],kind='结构／对象',locator='X,1 2–4; 25–42')
node(m,'rest','Knowledge / Rest',3,'归返','达到确信、稳定与安息','seals',locator='X,1 2–4')
n=system('norea','Thought of Norea','Sethian','NHC IX,2 · 简短启示与祈求','NOREA',[
 ('呼求','Norea向Father、Ennoia、Nous、Logos等神圣名号呼求。'),('接纳','她被接入其位置，与Autogenes及Imperishable Ones相连。'),('认识与安息','她承受living Logos与Father之Mind，认识Pleroma而不再不足。')],['本篇Adamas的称呼及位置不能从AJ直接照搬。'])
row(n,0,'',[('father','Father of All / Adamas','本篇向其呼求、其内含Norea之Thought的最高相关名号'),('ennoia','Ennoia of Light','神圣Thought'),('nous','Nous / Logos / Voice of Truth','呼求中的神圣认知与启示称号')],kind='祈求名号',locator='IX,2 27,11–28,28')
node(n,'norea','Norea',1,'接受启示者','被接纳、认识并承受神圣Thought','father',locator='27,11–28,28')
row(n,2,'norea',[('autogenes','Autogenes','她得以安息的神圣存在'),('helpers','Four Holy Helpers','代其向Father祈求'),('imperishable','Imperishable Ones / Pleroma','她所参与并认识的神圣整体')],kind='援助／归属',locator='27,11–28,28')
aa=system('adamapoc','Apocalypse of Adam','Sethian','NHC V,5 · 历史、seed与Illuminator','AA',[
 ('神性与失落','Adam向Seth讲述自己与Eve曾有的glory与knowledge及其丧失。'),('世代与灾难','洪水等毁灭尝试与不受污染的seed保存交替展开。'),('启示者','Illuminator出现；十三kingdoms对其来源各有说法，另有无王权generation。'),('救赎','真正knowledge与保存seed的力量揭示其来处，抄本结尾以baptism及圣名语言收束。')],['十三kingdoms是关于Illuminator来源的不同说法，不是十三位Aeons。'])
row(aa,0,'',[('eternal','Eternal God','与造物者区别的神圣来源'),('creator','Creator / Ruler','使人受下界局限的权能')],kind='来源／统治者',locator='V,5 64–67')
row(aa,1,'eternal',[('adam','Adam / Eve','原有glory与knowledge、随后受局限'),('seth','Seth / Seed','启示保存与传递的群体来源'),('illuminator','Illuminator','末期启示并引发诸国不同说明')],kind='人祖／启示者',locator='64–85')
row(aa,2,'illuminator',[('kingdoms','Thirteen Kingdoms','对启示者来历的不同说法'),('kingless','Kingless Generation','有别于诸国、掌握不同认识的群体'),('waters','Living Water / Holy Name','结尾保存与启示的语言')],kind='群体／救赎',locator='77–85')

# Add explicit, source-qualified differences rather than normalize them away.
VARIANTS += [
 ('AJ · short七天名单','III / BG 对照 II','III首位Aoth、BG首位Yaoth为lion-faced；II首位Athoth为sheep-faced。第五项短本Adonaios，长本Sabaoth；逐本保存。','AJ'),
 ('AJ · 文本保存状况','II / III / IV / BG','II为较完整长本，IV为有缺损的长本；III与BG为两个短本见证，仍有独立异文。长短本是recensions，不是四个现代译者。','AJ'),
 ('神性来源与个体','Divine Spark / Seed / Aeon','神性由上界而来、参与神圣群体、对应某个专名Aeon，是三个不同关系。本文分别记录，不替用户提出人人都是某位Aeon的说法。','TUR'),
]
for n in nodes:
    if n['name']=='Harmoupiael' and n['system']=='eg':n['name']='Harmupiael'
    if n['system']=='basil':
        parents={'father':'','nous':'father','logos':'nous','phronesis':'logos','sophia':'phronesis','angels':'sophia','365':'angels','abraxas':'365','world':'365','christ':'father'}
        n['parent']='basil-'+parents[n['key']] if parents[n['key']] else ''
    if n['id']=='tt-man':n['role']='spiritual、psychic、material三种构成／类型的讨论对象'
    if n['id']=='ajshort-adam':n['parent']='ajshort-yald'
    n['relation']='关联／所属'
    if n['system'] in ('aj','ajshort') and n['key'] in ('yald','earthseth'):n['relation']='叙事中的生育来源'
    if n['system'] in ('aj','ajshort') and n['key'] in ('adamas','seth','seed','repentant'):n['relation']='安置／居所'
    if n['key'] in ('epinoia','soter','jesus'):n['relation']='派遣／援助关系'
    if n['detail']:n['relation']='名单归属'

from gnostic_relations import revise_atlas
variants=[dict(topic=a,versions=b,difference=c,source=d) for a,b,c,d in VARIANTS]
edges=revise_atlas(nodes,systems,SOURCES,variants)
data=dict(schema_version=2,title='Gnostic Cosmologies',systems=systems,nodes=nodes,edges=edges,sources=SOURCES,glossary=[dict(name=a,meaning=b) for a,b in GLOSSARY],variants=variants,anatomy=ANATOMY)
(OUT/'atlas_data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (OUT/'name_catalog.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['system','id','name','aliases','kind','tier','parent','function','source','locator','notes'])
    for n in nodes:w.writerow([n['system'],n['id'],n['name'],' / '.join(n['aliases']),n['kind'],n['tier'],n['parent'],n['role'],n['source'],n['locator'],n['notes']])
    for i,n in enumerate(ANATOMY):w.writerow(['aj','anatomy-'+str(i),n['name'],'','body-maker','subordinate','Body-Making Angels',n['function'],n['source'],n['locator'],n['category']])
with (OUT/'relationships.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['id','system','from_id','to_id','type','label','source','locator','interpretive','notes']);w.writeheader();w.writerows(edges)
md=['# Gnostic体系与名号总表','', '2026-10-31。以Sethian / Apocryphon of John为主视图、Ptolemaic Valentinian为主对照；其余传统和变体分开。角色、属性、领域、群体与过程分别标识。层号仅为图面排布，不是跨文本统一官阶。完整数据见atlas_data.json，可视化见index.html。','']
for s in systems:
    md+=['## '+s['title'],'',s['subtitle'],'']
    md+=['- '+h+'：'+p for h,p in s['flow']]
    md+=['','| 名号 | 类型 | 来源／上属 | 作用 | 定位 |','| --- | --- | --- | --- | --- |']
    lookup={n['id']:n['name'] for n in nodes}
    for n in nodes:
        if n['system']==s['id']:md.append('| '+n['name']+' | '+n['kind']+' | '+lookup.get(n['parent'],'—')+' | '+n['role'].replace('|','／')+' | '+n['source']+' '+n['locator']+' |')
    md+=['']+['- '+x for x in s['notes']]+['']
md+=['## 术语','']+['- **'+a+'**：'+b for a,b in GLOSSARY]+['','## 版本差异','']
md+=['- **'+v['topic']+'**（'+v['versions']+'）：'+v['difference'] for v in variants]
md+=['','## Apocryphon of John · 带类型的多来源关系','', '| 来源 | 对象 | 关系 | 原文定位 |','| --- | --- | --- | --- |']
lookup={n['id']:n['name'] for n in nodes}
for edge in edges:
    if edge['system']=='aj':md.append('| '+lookup[edge['from_id']]+' | '+lookup[edge['to_id']]+' | '+edge['label']+' | '+edge['locator']+' |')
md+=['','## 来源','']+['- '+k+'：['+v['title']+']('+v['url']+')；'+v['edition'] for k,v in SOURCES.items()]
(OUT/'cosmology_reference.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
template=OUT/'template.html'
if template.exists():
    content=template.read_text(encoding='utf-8').replace('__ATLAS_DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/'))
    content=content.replace('__ATLAS_APP__',(OUT/'app.js').read_text(encoding='utf-8'))
    (OUT/'index.html').write_text(content,encoding='utf-8')
print(f'{len(systems)} systems; {len(nodes)} entries; {len(ANATOMY)} body-maker appendix names')
