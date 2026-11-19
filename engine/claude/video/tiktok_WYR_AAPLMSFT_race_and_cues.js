if(sc==='r1'){const p1=eio((t-T(sc,'@1'))/2.6),p2=eio((t-T(sc,'@2'))/2.0);const vb=1000+8700*p1,va=vb+4300*p2;const f=v=>'$'+(Math.round(v/10)*10).toLocaleString('en-US');
 const A=document.getElementById('vA'),Bv=document.getElementById('vB');A.textContent=(p2>=1?'≈ ':'')+f(va);Bv.textContent=(p1>=1?'≈ ':'')+f(vb);
 document.getElementById('bA').style.height=(40+430*(va-1000)/13000)+'px';document.getElementById('bB').style.height=(40+430*(vb-1000)/13000)+'px';
 const w=p2>=1;document.getElementById('bA').style.background=w?'var(--bull)':'var(--cream)';A.style.color=w?'var(--bull)':'var(--cream)'}
if(sc==='r1'){for(let k=0;k<2.4;k+=0.1)out.push({t:T(sc,'@1')+k,type:'tick2'});for(let k=0;k<1.8;k+=0.1)out.push({t:T(sc,'@2')+k,type:'tick2'});out.push({t:T(sc,'@2')+2.0,type:'hit'})}
