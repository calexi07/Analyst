const {chromium}=require('playwright');const fs=require('fs');const {spawn}=require('child_process');
const vo=JSON.parse(fs.readFileSync('vo.json'));const IDS=['hook','recap','changed','today','next','outro'];
const TIM={};IDS.forEach(id=>{const lead=id==='hook'?0.15:0.55;TIM[id]={lead,starts:vo[id].starts,len:vo[id].len,dur:+(lead+vo[id].len+0.6).toFixed(3)}});
const total=IDS.reduce((a,id)=>a+TIM[id].dur,0);const off=[0];IDS.forEach((id,i)=>off.push(off[i]+TIM[id].dur));
fs.writeFileSync('tim.json',JSON.stringify({TIM,total,off}));
const FPS=30;const mode=process.argv[2]||'test';
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/scenes2.html');await p.evaluate(()=>document.fonts.ready);await p.evaluate(t=>setTim(t),TIM);
const cues=[];for(let i=0;i<6;i++){const c=await p.evaluate(i=>cueList(i),i);c.forEach(x=>cues.push({t:+(off[i]+x.t).toFixed(3),type:x.type}))}
fs.writeFileSync('cues.json',JSON.stringify(cues));
const go=async(i,t)=>p.evaluate(([i,t,g,T])=>render(i,t,g,T),[i,t,off[i]+t,total]);
if(mode==='test'){const shots=JSON.parse(process.argv[3]);for(const [i,t] of shots){await go(i,t);await p.screenshot({path:`test_${i}_${t}.jpg`,type:'jpeg',quality:80})}}
else{const only=process.argv[3]!==undefined?[+process.argv[3]]:[0,1,2,3,4,5];for(const i of only){const n=Math.round(TIM[IDS[i]].dur*FPS);
 const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p','-r','30',`tmp_${i}.mp4`]);
 for(let f=0;f<n;f++){await go(i,f/FPS);const buf=await p.screenshot({type:'jpeg',quality:92});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r))}
 ff.stdin.end();await new Promise((r,j)=>ff.on('close',c=>c===0?r():j(c)));fs.renameSync(`tmp_${i}.mp4`,`seg${i}.mp4`);console.log('seg',i,n)}}
await b.close();console.log(total.toFixed(2),cues.length)})();
