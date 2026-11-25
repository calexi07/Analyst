-- Daily Observer · Auto-Analyst — run once in Supabase → SQL Editor
-- Market events from the "BE Auto-Analyst" TradingView indicator, the analyst's notes, and the virtual (paper) trades.

-- 1) what happened on the chart: one row per event (fractal / swing break, liquidity taken, zone created / touched / invalidated …)
--    plus one 'bar' row per closed 1H candle (the price feed for the paper trades)
create table if not exists public.aa_events (
  id        bigserial primary key,
  uid       text unique,                    -- pair|tf|ev|bar_time|n — TradingView retries do not double
  at        timestamptz not null default now(),
  bar_time  timestamptz,                    -- open time of the 1H candle that closed
  pair      text not null,
  tf        text not null,                  -- D / 4H / 1H
  ev        text not null,                  -- bar · frac_bos · frac_choch · swing_bos · swing_choch · liq · zone_new · zone_touch · zone_break · pd
  dir       int,                            -- +1 bullish / -1 bearish (for liq: -1 = a low was taken, +1 = a high was taken)
  price     double precision,               -- close of the 1H candle
  level     double precision,               -- the broken / taken level
  zlo       double precision,               -- zone low (zone events)
  zhi       double precision,               -- zone high
  info      jsonb,                          -- extra fields (o/h/l/c for bars, liquidity name, zone kind, state snapshot …)
  raw       text
);
create index if not exists aa_events_pair_at on public.aa_events (pair, bar_time desc);
create index if not exists aa_events_ev on public.aa_events (ev);

-- 2) the analyst's notes: morning plan, confirmation, end-of-day review
create table if not exists public.aa_notes (
  id         bigserial primary key,
  created_at timestamptz not null default now(),
  pair       text not null,
  day        date not null,                 -- trading day (Europe/Bucharest)
  kind       text not null,                 -- plan · confirm · close
  model      text,
  text       text,                          -- the readable analysis (markdown)
  data       jsonb,                         -- structured output (watch list, setup, verdict, lessons …)
  context    jsonb                          -- what the analyst was given (for audit: nothing is rewritten after the fact)
);
create index if not exists aa_notes_pair_day on public.aa_notes (pair, day desc);

-- 3) virtual trades opened from confirmed setups, managed automatically from the 1H bars
create table if not exists public.aa_paper (
  id         bigserial primary key,
  created_at timestamptz not null default now(),
  pair       text not null,
  day        date,
  note_id    bigint references public.aa_notes(id) on delete set null,
  setup      text,                          -- short name of the setup
  dir        int not null,                  -- +1 long / -1 short
  order_type text default 'limit',          -- limit · market
  entry      double precision not null,
  sl         double precision not null,
  tp         double precision not null,
  status     text not null default 'pending', -- pending · open · won · lost · expired · cancelled
  expires_at timestamptz,                   -- a pending order not filled by then is expired
  opened_at  timestamptz,
  closed_at  timestamptz,
  exit_price double precision,
  r          double precision,
  why        text
);
create index if not exists aa_paper_pair on public.aa_paper (pair, status);

alter table public.aa_events enable row level security;
alter table public.aa_notes  enable row level security;
alter table public.aa_paper  enable row level security;
drop policy if exists "aa_events read" on public.aa_events;
drop policy if exists "aa_notes read"  on public.aa_notes;
drop policy if exists "aa_paper read"  on public.aa_paper;
drop policy if exists "aa_paper edit"  on public.aa_paper;
create policy "aa_events read" on public.aa_events for select to anon using (true);
create policy "aa_notes read"  on public.aa_notes  for select to anon using (true);
create policy "aa_paper read"  on public.aa_paper  for select to anon using (true);
create policy "aa_paper edit"  on public.aa_paper  for update to anon using (true) with check (true);   -- cancel a pending order from the app
-- inserts come only from the aa-event and aa-analyst functions (service role)
