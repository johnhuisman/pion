const $=id=>document.getElementById(id);
const names={k:'koning',q:'dame',r:'toren',b:'loper',n:'paard',p:'pion'};
let moves=[],claimed=null,flipped=false,selected=null,data=null,busy=false;
let catalog=[],lesson=null,group=null,color='white',timer=null,generation=0;
function save(){try{localStorage.setItem('pion-v2',JSON.stringify({moves,claim:claimed,lesson:lesson?.id,color}));}catch{}}
function say(message){$('comment').textContent=message;}
function activeTurn(){return data&&((data.turn==='Wit')===(color==='white'));}
function stopTimer(){generation++;clearTimeout(timer);timer=null;}
async function refresh(next=moves,claim=claimed){
 if(busy)return false;
 busy=true;
 try{
  const r=await fetch('/api/position',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({moves:next,claim})});
  const d=await r.json();if(!r.ok)throw Error(d.error||'Laden mislukt');
  moves=next;claimed=claim;data=d;selected=null;save();render();return true;
 }catch(e){say('De stelling kon niet worden geladen: '+e.message+' Probeer opnieuw.');return false;}
 finally{busy=false;}
}
function render(){
 $('board').replaceChildren();const files=flipped?'hgfedcba':'abcdefgh',ranks=flipped?'12345678':'87654321';
 for(const rank of ranks)for(const file of files){
  const sq=file+rank,p=data.pieces[sq],el=document.createElement('button');el.type='button';el.className='square'+((file.charCodeAt(0)+Number(rank))%2===0?' dark':'');
  el.setAttribute('aria-label',sq+(p?' '+(p===p.toUpperCase()?'witte ':'zwarte ')+names[p.toLowerCase()]:''));
  if(data.last&&(data.last.slice(0,2)===sq||data.last.slice(2,4)===sq))el.classList.add('last');
  if(data.check_square===sq)el.classList.add('check');if(selected===sq)el.classList.add('selected');
  if(selected&&data.legal.some(m=>m.startsWith(selected+sq)))el.classList.add('target');
  if(p){const img=document.createElement('img');img.className='piece-img';img.alt='';img.src='/static/pieces/'+(p===p.toUpperCase()?'w':'b')+p.toLowerCase()+'.svg';el.append(img);}
  if(file===files[0]){const c=document.createElement('span');c.className='coord';c.textContent=rank;el.append(c);}
  if(rank===ranks[7]){const c=document.createElement('span');c.className='coord file';c.textContent=file;el.append(c);}
  el.onclick=()=>choose(sq);$('board').append(el);
 }
 const complete=lesson&&moves.length===lesson.moves.length;
 $('status').textContent=complete?'Variant voltooid!':data.status;
 $('result').textContent=data.result||'';
 $('topPlayer').textContent=flipped?'Wit':'Zwart';$('bottomPlayer').textContent=flipped?'Zwart':'Wit';
 document.querySelectorAll('.dot')[0].className='dot '+(flipped?'white':'black');document.querySelectorAll('.dot')[1].className='dot '+(flipped?'black':'white');
 $('history').replaceChildren();
 if(!data.history.length){$('history').innerHTML='<p class="muted">Het bord ligt klaar.</p>';}
 for(let i=0;i<data.history.length;i+=2){const row=document.createElement('div');row.className='move-row';for(const txt of [String(i/2+1)+'.',data.history[i],data.history[i+1]||'']){const s=document.createElement('span');s.textContent=txt;row.append(s);}$('history').append(row);}
 $('history').scrollTop=$('history').scrollHeight;$('undo').disabled=!moves.length&&!claimed;$('claim').hidden=!!lesson||!data.claims.length;
 $('hint').disabled=!lesson||complete||!activeTurn();
 $('trainingLabel').textContent=lesson?`${group.name} · ${lesson.name} · jij speelt ${color==='white'?'wit':'zwart'} · ${moves.length}/${lesson.moves.length} halve zetten`:'Kies een opening en start de training.';
}
function completeMessage(){say('Goed gedaan, je hebt deze variant uitgespeeld. '+lesson.plan+' Oefen opnieuw of kies een andere variant.');}
function scheduleReply(){
 if(!lesson||!data)return;
 if(moves.length===lesson.moves.length){completeMessage();return;}
 if(activeTurn())return;
 const token=generation;
 timer=setTimeout(async()=>{
  timer=null;if(token!==generation||busy)return;
  const index=moves.length;
  if(await refresh([...moves,lesson.moves[index]],null)){
   say('Pion speelt '+lesson.san[index]+'. '+lesson.notes[index]+' '+lesson.plan);
   if(moves.length===lesson.moves.length)completeMessage();
  }
 },650);
}
async function playMove(uci){
 if(lesson){
  const index=moves.length;
  if(uci!==lesson.moves[index]){say('Deze zet is legaal, maar hoort niet bij de gekozen variant. Probeer opnieuw of vraag een hint. '+lesson.plan);selected=null;render();return;}
  if(await refresh([...moves,uci],null)){say('Goed: '+lesson.san[index]+'. '+lesson.notes[index]);scheduleReply();}
 }else await refresh([...moves,uci],null);
}
function choose(sq){
 if(busy||timer||!data||data.result)return;
 if(lesson&&(moves.length===lesson.moves.length||!activeTurn()))return;
 const options=selected?data.legal.filter(m=>m.startsWith(selected+sq)):[];
 if(options.length){
  if(options[0].length===5){$('choices').replaceChildren();for(const m of options){const b=document.createElement('button'),img=document.createElement('img');img.src='/static/pieces/'+(data.turn==='Wit'?'w':'b')+m[4]+'.svg';img.alt=names[m[4]];img.width=55;b.append(img);b.setAttribute('aria-label',names[m[4]]);b.onclick=()=>{$('promotion').close();playMove(m);};$('choices').append(b);}$('promotion').showModal();}
  else playMove(options[0]);return;
 }
 selected=data.legal.some(m=>m.startsWith(sq))?sq:null;render();
}
function fillVariants(){
 const g=catalog.find(o=>o.id===$('opening').value);$('variant').replaceChildren();
 for(const v of g.variants){const option=document.createElement('option');option.value=v.id;option.textContent=v.name;$('variant').append(option);}
 if(!lesson)say(g.intro+' '+g.variants[0].plan);
}
async function startTraining(){
 if(busy)return;
 const nextGroup=catalog.find(o=>o.id===$('opening').value),nextLesson=nextGroup.variants.find(v=>v.id===$('variant').value);
 stopTimer();const old={group,lesson,flipped};group=nextGroup;lesson=nextLesson;flipped=color==='black';
 if(await refresh([],null)){say(group.intro+' '+lesson.plan);scheduleReply();}else{group=old.group;lesson=old.lesson;flipped=old.flipped;}
}
function setColor(next){if(busy)return;color=next;$('playWhite').classList.toggle('active',color==='white');$('playBlack').classList.toggle('active',color==='black');if(lesson)startTraining();}
function setTheme(theme){document.body.dataset.theme=theme;document.querySelectorAll('[data-theme]').forEach(b=>{if(b.tagName==='BUTTON'){b.classList.toggle('active',b.dataset.theme===theme);b.setAttribute('aria-pressed',b.dataset.theme===theme);}});try{localStorage.setItem('pion-theme',theme);}catch{}}
for(const button of document.querySelectorAll('.board-themes button'))button.onclick=()=>setTheme(button.dataset.theme);
let theme='wood';try{theme=localStorage.getItem('pion-theme')||'wood';}catch{}setTheme(['wood','green','slate'].includes(theme)?theme:'wood');
$('cancelPromo').onclick=()=>$('promotion').close();
$('flip').onclick=()=>{flipped=!flipped;if(data)render();};
$('undo').onclick=async()=>{
 if(busy)return;stopTimer();let count=moves.length;
 if(claimed){}else if(lesson){count=Math.max(0,count-1);while(count>0&&((count%2===0)!==(color==='white')))count--;}
 else count=Math.max(0,count-1);
 if(await refresh(moves.slice(0,count),null)){say(lesson?'We doen die zet opnieuw. '+lesson.plan:'Zet teruggenomen.');scheduleReply();}
};
$('new').onclick=()=>{if(busy)return;if(lesson)startTraining();else{stopTimer();refresh([],null);}};
$('claim').onclick=()=>{if(!busy)refresh(moves,data.claims[0]);};
$('hint').onclick=()=>{if(!lesson||!activeTurn()||busy||timer)return;const i=moves.length;if(i>=lesson.moves.length)return;const uci=lesson.moves[i];selected=uci.slice(0,2);render();say('Probeer '+lesson.san[i]+'. '+lesson.notes[i]);};
$('opening').onchange=fillVariants;$('startTraining').onclick=startTraining;$('playWhite').onclick=()=>setColor('white');$('playBlack').onclick=()=>setColor('black');
async function init(){
 try{
  const response=await fetch('/api/openings');if(!response.ok)throw Error('Openingen laden mislukt');catalog=await response.json();
  for(const g of catalog){const o=document.createElement('option');o.value=g.id;o.textContent=g.name;$('opening').append(o);}fillVariants();
  let saved=null;try{saved=JSON.parse(localStorage.getItem('pion-v2')||'null');}catch{}
  if(saved&&Array.isArray(saved.moves)){
   for(const g of catalog){const v=g.variants.find(v=>v.id===saved.lesson);if(v&&saved.moves.every((m,i)=>m===v.moves[i])){group=g;lesson=v;break;}}
   moves=saved.moves;claimed=saved.claim||null;color=saved.color==='black'?'black':'white';flipped=color==='black';
   if(lesson){$('opening').value=group.id;fillVariants();$('variant').value=lesson.id;say(group.intro+' '+lesson.plan);}
   $('playWhite').classList.toggle('active',color==='white');$('playBlack').classList.toggle('active',color==='black');
  }
  if(await refresh(moves,claimed))scheduleReply();
 }catch(e){say(e.message+' Vernieuw de pagina om opnieuw te proberen.');}
}
init();
