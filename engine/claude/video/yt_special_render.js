const {chromium}=require('playwright');const fs=require('fs');const {spawn}=require('child_process');
const spec=JSON.parse(fs.readFileSync('spec.json'));const vo=JSON.parse(fs.readFileSync('vo.json'));const IDS=spec.order;
const HOLD={title:1.2,outro:9.0,recap:1.2,news:1.2,meaning:1.5,pairs:1.5,watch:1.2,scen:1.5};const CH=['recap','news','meaning','pairs','watch','scen'];
const TIM={};IDS.forEach(id=>{const lead=id==='cold'?0.3:(CH.includes(id)?0.9:0.7);const tail=HOLD[id]||1.0;TIM[id]={lead,starts:vo[id].starts,dur:+(lead+vo[id].len+tail).toFixed(3)}});
const Tf=(sc,v)=>{v=String(v);if(v[0]!=='@')return +v;const m=v.slice(1).split('+');return TIM[sc].lead+TIM[sc].starts[+m[0]]+(m[1]?+m[1]:0)};
spec.subs=spec.subs.map(s=>[s[0],+Tf(s[0],s[1]).toFixed(3)]);
const total=IDS.reduce((a,id)=>a+TIM[id].dur,0);const off=[0];IDS.forEach((id,i)=>off.push(+(off[i]+TIM[id].dur).toFixed(3)));
fs.writeFileSync('tim.json',JSON.stringify({TIM,total,off,IDS}));
const FPS=30;const mode=process.argv[2]||'test';
async function page(b){const p=await b.newPage({viewport:{width:1920,height:1080}});await p.goto('file://'+process.cwd()+'/engine.html');await p.evaluate(()=>document.fonts.ready);
 await p.evaluate(([s,t,c])=>init(s,t,c),[spec,TIM,Object.fromEntries(IDS.map(id=>[id,vo[id].words]))]);return p}
(async()=>{const b=await chromium.launch();
 if(mode==='test'){const p=await page(b);const errs=[];p.on('pageerror',e=>errs.push(e.message));const shots=JSON.parse(process.argv[3]);for(const [i,t] of shots){await p.evaluate(([i,t,g,T])=>render(i,t,g,T),[i,t,off[i]+t,total]);await p.screenshot({path:`test_${i}_${t}.jpg`,type:'jpeg',quality:80})}console.log('errs',errs)}
 else if(mode==='cues'){const p=await page(b);const cues=[];for(let i=0;i<IDS.length;i++){const c=await p.evaluate(i=>cueList(i),i);c.forEach(x=>cues.push({t:+(off[i]+x.t).toFixed(3),type:x.type}))}fs.writeFileSync('cues.json',JSON.stringify(cues));console.log('cues',cues.length,total.toFixed(1));console.log(JSON.stringify(IDS.map((id,i)=>[id,off[i]])))}
 else{const list=process.argv[3].split(',').map(Number);const p=await page(b);for(const i of list){const n=Math.round(TIM[IDS[i]].dur*FPS);
  const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-c:v','libx264','-crf','19','-preset','veryfast','-pix_fmt','yuv420p','-r','30',`tmp_${i}.mp4`]);
  for(let f=0;f<n;f++){await p.evaluate(([i,t,g,T])=>render(i,t,g,T),[i,f/FPS,off[i]+f/FPS,total]);const buf=await p.screenshot({type:'jpeg',quality:90});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r))}
  ff.stdin.end();await new Promise((r,j)=>ff.on('close',c=>c===0?r():j(c)));fs.renameSync(`tmp_${i}.mp4`,`seg${i}.mp4`);console.log('seg',i,n)}}
 await b.close()})();
