-- Daily Observer · Strategies (TradingView strategy alerts) — run once in Supabase → SQL Editor
create table if not exists public.do_strat_events (
  id         bigserial primary key,
  uid        text unique,                      -- strategy|pair|event|trade|what|bar: TradingView retries do not double
  at         timestamptz not null default now(),
  bar_time   timestamptz,
  strategy   text not null,                    -- SWING / MACD / INTRADAY (UNKNOWN = message the function could not read)
  variant    text,                             -- e.g. "SWING 4H"
  pair       text,
  tf         text,
  ev         text not null,                    -- order · open · filled · cancel · move · partial · closenow · closed
  dir        int,
  trade_id   text,                             -- the strategy's entry id (L / S / EU L / NY S / PB L …)
  what       text,                             -- STOP / LIMIT / MARKET, or the exit / move reason
  entry      double precision,
  sl         double precision,
  tp         double precision,
  price      double precision,
  r          double precision,
  lots10k    double precision,                 -- lots for a $10k account at 1% risk
  push       boolean default true,
  title      text,
  body       text,
  raw        text,
  done       boolean default false             -- ticked in the app ("I did it")
);
create index if not exists do_strat_events_at on public.do_strat_events (at desc);
alter table public.do_strat_events enable row level security;
drop policy if exists "do_strat_events read" on public.do_strat_events;
drop policy if exists "do_strat_events tick" on public.do_strat_events;
drop policy if exists "do_strat_events clear" on public.do_strat_events;
create policy "do_strat_events read"  on public.do_strat_events for select to anon using (true);
create policy "do_strat_events tick"  on public.do_strat_events for update to anon using (true) with check (true);
create policy "do_strat_events clear" on public.do_strat_events for delete to anon using (true);
-- inserts come only from the strategy-alert function (service role)
