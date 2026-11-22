/* ===== Strategies — alerts from the TradingView strategies (BE Swing · BE MACD · BE Intraday) =====
   TradingView → strategy-alert function → do_strat_events + Web Push to this phone. The page polls every 30 s while it is open. */
const ST_DEF = [
  ['SWING', 'BE Swing', '#7AA2FF', 'Bias + structure, 4H / 1H / 15m signal candles · holds days'],
  ['MACD', 'BE MACD', '#B69CFF', 'MACD cross with the bias, 1H · TP 3R'],
  ['INTRADAY', 'BE Intraday', '#FFC857', 'Europe + New York opening range, gold EMA20 pullback · max 4h'],
];
const ST_EV = {
  order:['📥','Order to place','info'], open:['🚀','Open now','pos'], filled:['✅','Filled','pos'], cancel:['✖','Cancel order','amber'],
  move:['🔒','Move the SL','info'], partial:['💰','Half closed','pos'], closenow:['⏹','Close now','neg'], closed:['🏁','Closed','muted'], unparsed:['❔','Unread message','muted'],
};
const ST_ACT = ['order','open','cancel','move','partial','closenow'];
S.stv = S.stv || { rows:[], loaded:false, err:null, busy:false, timer:null, sig:'' };
const stDec = p => /JPY/.test(p) ? 3 : /XAU/.test(p) ? 2 : /^(GER40|NAS100|US30|SPX500|UK100)$/.test(p) ? 1 : 5;
const stPx = (p, x) => x==null ? '–' : Number(x).toFixed(stDec(p || ''));
const stR = r => r==null ? '' : (r >= 0 ? '+' : '−') + Math.abs(r).toFixed(2) + 'R';
const stWhen = t => { const d = new Date(t), now = new Date(), f = o => d.toLocaleString('en-GB', { timeZone:'Europe/Bucharest', ...o });
  const same = f({ day:'2-digit', month:'2-digit', year:'numeric' }) === now.toLocaleString('en-GB', { timeZone:'Europe/Bucharest', day:'2-digit', month:'2-digit', year:'numeric' });
  return (same ? 'Today' : f({ weekday:'short', day:'numeric', month:'short' })) + ' ' + f({ hour:'2-digit', minute:'2-digit' }); };
const stWeekStart = () => { const d = new Date(); const day = (d.getDay() + 6) % 7; d.setHours(0, 0, 0, 0); d.setDate(d.getDate() - day); return d.getTime(); };
async function stLoad(){
  if(S.stv.busy) return false; S.stv.busy = true;
  try{
    const { data, error } = await sb.from('do_strat_events').select('*').order('at', { ascending:false }).limit(1500);
    if(error) throw error;
    const sig = data.length + '|' + (data[0]?.id ?? '') + '|' + data.filter(r => r.done).length;
    const changed = sig !== S.stv.sig; S.stv.rows = data; S.stv.sig = sig; S.stv.err = null; S.stv.loaded = true; return changed;
  }catch(e){ S.stv.err = /relation|does not exist|schema cache/i.test(e.message || '') ? 'missing' : (e.message || String(e)); S.stv.loaded = true; return true; }
  finally{ S.stv.busy = false; }
}
/* open trades and pending orders, rebuilt from the event stream */
function stState(rows){
  const key = r => [r.variant, r.pair, r.trade_id].join('|');
  const open = new Map(), pend = new Map(), closed = [];
  [...rows].sort((a, b) => a.id - b.id).forEach(r => {
    const k = key(r);
    if(r.ev === 'order') pend.set(k, r);
    else if(r.ev === 'cancel') pend.delete(k);
    else if(r.ev === 'open' || r.ev === 'filled'){
      pend.delete(k);
      if(r.ev === 'filled' && / /.test(r.trade_id || '')) { const g = r.trade_id.split(' ')[0]; [...pend.keys()].forEach(x => { const p = pend.get(x); if(p.variant===r.variant && p.pair===r.pair && (p.trade_id||'').startsWith(g + ' ')) pend.delete(x); }); }
      const o = open.get(k); open.set(k, { ...(o || {}), ...r, sl0: o?.sl0 ?? r.sl, opened: o?.opened ?? r.at });
    }
    else if(r.ev === 'move'){ const o = open.get(k); if(o) open.set(k, { ...o, sl:r.sl, locked:r.r }); }
    else if(r.ev === 'partial'){ const o = open.get(k); if(o) open.set(k, { ...o, half:true }); closed.push(r); }
    else if(r.ev === 'closenow'){ const o = open.get(k); if(o) open.set(k, { ...o, closing:r.what }); }
    else if(r.ev === 'closed'){ open.delete(k); closed.push(r); }
  });
  return { open:[...open.values()], pend:[...pend.values()], closed };
}
function stStats(closed){
  const full = closed.filter(r => r.ev === 'closed' && r.r != null), wk = stWeekStart();
  const sum = a => a.reduce((s, r) => s + (r.r || 0), 0);
  const wkR = closed.filter(r => r.r != null && new Date(r.at).getTime() >= wk);
  return { n:full.length, w:full.filter(r => r.r > 0).length, R:sum(closed.filter(r => r.r != null)), wkR:sum(wkR), wkN:wkR.filter(r => r.ev==='closed').length };
}
function renderStrategies(){
  const m = document.getElementById('main'); if(!m) return;
  if(!S.stv.loaded){ m.innerHTML = '<div class="card fc-empty"><p>Loading strategy alerts…</p></div>'; stLoad().then(() => S.view==='strategies' && renderStrategies()); stPoll(); return; }
  stPoll();
  const f = ls.get('do_st_f', 'all'), todo = ls.get('do_st_todo', '0') === '1';
  const rows = S.stv.rows, mine = r => f === 'all' || r.strategy === f;
  const cards = ST_DEF.map(([k, name, col, sub]) => {
    const rs = rows.filter(r => r.strategy === k), st = stState(rs), s = stStats(st.closed), last = rs[0];
    return `<button type="button" class="st-card" data-stf="${k}" aria-pressed="${f===k}" style="--c:${col}">
      <div class="st-ch"><b>${name}</b><span>${esc(sub)}</span></div>
      <div class="st-kp"><div><em>${st.open.length}</em><small>open</small></div><div><em>${st.pend.length}</em><small>pending</small></div>
        <div><em class="${s.wkR > 0 ? 'up' : s.wkR < 0 ? 'dn' : ''}">${s.wkN || s.wkR ? stR(s.wkR) : '–'}</em><small>this week</small></div>
        <div><em class="${s.R > 0 ? 'up' : s.R < 0 ? 'dn' : ''}">${s.n ? stR(s.R) : '–'}</em><small>${s.n ? `${s.n} trades · ${Math.round(100 * s.w / s.n)}% win` : 'no trades yet'}</small></div></div>
      <div class="st-last">${last ? `Last alert ${esc(stWhen(last.at))} · ${esc(last.pair || '')}` : 'No alert yet'}</div></button>`; }).join('');
  const all = stState(rows.filter(mine));
  const live = [...all.pend.map(r => ({ ...r, kind:'pend' })), ...all.open.map(r => ({ ...r, kind:'open' }))].sort((a, b) => (b.at > a.at ? 1 : -1));
  const lvl = r => `<div class="st-lv"><span>Entry <b>${stPx(r.pair, r.entry)}</b></span><span class="dn">SL <b>${stPx(r.pair, r.sl)}</b></span><span class="up">TP <b>${r.tp==null ? 'none' : stPx(r.pair, r.tp)}</b></span>${r.lots10k ? `<span>${fmt(r.lots10k, 2)} lots / $10k</span>` : ''}</div>`;
  const nm = r => (ST_DEF.find(d => d[0]===r.strategy) || [0, r.strategy])[1] + (r.variant && r.variant.includes(' ') ? ' ' + r.variant.split(' ').slice(1).join(' ') : '');
  const side = r => r.dir > 0 ? '<span class="wl-tag" style="background:#22AB94;color:#fff">▲ Long</span>' : r.dir < 0 ? '<span class="wl-tag" style="background:#F23645;color:#fff">▼ Short</span>' : '';
  const tv = p => `https://www.tradingview.com/chart/?symbol=${encodeURIComponent('FOREXCOM:' + p)}`;
  const liveCard = r => `<article class="st-live ${r.kind}">
      <div class="st-lh"><b>${esc(r.pair)}</b>${side(r)}<span class="wl-tag" style="background:var(--surface-2)">${esc(nm(r))}</span>
        <span class="wl-tag st-k-${r.kind}">${r.kind==='pend' ? '⏳ ' + esc(r.what || 'order') + ' pending' : r.closing ? '⏹ close now' : r.half ? '💰 half off' : '● in trade'}</span></div>
      ${lvl(r)}
      <div class="muted st-sm">${r.kind==='pend' ? 'Placed' : 'Opened'} ${esc(stWhen(r.opened || r.at))}${r.kind==='open' && r.sl0!=null && r.sl!==r.sl0 ? ` · SL moved from ${stPx(r.pair, r.sl0)}${r.locked!=null ? ' · locks ' + stR(r.locked) : ''}` : ''}${r.closing ? ` · strategy says close (${esc(r.closing)})` : ''}</div>
      <a class="st-sm" href="${tv(r.pair)}" target="_blank" rel="noopener">Open the chart ↗</a></article>`;
  const feed = rows.filter(mine).filter(r => !todo || (ST_ACT.includes(r.ev) && !r.done)).slice(0, 200);
  const evCard = r => { const [ic, lbl, tone] = ST_EV[r.ev] || ['•', r.ev, 'muted'], act = ST_ACT.includes(r.ev);
    const lines = (r.body || '').split('\n'), doL = lines.filter(l => /^Do:|^Nothing to do|^Your |^Entry recorded/.test(l)), info = lines.filter(l => !doL.includes(l));
    return `<article class="st-ev ${act && !r.done ? 'act' : ''} ${r.done ? 'done' : ''}" style="--t:var(--${tone==='muted' ? 'muted' : tone})">
      <div class="st-eh"><i>${ic}</i><span class="st-et"><b>${esc(r.pair || '')}</b> · ${esc(lbl)}${r.r!=null ? ` <em class="${r.r >= 0 ? 'up' : 'dn'}">${stR(r.r)}</em>` : ''}</span><span class="muted st-sm">${esc(nm(r))} · ${esc(stWhen(r.at))}</span></div>
      <div class="st-tt">${esc((r.title || '').replace(/^BE [A-Z]+( \S+)? · [A-Z0-9]+ · /, ''))}</div>
      ${info.length ? `<div class="st-sm">${esc(info.join('\n'))}</div>` : ''}
      ${doL.length ? `<div class="st-do">${esc(doL.join('\n'))}</div>` : ''}
      <div class="st-ef">${act ? (r.done ? '<span class="muted st-sm">✓ done</span>' : `<button type="button" class="btn btn-primary" data-stdone="${r.id}">✓ Done</button>`) : ''}${r.pair ? `<a class="btn" href="${tv(r.pair)}" target="_blank" rel="noopener">Chart ↗</a>` : ''}</div></article>`; };
  const nTodo = rows.filter(mine).filter(r => ST_ACT.includes(r.ev) && !r.done).length;
  const hook = `${SUPABASE_URL}/functions/v1/strategy-alert?key=${ls.get('do_st_key', '') || 'YOUR_STRAT_KEY'}`;
  m.innerHTML = `<header class="hp-top"><div><div class="pairtitle">Strategies</div><div class="muted" style="font-weight:600;font-size:12px">Alerts from your TradingView strategies · what to do at your broker, as it happens</div></div>
      <div style="display:flex;gap:8px;align-items:center">${pushBtnHtml()}<button type="button" class="btn" id="stRef">↻ Refresh</button></div></header>
    ${S.stv.err==='missing' ? `<div class="card" style="border-color:var(--amber)"><b>One-time setup:</b> run <code>supabase/migration-strategies.sql</code> in Supabase → SQL Editor, then deploy the <b>strategy-alert</b> function (see “Connect TradingView” below).</div>` : S.stv.err ? `<div class="card" style="border-color:var(--neg)">Could not load: ${esc(S.stv.err)}</div>` : ''}
    ${PUSH.st !== 'on' ? `<div class="card st-push">🔔 <span><b>${esc(PUSH_TXT[PUSH.st] || '')}</b> — turn them on on your phone (in the installed app) so every alert rings there too.</span>${PUSH.st==='off' ? '<button type="button" class="btn btn-primary" data-pushbtn>Turn on</button>' : ''}</div>` : ''}
    <div class="st-cards"><button type="button" class="st-card st-all" data-stf="all" aria-pressed="${f==='all'}"><div class="st-ch"><b>All strategies</b><span>${rows.length} alerts stored</span></div>
      <div class="st-kp"><div><em>${stState(rows).open.length}</em><small>open</small></div><div><em>${stState(rows).pend.length}</em><small>pending</small></div><div><em>${rows.filter(r => ST_ACT.includes(r.ev) && !r.done).length}</em><small>to do</small></div></div></button>${cards}</div>
    <h3 class="st-h">Live now${f!=='all' ? ' · ' + esc((ST_DEF.find(d => d[0]===f) || [0, f])[1]) : ''}</h3>
    ${live.length ? `<div class="st-grid">${live.map(liveCard).join('')}</div>` : '<div class="card fc-empty"><p>No open trade and no pending order.</p></div>'}
    <div class="st-fh"><h3 class="st-h">Alerts</h3><div class="seg" role="group"><button type="button" data-sttodo="0" aria-pressed="${!todo}">All</button><button type="button" data-sttodo="1" aria-pressed="${todo}">To do${nTodo ? ' (' + nTodo + ')' : ''}</button></div></div>
    ${feed.length ? `<div class="st-feed">${feed.map(evCard).join('')}</div>` : `<div class="card fc-empty"><p>${todo ? 'Nothing to do. 🎉' : 'No alerts yet. Connect TradingView below.'}</p></div>`}
    <details class="card st-setup" ${rows.length ? '' : 'open'}><summary><b>Connect TradingView</b> <span class="muted">· one alert per chart</span></summary>
      <ol>
        <li>Supabase → SQL Editor: run <code>supabase/migration-strategies.sql</code> (once).</li>
        <li>Supabase → Edge Functions → new function <b>strategy-alert</b>, paste <code>supabase/functions/strategy-alert/index.ts</code>, turn <b>Verify JWT off</b>, deploy.</li>
        <li>Edge Functions → Secrets: add <b>STRAT_KEY</b> = a long random word. Type it here too: <input class="inp" id="stKey" placeholder="your STRAT_KEY" value="${esc(ls.get('do_st_key', ''))}" style="max-width:220px"> <button type="button" class="btn" id="stCheck">Check setup</button> <button type="button" class="btn" id="stTest">Send a test notification</button><div id="stOut" class="st-sm muted"></div></li>
        <li>TradingView: open the chart with the strategy (BE Swing, BE MACD or BE Intraday) → Alerts → <b>Create alert</b> → Condition: the strategy → <b>alert() function calls only</b> → Expiration: open-ended → Notifications: tick <b>Notify in app</b> and <b>Webhook URL</b>:<pre class="su-code">${esc(hook)}</pre></li>
        <li>One alert per pair and strategy (TradingView limits the number of alerts on your plan). Alerts fire at the close of a chart bar, so on a 1H chart they come at most an hour late; on 5m charts within 5 minutes.</li>
      </ol>
      <p class="muted st-sm">Each alert says what happened, the levels, and what to do at your broker. “lots / $10k” is the size for a $10,000 account at 1% risk: multiply by your account size ÷ 10,000 (FX lots = 100,000 units, gold lots = 100 oz; indices are in contracts of your broker, check them).</p></details>`;
  m.querySelectorAll('[data-stf]').forEach(b => b.onclick = () => { ls.set('do_st_f', b.dataset.stf); renderStrategies(); });
  m.querySelectorAll('[data-sttodo]').forEach(b => b.onclick = () => { ls.set('do_st_todo', b.dataset.sttodo); renderStrategies(); });
  m.querySelectorAll('[data-stdone]').forEach(b => b.onclick = async () => { const id = +b.dataset.stdone; b.disabled = true;
    const { error } = await sb.from('do_strat_events').update({ done:true }).eq('id', id); if(error) { b.disabled = false; return toast(error.message); }
    const r = S.stv.rows.find(x => x.id === id); if(r) r.done = true; renderStrategies(); });
  m.querySelector('#stRef').onclick = async () => { await stLoad(); renderStrategies(); toast('Up to date'); };
  const out = m.querySelector('#stOut'), key = () => (m.querySelector('#stKey').value || '').trim();
  m.querySelector('#stKey').onchange = e => { ls.set('do_st_key', e.target.value.trim()); renderStrategies(); };
  const call = async q => { if(!key()) return toast('Type your STRAT_KEY first'); ls.set('do_st_key', key()); out.textContent = '…';
    try{ const r = await fetch(`${SUPABASE_URL}/functions/v1/strategy-alert?key=${encodeURIComponent(key())}&${q}=1`); out.textContent = JSON.stringify(await r.json()).replace(/[{}"]/g, '').replace(/,/g, ' · '); }
    catch(e){ out.textContent = 'Not reachable: ' + (e.message || e) + ' (deployed? Verify JWT off?)'; } };
  m.querySelector('#stCheck').onclick = () => call('check');
  m.querySelector('#stTest').onclick = () => call('test');
  if(PUSH.st === 'checking' && !PUSH.p) PUSH.p = pushCheck().then(() => S.view==='strategies' && renderStrategies());
  m.querySelectorAll('[data-pushbtn]').forEach(b => b.onclick = async () => { await pushToggle(); renderStrategies(); });
}
function stPoll(){
  if(S.stv.timer) return;
  S.stv.timer = setInterval(async () => {
    if(S.view !== 'strategies' || document.hidden) return;
    if(await stLoad() && S.view === 'strategies' && !document.querySelector('#main input:focus')) renderStrategies();
  }, 30000);
}
