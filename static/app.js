const $=id=>document.getElementById(id);
const glyph={K:'♚',Q:'♛',R:'♜',B:'♝',N:'♞',P:'♟',k:'♚',q:'♛',r:'♜',b:'♝',n:'♞',p:'♟'};
const names={k:'koning',q:'dame',r:'toren',b:'loper',n:'paard',p:'pion'};
let moves=[],claimed=null,flipped=false,selected=null,data=null,busy=false;
try { const saved=JSON.parse(localStorage.getItem('pion-v1')||'{}');moves=saved.moves||[];claimed=saved.claim||null; }catch{}
function save(){try{localStorage.setItem('pion-v1',JSON.stringify({moves,claim:claimed}));}catch{}}
async function refresh(next=moves,claim=claimed){
 busy=true;
 try{const r=await fetch('/api/position',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({moves:next,claim})});const d=await r.json();if(!r.ok)throw Error(d.error||'Laden mislukt');moves=next;claimed=claim;data=d;selected=null;save();render();}
 catch(e){$('status').textContent=e.message;}
 finally{busy=false;}
}
function render(){
 $('board').replaceChildren();const files=flipped?'hgfedcba':'abcdefgh',ranks=flipped?'12345678':'87654321';
 for(const rank of ranks)for(const file of files){const sq=file+rank,p=data.pieces[sq];const el=document.createElement('button');el.type='button';el.className='square'+((file.charCodeAt(0)+Number(rank))%2===0?' dark':'');el.setAttribute('aria-label',sq+(p?' '+(p===p.toUpperCase()?'witte ':'zwarte ')+names[p.toLowerCase()]:''));
 if(data.last&&(data.last.slice(0,2)===sq||data.last.slice(2,4)===sq))el.classList.add('last');if(data.check_square===sq)el.classList.add('check');if(selected===sq)el.classList.add('selected');if(selected&&data.legal.some(m=>m.startsWith(selected+sq)))el.classList.add('target');
 if(p){const span=document.createElement('span');span.className='piece '+(p===p.toUpperCase()?'w':'b');span.textContent=glyph[p];el.append(span);}
 if(file===files[0]){const c=document.createElement('span');c.className='coord';c.textContent=rank;el.append(c);}if(rank===ranks[7]){const c=document.createElement('span');c.className='coord file';c.textContent=file;el.append(c);}el.onclick=()=>choose(sq);$('board').append(el);}
 $('status').textContent=data.status;$('result').textContent=data.result||'';$('topPlayer').textContent=flipped?'Wit':'Zwart';$('bottomPlayer').textContent=flipped?'Zwart':'Wit';document.querySelectorAll('.dot')[0].className='dot '+(flipped?'white':'black');document.querySelectorAll('.dot')[1].className='dot '+(flipped?'black':'white');
 $('history').replaceChildren();if(!data.history.length){$('history').innerHTML='<p class="muted">Het bord ligt klaar.</p>';}
 for(let i=0;i<data.history.length;i+=2){const row=document.createElement('div');row.className='move-row';for(const txt of [String(i/2+1)+'.',data.history[i],data.history[i+1]||'']){const s=document.createElement('span');s.textContent=txt;row.append(s);}$('history').append(row);}$('history').scrollTop=$('history').scrollHeight;$('undo').disabled=!moves.length&&!claimed;$('claim').hidden=!data.claims.length;
}
function choose(sq){if(busy||!data||data.result)return;const options=selected?data.legal.filter(m=>m.startsWith(selected+sq)):[];if(options.length){if(options[0].length===5){$('choices').replaceChildren();for(const m of options){const b=document.createElement('button');b.textContent=glyph[data.turn==='Wit'?m[4].toUpperCase():m[4]];b.setAttribute('aria-label',names[m[4]]);b.onclick=()=>{$('promotion').close();refresh([...moves,m],null);};$('choices').append(b);}$('promotion').showModal();}else refresh([...moves,options[0]],null);return;}selected=data.legal.some(m=>m.startsWith(sq))?sq:null;render();}
$('cancelPromo').onclick=()=>$('promotion').close();$('flip').onclick=()=>{flipped=!flipped;if(data)render();};$('undo').onclick=()=>{if(!busy)refresh(claimed?moves:moves.slice(0,-1),null);};$('new').onclick=()=>{if(!busy&&(!moves.length||confirm('Een nieuwe partij beginnen?')))refresh([],null);};$('claim').onclick=()=>{if(!busy)refresh(moves,data.claims[0]);};refresh();
