-- Daily Observer — structure feed from the "BE FSB Export" TradingView indicator (webhook fsb-event)
-- One row per pair per closed 1H candle: OHLC + the 51 export columns (same order as the TradingView CSV export).
-- Rows older than 35 days are deleted by the edge function itself. Run once in the Supabase SQL editor.

create table if not exists fsb_bars (
  pair        text not null,
  bar_time    timestamptz not null,            -- open time of the 1H candle
  o           numeric, h numeric, l numeric, c numeric,
  v           jsonb not null,                  -- array of 51 values (null = empty), CSV order
  created_at  timestamptz default now(),
  primary key (pair, bar_time)
);
create index if not exists fsb_bars_time on fsb_bars (bar_time desc);

alter table fsb_bars enable row level security;
-- the GitHub export and the site read with the anon key; only the edge function (service role) writes
drop policy if exists fsb_bars_read on fsb_bars;
create policy fsb_bars_read on fsb_bars for select to anon, authenticated using (true);
