// Bias Engine — Discord bot (Supabase Edge Function, single file)
// Slash commands: /eurusd … /xauusd (29 pairs), /usd … /xau (9 assets), /bias (overview)
import nacl from "npm:tweetnacl@1.0.3";

const env = (k: string) => Deno.env.get(k) ?? "";
const PUBLIC_KEY = env("DISCORD_PUBLIC_KEY");
const APP_ID = env("DISCORD_APP_ID");
const BOT_TOKEN = env("DISCORD_BOT_TOKEN");
const GUILD_ID = env("DISCORD_GUILD_ID");
const DATA_URL = env("DATA_URL");
const REGISTER_KEY = env("REGISTER_KEY");

const PAIRS = ["EURUSD","GBPUSD","USDJPY","USDCHF","USDCAD","AUDUSD","NZDUSD","EURGBP","EURJPY","EURCHF","EURAUD","EURNZD","EURCAD","GBPJPY","GBPCHF","GBPAUD","GBPNZD","GBPCAD","AUDJPY","AUDCHF","AUDNZD","AUDCAD","NZDJPY","NZDCHF","NZDCAD","CADJPY","CADCHF","CHFJPY","XAUUSD"];
const ASSETS = ["USD","EUR","GBP","JPY","CHF","CAD","AUD","NZD","XAU"];
const COLOR: Record<string, number> = { bullish: 0x3ba55d, bearish: 0xed4245, neutral: 0xfaa61a, "two-sided": 0xfaa61a };
const DOT: Record<string, string> = { bullish: "🟢", bearish: "🔴", neutral: "🟡", "two-sided": "🟡" };

const sg = (x: number) => (x > 0 ? `+${x}` : `${x}`.replace("-", "−"));
const cap = (s: string) => s.charAt(0).toUpperCase() + s.slice(1);
const hex = (s: string) => new Uint8Array((s.match(/.{1,2}/g) ?? []).map((b) => parseInt(b, 16)));
const json = (o: unknown, status = 200) => new Response(JSON.stringify(o), { status, headers: { "Content-Type": "application/json" } });
const reply = (data: unknown) => json({ type: 4, data });

// deno-lint-ignore no-explicit-any
type D = any;

const period = (d: D) => `Week ${d.week} (${d.valid_label})`;
// Warning shown only when the week is over and no new file has been uploaded yet
function expiredNote(d: D) {
  const expired = Date.now() > new Date(d.valid_to + "T23:59:59Z").getTime();
  return expired ? `⚠️ **EXPIRED** — this analysis was for ${period(d)}. A new one is pending.\n\n` : "";
}

function assetEmbed(d: D, c: string, standalone: boolean) {
  const x = d.currencies[c];
  return {
    color: COLOR[x.bias],
    title: `${x.flag} ${c} ${sg(x.score)} · ${DOT[x.bias]} ${cap(x.bias)}` + (standalone ? ` · ${period(d)}` : ""),
    description: (standalone ? expiredNote(d) : "") + `*${x.name}* — ${x.short}\n*Last week: ${sg(x.prev)} → now ${sg(x.score)}*`,
    fields: [
      { name: "💡 Why", value: x.why.map((w: string) => `• ${w}`).join("\n") },
      { name: "✅ What would make it stronger", value: x.helps },
      { name: "❌ What would make it weaker", value: x.hurts },
      { name: "🗓 Events this week", value: x.events.map((w: string) => `• ${w}`).join("\n") },
    ],
  };
}

function pairEmbeds(d: D, p: string) {
  const x = d.pairs[p], b = p.slice(0, 3), q = p.slice(3);
  const head = {
    color: COLOR[x.bias],
    title: `${p} · ${DOT[x.bias]} ${cap(x.bias)} · ${period(d)}`,
    description: expiredNote(d) + x.text + (x.prev_bias !== x.bias ? `\n*Last week this pair was ${x.prev_bias}.*` : ""),
    fields: [
      { name: "Gap", value: `**${sg(x.gap)}**\n${b} ${sg(d.currencies[b].score)} vs ${q} ${sg(d.currencies[q].score)}`, inline: true },
      { name: "Conviction", value: `**${cap(x.conviction)}**`, inline: true },
    ],
  };
  return [head, assetEmbed(d, b, false), assetEmbed(d, q, false)];
}

function overviewEmbed(d: D) {
  const order = Object.keys(d.currencies).sort((a, z) => d.currencies[z].score - d.currencies[a].score);
  const rank = order.map((c, i) => {
    const x = d.currencies[c];
    return `${i + 1}. ${x.flag} **${c} ${sg(x.score)}** · ${DOT[x.bias]} ${x.bias} *(last week ${sg(x.prev)})*`;
  }).join("\n");
  return {
    color: 0x5865f2,
    title: `📈 Bias Engine — ${period(d)} overview`,
    description: expiredNote(d) + d.summary.map((s: string) => `• ${s}`).join("\n"),
    fields: [
      { name: "🏆 Ranking", value: rank },
      { name: "🗓 Key events (Bucharest time)", value: d.key_events.map((s: string) => `• ${s}`).join("\n") },
      { name: "How to use", value: "Type a pair (e.g. `/eurusd`) or an asset (e.g. `/aud`, `/xau`)." },
    ],
  };
}

async function register() {
  const cmds = [
    { name: "bias", description: "Bias Engine: weekly overview and ranking", type: 1 },
    ...PAIRS.map((p) => ({ name: p.toLowerCase(), description: `Fundamental bias for ${p.slice(0, 3)}/${p.slice(3)}`, type: 1 })),
    ...ASSETS.map((c) => ({ name: c.toLowerCase(), description: `Fundamental score for ${c}`, type: 1 })),
  ];
  const r = await fetch(`https://discord.com/api/v10/applications/${APP_ID}/guilds/${GUILD_ID}/commands`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", Authorization: `Bot ${BOT_TOKEN}` },
    body: JSON.stringify(cmds),
  });
  return new Response(r.ok ? `✅ Registered ${cmds.length} commands.` : `❌ Discord said ${r.status}: ${await r.text()}`, {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
}

export async function handle(req: Request): Promise<Response> {
  const url = new URL(req.url);
  if (req.method === "GET") {
    if (REGISTER_KEY && url.searchParams.get("register") === REGISTER_KEY) return await register();
    return new Response("Bias Engine bot is running.");
  }
  const sig = req.headers.get("X-Signature-Ed25519") ?? "";
  const ts = req.headers.get("X-Signature-Timestamp") ?? "";
  const body = await req.text();
  let ok = false;
  try { ok = nacl.sign.detached.verify(new TextEncoder().encode(ts + body), hex(sig), hex(PUBLIC_KEY)); } catch { ok = false; }
  if (!ok) return new Response("invalid request signature", { status: 401 });

  const i = JSON.parse(body);
  if (i.type === 1) return json({ type: 1 }); // Discord PING
  if (i.type !== 2) return json({ error: "unsupported" }, 400);

  let d: D;
  try {
    const r = await fetch(`${DATA_URL}${DATA_URL.includes("?") ? "&" : "?"}t=${Date.now()}`);
    if (!r.ok) throw new Error(String(r.status));
    d = await r.json();
  } catch (e) {
    return reply({ content: `⚠️ Could not load the analysis data (${e}).` });
  }
  const name = String(i.data?.name ?? "").toUpperCase();
  if (name === "BIAS") return reply({ embeds: [overviewEmbed(d)] });
  if (PAIRS.includes(name)) return reply({ embeds: pairEmbeds(d, name) });
  if (ASSETS.includes(name)) {
    return reply({ embeds: [assetEmbed(d, name, true)] });
  }
  return reply({ content: "Unknown command." });
}

if (import.meta.main) Deno.serve(handle);
