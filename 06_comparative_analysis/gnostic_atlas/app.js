const D = JSON.parse(document.getElementById('atlas-data').textContent);
const $ = selector => document.querySelector(selector);
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const lookup = new Map(D.nodes.map(n => [n.id, n]));
const edgeTypes = {all:'全部关系',generation:'生成／造形',location:'安置／谱系',power:'力量／形象',assistance:'援助／行动',control:'控制／束缚',membership:'名列／同工'};
const typeGroups = {generation:['generation','emanation','formation','material'],location:['location','descent','state','assignment'],power:['power','image','source'],assistance:['assistance','action','request'],control:['control'],membership:['membership','cooperation','textual','related']};
let sys='aj', view='graph', selected='aj-monad', detail=false, q='', edgeFilter='all', focusRelations=false;
const localSource = {AJ:'../../scratch/sources/waldstein_wisse_1995.pdf',TUR:'../../scratch/sources/TURNER-2001-VERIFIED.txt',PS:'../../01_sources/gnostic_readings/downloads/PS-MEAD.pdf',AJW:'../../01_sources/gnostic_readings/downloads/AJ-W.txt',HA:'../../01_sources/gnostic_readings/downloads/HA-E.txt',OW:'../../01_sources/gnostic_readings/downloads/OW-E.txt',TT:'../../01_sources/gnostic_readings/downloads/TT-E.txt',VE:'../../01_sources/gnostic_readings/downloads/VE-ALT.txt',TP:'../../01_sources/gnostic_readings/downloads/TP-E.txt',EG:'../../01_sources/gnostic_readings/downloads/EG-COPTIC.txt',EUG:'../../01_sources/gnostic_readings/downloads/EUG-E.txt',SJC:'../../01_sources/gnostic_readings/downloads/SJC-E.txt',ALL:'../../01_sources/gnostic_readings/downloads/ALL-E.txt',ZOS:'../../01_sources/gnostic_readings/downloads/ZOS-E.txt',FL:'../../01_sources/gnostic_readings/downloads/FLORA-E.txt',GT:'../../01_sources/gnostic_readings/downloads/GT-E.txt',HI:'../../01_sources/gnostic_readings/downloads/HIPP-VII.txt',MARS:'../../01_sources/gnostic_readings/downloads/MARS.txt',NOREA:'../../01_sources/gnostic_readings/downloads/NOREA.txt',AA:'../../01_sources/gnostic_readings/downloads/AA-CORRECT.txt',MELCH:'../../01_sources/gnostic_readings/downloads/MELCH.txt'};
function sourceUrl(id, locator='') {
    if (id==='IR') { const match=locator.match(/^I\.(\d+)/); if(match) return 'https://www.newadvent.org/fathers/01031'+match[1].padStart(2,'0')+'.htm'; }
    return D.sources[id]?.url || '#';
}
function nav() {
    let previous='';
    $('.sidebar').innerHTML=D.systems.map(s=>{
        const heading=s.tradition!==previous?'<div class="family">'+esc(s.tradition)+'</div>':'';
        previous=s.tradition;
        return heading+'<button class="nav '+(sys===s.id?'on':'')+'" data-system="'+s.id+'">'+esc(s.title)+'<span>'+esc(s.subtitle)+'</span></button>';
    }).join('');
    $('.mobile-select').innerHTML=D.systems.map(s=>'<option value="'+s.id+'" '+(s.id===sys?'selected':'')+'>'+esc(s.title)+'</option>').join('');
}
function relatedEdges(id) { return D.edges.filter(e=>e.from_id===id || e.to_id===id); }
function relationList(id) {
    const items=relatedEdges(id);
    return '<div class="meta"><label>关系与来源</label>'+items.map(e=>{
        const incoming=e.to_id===id, other=lookup.get(incoming?e.from_id:e.to_id);
        return '<div class="edge-record"><button data-node="'+other.id+'">'+(incoming?'← ':'→ ')+esc(other.name)+'</button><div>'+esc(e.label)+(e.interpretive?' · 对应解释':'')+'</div><a href="'+sourceUrl(e.source,e.locator)+'" target="_blank" rel="noopener">'+esc(e.locator)+'</a></div>';
    }).join('')+'</div>';
}
function detailPanel(n) {
    if (!n) return '';
    const source=D.sources[n.source];
    return '<div class="details"><div class="kind">'+esc(n.kind)+'</div><h3>'+esc(n.name)+'</h3><p>'+esc(n.role)+'</p>'+
        (n.notes?'<p>'+esc(n.notes)+'</p>':'')+
        (n.aliases.length?'<div class="meta"><label>同篇别名／异拼</label>'+esc(n.aliases.join(' · '))+'</div>':'')+
        relationList(n.id)+'<div class="meta"><label>条目来源</label><a class="source-link" target="_blank" rel="noopener" href="'+sourceUrl(n.source,n.locator)+'">'+esc(source.title)+'</a><div class="locator">'+esc(n.locator)+'</div><div class="locator">'+esc(source.edition)+'</div></div></div>';
}
const ajRows={0:'本源',1:'Father–Mother–Son',2:'Pentad · 神圣属性',3:'同工与作用',4:'Four Luminaries',5:'十二随侍Aeons',6:'人祖、后裔与安置群体',7:'Sophia的暂居状态',8:'下层造物者',9:'统治者与powers名列',10:'名列展开',11:'身体造形',12:'Adam与内在援助',13:'生命、形象与束缚',14:'Pronoia的救赎行动'};
function zone(tier) {
    if (['aj','ajshort'].includes(sys)) return tier===0?'本源':tier<7?'Pleroma · 神圣展开':tier===7?'失衡后的状态':tier<12?'Cosmos · 下层形成':'人的构成与救赎';
    if(sys==='val') return tier<8?'Pleroma':tier<11?'Pleroma之外 · 世界形成':'人的构成与归返';
    return '';
}
function graph() {
    const s=D.systems.find(s=>s.id===sys), shown=D.nodes.filter(n=>n.system===sys&&(detail||!n.detail));
    const tiers=[...new Set(shown.map(n=>n.tier))].sort((a,b)=>a-b);
    if(!shown.some(n=>n.id===selected)) selected=shown[0]?.id;
    const chart=tiers.map((tier,i)=>{
        const section=zone(tier)&&(i===0||zone(tier)!==zone(tiers[i-1]))?'<div class="zone">'+zone(tier)+'</div>':'';
        const label=['aj','ajshort'].includes(sys)?ajRows[tier]:'分组 '+String(tier+1).padStart(2,'0');
        const card=n=>'<button class="node '+(n.id===selected?'selected':'')+'" data-node="'+n.id+'"><span class="name">'+esc(n.name)+'</span><span class="kind">'+esc(n.kind)+'</span></button>';
        let cards;
        if(['aj','ajshort'].includes(sys)&&tier===5) {
            cards='<div class="member-columns">'+['harmozel','oroiael','daveithe','eleleth'].map(light=>'<div class="member-column">'+shown.filter(n=>n.tier===tier&&n.parent===sys+'-'+light).map(card).join('')+'</div>').join('')+'</div>';
        } else if(sys==='aj'&&tier===10) {
            cards='<div class="member-columns two">'+['twelve','seven'].map(group=>'<div class="member-column">'+shown.filter(n=>n.tier===tier&&n.parent==='aj-'+group).map(card).join('')+'</div>').join('')+'</div>';
        } else cards='<div class="cards">'+shown.filter(n=>n.tier===tier).map(card).join('')+'</div>';
        return section+'<div class="tier" data-row="'+tier+'"><div class="tierlabel">'+esc(label)+'</div>'+cards+'</div>';
    }).join('');
    return '<div class="viewhead"><div><h2>'+esc(s.title)+'</h2><div class="subtitle">'+esc(s.subtitle)+'</div></div><label class="toggle"><input id="detail-toggle" type="checkbox" '+(detail?'checked':'')+'> 展开名单</label></div>'+
        '<div class="relation-controls"><select id="edge-filter" aria-label="筛选关系类型">'+Object.entries(edgeTypes).map(([key,name])=>'<option value="'+key+'" '+(key===edgeFilter?'selected':'')+'>'+name+'</option>').join('')+'</select><span>实线：文本关系　虚线：对应解释</span></div>'+
        '<div class="graph-layout"><div><div class="chart"><svg class="links" aria-label="带类型的关系连线"><defs><marker id="arrow" markerWidth="5" markerHeight="5" refX="4.2" refY="2.5" orient="auto"><path d="M0 0 L5 2.5 L0 5" fill="#888" stroke="none"/></marker></defs></svg>'+chart+'</div>'+
        '<div class="reading"><h3>生成与归返</h3><div class="flow">'+s.flow.map(([h,p],i)=>'<div><b>'+String(i+1).padStart(2,'0')+' · '+esc(h)+'</b><p>'+esc(p)+'</p></div>').join('')+'</div><ul class="notes">'+s.notes.map(n=>'<li>'+esc(n)+'</li>').join('')+'</ul></div></div>'+detailPanel(lookup.get(selected))+'</div>';
}
function filteredEdges() {
    return D.edges.filter(e=>e.system===sys&&(edgeFilter==='all'||typeGroups[edgeFilter]?.includes(e.type)));
}
function links() {
    const chart=$('.chart'); if(!chart) return;
    const svg=$('.links'), rect=chart.getBoundingClientRect();
    const elements=new Map([...chart.querySelectorAll('.node')].map(el=>[el.dataset.node,el]));
    svg.setAttribute('viewBox','0 0 '+rect.width+' '+rect.height);
    svg.querySelectorAll('path.edge').forEach(p=>p.remove());
    const visible=filteredEdges().filter(e=>elements.has(e.from_id)&&elements.has(e.to_id));
    const ports=new Map();
    for(const edge of visible) for(const id of [edge.from_id,edge.to_id]) {
        if(!ports.has(id)) ports.set(id,[]);
        ports.get(id).push(edge.id);
    }
    const port=(id,edgeId)=>{
        const group=ports.get(id), index=group.indexOf(edgeId);
        return (index+1)/(group.length+1);
    };
    for(const [index,edge] of visible.entries()) {
        const source=elements.get(edge.from_id), target=elements.get(edge.to_id);
        if(!source||!target) continue; // Hidden entries have no rendered card.
        const a=source.getBoundingClientRect(), b=target.getBoundingClientRect();
        const ax=a.x-rect.x, ay=a.y-rect.y, bx=b.x-rect.x, by=b.y-rect.y;
        let path;
        const sameRow=Math.abs((ay+a.height/2)-(by+b.height/2))<Math.max(a.height,b.height);
        if(sameRow) {
            const right=bx>ax, x1=right?ax+a.width:ax, x2=right?bx:bx+b.width;
            const y1=ay+a.height*port(edge.from_id,edge.id), y2=by+b.height*port(edge.to_id,edge.id);
            const gap=Math.max(10,Math.min(32,Math.abs(x2-x1)/2));
            path=`M${x1},${y1} C${x1+(right?gap:-gap)},${y1-16} ${x2+(right?-gap:gap)},${y2-16} ${x2},${y2}`;
        } else {
            const down=by>ay, x1=ax+a.width*port(edge.from_id,edge.id),x2=bx+b.width*port(edge.to_id,edge.id);
            const y1=down?ay+a.height:ay,y2=down?by:by+b.height;
            if(Math.abs(lookup.get(edge.from_id).tier-lookup.get(edge.to_id).tier)>2 || !down) {
                const left=['power','image','source','assistance','action'].includes(edge.type);
                const inset=5+(index%13)*1.7;
                const rail=left?inset:rect.width-inset;
                const middle=(y1+y2)/2, distance=Math.abs(y2-y1), bend=(down?1:-1)*Math.min(65,distance*.2);
                // Separate ports and curved outer routes preserve every relationship.
                path=`M${x1},${y1} C${x1},${y1+bend} ${rail},${y1+bend} ${rail},${middle} C${rail},${y2-bend} ${x2},${y2-bend} ${x2},${y2}`;
            } else path=`M${x1},${y1} C${x1},${y1+22} ${x2},${y2-22} ${x2},${y2}`;
        }
        const el=document.createElementNS('http://www.w3.org/2000/svg','path');
        el.setAttribute('class','edge '+(edge.interpretive?'interpretive ':'')+(focusRelations&&(edge.from_id===selected||edge.to_id===selected)?'selected':''));
        el.setAttribute('data-edge',edge.id);el.setAttribute('data-type',edge.type);el.setAttribute('d',path);el.setAttribute('marker-end','url(#arrow)');
        const title=document.createElementNS('http://www.w3.org/2000/svg','title');
        title.textContent=lookup.get(edge.from_id).name+' → '+lookup.get(edge.to_id).name+' · '+edge.label+' · '+edge.locator;
        el.append(title);svg.append(el);
    }
}
function tableRows(list) {
    return list.map(n=>{
        const incoming=D.edges.filter(e=>e.to_id===n.id);
        return '<tr><td><button class="textbutton" data-node="'+n.id+'">'+esc(n.name)+'</button><small>'+esc(n.aliases.join(' / '))+'</small></td><td>'+esc(n.kind)+'<small>'+esc(D.systems.find(s=>s.id===n.system).title)+'</small></td><td>'+incoming.map(e=>esc(lookup.get(e.from_id)?.name)+'<small>'+esc(e.label)+'</small>').join('<br>')+'</td><td>'+esc(n.role)+'</td><td><a href="'+sourceUrl(n.source,n.locator)+'" target="_blank" rel="noopener">'+esc(n.locator)+'</a></td></tr>';
    }).join('');
}
function catalog(all=false) {
    const needle=q.trim().toLowerCase();
    const list=D.nodes.filter(n=>(all||needle||n.system===sys)&&[n.name,...n.aliases,n.role,n.notes,n.kind,D.systems.find(s=>s.id===n.system).title].join(' ').toLowerCase().includes(needle));
    const anatomy=D.anatomy.filter(n=>(!needle&&sys==='aj')||needle&&(n.name+' '+n.function).toLowerCase().includes(needle));
    return '<div class="viewhead"><div><h2>'+(all?'全部名号':needle?'名号检索':'名号表')+'</h2><div class="subtitle">'+list.length+' 项；同名在不同文本中分开保存</div></div><button class="back" id="all-catalog">全部体系</button></div>'+
        '<div class="tablewrap"><table><thead><tr><th>名号／别名</th><th>类型／文本</th><th>来源／安置／其他关系</th><th>作用</th><th>定位</th></tr></thead><tbody>'+tableRows(list)+'</tbody></table></div>'+
        (anatomy.length?'<h3 class="sectiontitle">Body-making catalogue · '+anatomy.length+' 项</h3><div class="tablewrap"><table><thead><tr><th>名号</th><th>职司</th><th>所属</th></tr></thead><tbody>'+anatomy.map(n=>'<tr><td>'+esc(n.name)+'</td><td>'+esc(n.function)+'</td><td>下界身体／感官／passions</td></tr>').join('')+'</tbody></table></div>':'');
}
function variants() {
    return '<div class="viewhead"><div><h2>版本对照</h2><div class="subtitle">同名、同数字不作跨文本自动合并</div></div></div><div class="tablewrap"><table><thead><tr><th>关系</th><th>版本</th><th>差异</th></tr></thead><tbody>'+D.variants.map(v=>'<tr><td>'+esc(v.topic)+'</td><td>'+esc(v.versions)+'</td><td>'+esc(v.difference)+'</td></tr>').join('')+'</tbody></table></div>';
}
function sources() {
    return '<div class="viewhead"><div><h2>资料与术语</h2><div class="subtitle">原典、版本及学术整理</div></div></div><div class="sourcegrid">'+Object.entries(D.sources).map(([id,s])=>'<article class="sourcecard"><h3>'+esc(s.title)+'</h3><p>'+esc(s.edition)+'</p><a href="'+s.url+'" target="_blank" rel="noopener">原文／出版信息 ↗</a>'+(localSource[id]?' · <a href="'+localSource[id]+'">本地资料</a>':'')+'</article>').join('')+'</div><h3 class="sectiontitle">术语</h3><div class="glossary">'+D.glossary.map(g=>'<div class="term"><b>'+esc(g.name)+'</b><p>'+esc(g.meaning)+'</p></div>').join('')+'</div><h3 class="sectiontitle">数据与下载</h3><p class="subtitle"><a href="../../01_sources/gnostic_readings/download_manifest.json">下载与指纹清单</a> · <a href="atlas_data.json">关系数据 JSON</a> · <a href="name_catalog.csv">名号表 CSV</a> · <a href="relationships.csv">多来源关系 CSV</a> · <a href="cosmology_reference.md">文字总表</a></p>';
}
function render() {
    nav();$('.tabs').querySelectorAll('button').forEach(b=>{b.classList.toggle('on',b.dataset.view===view);b.setAttribute('aria-selected',b.dataset.view===view)});
    $('#view').innerHTML=view==='graph'?graph():view==='catalog'?catalog():view==='variants'?variants():sources();
    $('#counts').textContent=D.systems.length+' views / '+D.nodes.length+' entries';
    requestAnimationFrame(links);
}
function selectNode(id) {
    if(id==='aj-eleleth2')id='aj-sophia';
    const n=lookup.get(id);if(!n)return;
    sys=n.system;selected=id;view='graph';q='';focusRelations=true;$('.search').value='';if(n.detail)detail=true;render();
}
document.addEventListener('click',e=>{
    const n=e.target.closest('[data-node]'),s=e.target.closest('[data-system]'),v=e.target.closest('[data-view]');
    if(n)selectNode(n.dataset.node);
    else if(s){sys=s.dataset.system;selected='';q='';focusRelations=false;$('.search').value='';render();}
    else if(v){view=v.dataset.view;render();}
    else if(e.target.id==='all-catalog')$('#view').innerHTML=catalog(true);
});
document.addEventListener('change',e=>{
    if(e.target.id==='detail-toggle'){detail=e.target.checked;render();}
    else if(e.target.id==='edge-filter'){edgeFilter=e.target.value;links();}
    else if(e.target.matches('.mobile-select')){sys=e.target.value;selected='';render();}
});
$('.search').addEventListener('input',e=>{q=e.target.value;view='catalog';render();});
window.addEventListener('resize',()=>requestAnimationFrame(links));
render();
