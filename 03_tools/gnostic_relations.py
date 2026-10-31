"""Typed, many-to-many relationships; layout rows are not ontological ranks."""
import copy

def revise_atlas(nodes, systems, sources, variants):
    sources['BROEK'] = dict(title='van den Broek · Gnostic Religion in Antiquity',
        url='https://www.cambridge.org/core/books/gnostic-religion-in-antiquity/271084C3309208717EB23F3A4CCCF7AA',
        edition='2013, p. 172: Sophia as one of the three attendants of Eleleth')
    sources['PLESE'] = dict(title='Pleše · Poetics of the Gnostic Universe',
        url='https://doi.org/10.1163/9789047404026',
        edition='NHMS 52, Brill 2006; discussion of II 11,22–26, note 35; distinguishes rulers, authorities, powers')
    nodes[:] = [n for n in nodes if n['id'] != 'aj-eleleth2']
    for prefix in ['aj', 'ajshort']:
        bykey = {n['key']: n for n in nodes if n['system'] == prefix}
        def update(key, **values):
            if key in bykey: bykey[key].update(values)
        update('autogenes', tier=1, notes='Father–Mother–Son结构中的Son；本图将其与四个属性的展开分组，不把排版先后当作精确本体位阶。Invisible Spirit与Barbelo共同参与其显现。')
        update('sophia', name='Sophia / Wisdom', tier=5, aliases=['Wisdom', 'Sophia of the Epinoia'],
            notes='按标准解释，与Eleleth随侍名单中的Wisdom作同一位处理，不重复计数。科普特文本同用Sophia，且van den Broek 2013 p.172明确按Eleleth的随侍者解释。失衡后的Ninth为另一叙事状态，不是原有神圣身份的降格排名。',
            locator='II 8,18–20; 9,25–10,19; 13,32–14,13; van den Broek 2013 p.172' if prefix=='aj' else 'III / BG对应四灯与Sophia段；Synopsis 20–25')
        update('seven', tier=9, role='原文七重powers及兽面名列的相关展开；与十二Authorities并列检视，不画成确定的较低一级。',
            notes='原文先说Archons产生powers，又将七重powers与Authorities结合。不能仅凭重名就逐项断言此名单等于十二名单中的前七位；也不将不同名列推成两套完全无关的统治者。Pleše对七rulers、powers及十二Authorities作进一步区分。')
        update('body', parent=prefix+'-seven', relation='造形与分工')
        update('counterfeit', parent=prefix+'-yald', kind='下层控制力量', relation='制造／控制', locator='II 21,6–10; 29,23–30,11')
        update('fate', parent=prefix+'-yald', kind='下层命运枷锁', relation='合谋生成', locator='II 28,11–32', notes='Chief Archon与Authorities的计划及末后束缚；原段另有与Sophia发生关系的晦涩叙事。不是Adam产生的对象。')
        update('spirit', parent=prefix+'-monad', kind='上界生命援助', relation='上界来向', locator='II 25,16–27,30', notes='从上界来临、使灵魂获得生命与力量；图线表达神圣来向，不补写其直接生育者。')
        update('eve', parent=prefix+'-yald', role='Chief Archon从Adam取其部分力量、依Epinoia显现形象塑成女性；Epinoia显现并唤醒认识。',
            kind='下界女性／启示承载', relation='造形', locator='II 22,28–23,26')
        update('epinoia', locator='II 20,9–29; 22,28–23,26', notes='受上界派遣并隐藏于Adam，帮助、唤醒并修正母亲缺陷；与Adam的援助／内在关系单独连线。')
        if prefix=='aj':
            update('return', parent='aj-barbelo', relation='Pronoia自述的行动',
                notes='II 30,11–31,25自述者为Pronoia；按该篇Barbelo／Pronoia关系连接，不归为Epinoia单独施行。', locator='II 30,11–31,25')
            update('twelve', notes='十二Authorities名列；七位被配置于七天、五位于深渊。与后续七重powers描述关系复杂，保留原文区分。')
            for n in bykey.values():
                if n['key'].startswith('authority') or n['key'].startswith('power'):
                    n['tier']=10
            nodes.append(dict(id='aj-kings',system='aj',key='kings',name='Seven Heavenly Kings',tier=9,
                kind='十二Authorities的天域分配',role='七位配置在七天，另五位配置于深渊；不强配每个兽面名号的一一身份。',
                parent='aj-twelve',aliases=[],source='AJ',locator='II 11,4–7',notes='这是配置／分组条目，不另增加七位新神。',detail=True,relation='配置于七天'))
            nodes.append(dict(id='aj-ninth',system='aj',key='ninth',name='Sophia · in the Ninth',tier=7,
                kind='失衡后的暂居状态',role='Sophia被安置在其子之上、第九处，直到修正缺陷；与其原本神圣身份分开呈现。',
                parent='aj-sophia',aliases=[],source='AJ',locator='II 13,32–14,13',notes='叙事状态卡，不是另一位Sophia，也不表示原典在此已绘出完整的九级家谱。',detail=False,relation='状态／位置变化'))
            nodes.append(dict(id='aj-five-lights',system='aj',key='five-lights',name='Five Lights',tier=11,
                kind='取回母之力量的援助',role='Mother–Father派遣，劝Yaldabaoth向Adam吹气，使母之力量转入人。',
                parent='aj-barbelo',aliases=[],source='AJ',locator='II 19,15–33',notes='保留原文five；不在这里擅自认定其五个成员的名字。',detail=True,relation='派遣／劝告'))

    edges=[]
    def add(prefix,a,b,typ,label,locator,source='AJ',interpretive=False,notes=''):
        edges.append(dict(id=f'{prefix}-edge-{len(edges)}',system=prefix,from_id=prefix+'-'+a,to_id=prefix+'-'+b,
            type=typ,label=label,source=source,locator=locator,interpretive=interpretive,notes=notes))
    for prefix in ['aj','ajshort']:
        exists={n['key'] for n in nodes if n['system']==prefix}
        def e(a,b,typ,label,loc,**kw):
            if a in exists and b in exists: add(prefix,a,b,typ,label,loc,**kw)
        e('monad','barbelo','emanation','First Thought显现','II 4,19–26')
        e('monad','autogenes','generation','以纯光参与Only-Begotten生成','II 6,10–18')
        e('barbelo','autogenes','generation','Mother–Father孕育Only-Begotten','II 6,10–18')
        for key in ['foreknow','incorrupt','life','truth']:
            e('monad',key,'emanation','应允后显现','II 4,26–6,10')
            e('barbelo',key,'request','请求；与之同立、同属Pentad','II 4,26–6,10')
        e('autogenes','nous','request','请求同工Mind','II 6,20–7,3')
        e('monad','nous','emanation','应允后Mind显现','II 6,20–7,3')
        e('nous','word','cooperation','通过Word行动','II 7,3–15')
        e('will','word','cooperation','Word随Will行动','II 7,3–15')
        e('word','autogenes','cooperation','Autogenes通过Word建立万有','II 7,3–15')
        for light in ['harmozel','oroiael','daveithe','eleleth']:
            e('autogenes',light,'emanation','Four Luminaries展开','II 7,30–8,28')
            for i in range(3):
                key='sophia' if light=='eleleth' and i==2 else light+str(i)
                e(light,key,'membership','随侍Aeon','II 7,30–8,28',interpretive=(key=='sophia'),
                  notes='Sophia与Wisdom按标准解释合一，另见van den Broek 2013 p.172。' if key=='sophia' else '')
        for a,b in [('harmozel','adamas'),('oroiael','seth'),('daveithe','seed'),('eleleth','repentant')]:
            e(a,b,'location','安置／居所','II 8,28–9,24')
        e('monad','adamas','emanation','与Autogenes之Will共同显现Perfect Man','II 8,28–9,11')
        e('autogenes','adamas','emanation','参与Perfect Man显现','II 8,28–9,11')
        e('adamas','seth','generation','其子','II 9,11–14')
        e('seth','seed','descent','seed／后裔','II 9,14–17')
        e('sophia','yald','generation','独自生育','II 9,25–10,19')
        e('sophia','yald','power','母之力量进入其子','II 10,19–22')
        e('sophia','ninth','state','悔悟后被安置于第九处','II 13,32–14,13')
        e('yald','twelve','generation','产生Authorities','II 10,26–11,22')
        e('twelve','kings','assignment','七位配于天、五位配于深渊','II 11,4–7')
        e('twelve','seven','textual','统治者的七重展开；具体认同不强并','II 11,23–12,25',interpretive=True,
          notes='保留文本称Archons产生powers的关系；不把十二名列和兽面名列无说明合为同七个人。')
        e('kings','seven','textual','七天统治与七重展开的关联','II 11,4–12,25',interpretive=True)
        for n in nodes:
            if n['system']==prefix and n['key'].startswith('authority'):
                e('twelve',n['key'],'membership','十二名列成员',n['locator'])
            if n['system']==prefix and n['key'].startswith('power'):
                e('seven',n['key'],'membership','兽面／七重配对名列',n['locator'])
        e('seven','body','generation','powers与造形天使的分工','II 11,23–26; 14,13–19,14')
        e('body','adam','formation','制作魂体／身体','II 14,13–19,14')
        e('yald','adam','formation','参与造形','II 14,13–19,14')
        e('adamas','adam','image','上界Man的形象／范型','II 14,13–15,13')
        e('yald','adam','power','吹气；母之力量转入Adam','II 19,15–33')
        e('sophia','barbelo','request','请求取回母之力量','II 19,15–23')
        e('barbelo','five-lights','assistance','派遣取回力量的帮助者','II 19,15–33')
        e('five-lights','yald','assistance','劝告向Adam吹气','II 19,15–33')
        e('barbelo','epinoia','assistance','Mother–Father派出帮助者','II 20,9–29')
        e('epinoia','adam','assistance','隐藏其中、帮助并唤醒','II 20,9–29')
        e('monad','spirit','source','上界Spirit的来向','II 25,16–27,30',notes='来向线，不指定其直接生育者。')
        e('spirit','adam','assistance','给予生命与力量','II 25,16–27,30')
        e('yald','counterfeit','control','与诸powers制造／施行仿冒Spirit','II 21,6–10; 29,23–30,11')
        e('counterfeit','adam','control','误导、遗忘与限制人的代表节点','II 25,16–30,11',notes='Adam在此代表受影响的人类；不将后来全部事件硬当Adam个人的一次经历。')
        e('yald','fate','control','与Authorities合谋形成命运束缚','II 28,11–32')
        e('twelve','fate','control','Chief Archon的Authorities共同参与','II 28,11–32')
        e('fate','adam','control','束缚受造界及人类','II 28,11–32')
        e('yald','eve','formation','取Adam部分力量塑成女性','II 22,28–23,26')
        e('adam','eve','material','取其部分力量／形体材料','II 22,28–23,26')
        e('epinoia','eve','image','形象与显现','II 22,28–23,26')
        e('adam','earthseth','generation','认识上界形象后生子','II 24,34–25,7')
        e('barbelo','earthseth','assistance','上界Mother降下Spirit','II 25,1–7')
        if prefix=='aj':e('barbelo','return','action','Pronoia自述下降、唤醒与Five Seals','II 30,11–31,25')
        else:e('epinoia','return','assistance','短本中的认识与归返','III / BG对应救赎段；不添长本颂歌')
    for n in nodes:
        if n['system'] not in ('aj','ajshort') and n['parent']:
            edges.append(dict(id='legacy-edge-'+n['id'],system=n['system'],from_id=n['parent'],to_id=n['id'],
                type='related',label=n.get('relation','关联／所属'),source=n['source'],locator=n['locator'],interpretive=False,
                notes='旧条目的主关联；不默认等同父子生育。'))
    for s in systems:
        if s['id'] in ('aj','ajshort'):
            s['notes']=[n for n in s['notes'] if '总人口' not in n]
            s['notes']+=['连线按生成、安置、力量传递与援助分别标记；排列组不是本体等级。','Sophia与随侍名列中的Wisdom合一；第九处另为失衡后的暂居状态。']
    variants.extend([
        dict(topic='AJ · Wisdom / Sophia',versions='II 8,18–20 与9,25起',difference='按原文词形及标准学术解释合为同一位，保留Wisdom别名；不重复计为两个Aeons。',source='BROEK'),
        dict(topic='AJ · 十二与七的关系',versions='II 10,26–12,25',difference='保留Authorities、七天的配置、兽面名列及powers展开。不能把图上同排等同于已证同一群体，也不画成一套无争议的低一级人口。',source='PLESE')])
    return edges
