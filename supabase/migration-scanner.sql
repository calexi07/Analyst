-- Daily Observer — Scanner (BE Tunnel SMC v20 → webhook scan-event)
-- One row per pair per scan slot (scan_rows), one row per slot with the written summary (scan_runs).
-- Run once in the Supabase SQL editor.

create table if not exists scan_rows (
  id          bigserial primary key,
  uid         text unique not null,            -- PAIR|slot ms (|test)
  slot        timestamptz not null,            -- close time of the candle that ends at the scan hour
  hour_local  int,                             -- Europe/Bucharest hour of the slot
  pair        text not null,
  test        boolean default false,
  cls         text,                            -- watch / late / done / unclear (rule-based, in code)
  rank_score  numeric,                         -- ordering inside a class
  why         text,                            -- one-line reason built by the rules
  data        jsonb,                           -- the indicator message as sent
  created_at  timestamptz default now()
);
create index if not exists scan_rows_slot on scan_rows (slot desc);
create index if not exists scan_rows_pair on scan_rows (pair, slot desc);

create table if not exists scan_runs (
  slot        timestamptz primary key,
  hour_local  int,
  test        boolean default false,
  status      text default 'waiting',          -- waiting / done / error
  n           int,
  summary     text,
  model       text,
  error       text,
  created_at  timestamptz default now(),
  done_at     timestamptz
);

alter table scan_rows enable row level security;
alter table scan_runs enable row level security;
-- the site reads with the anon key (same as the other Daily Observer tables); only the edge function (service role) writes
drop policy if exists scan_rows_read on scan_rows;
create policy scan_rows_read on scan_rows for select to anon, authenticated using (true);
drop policy if exists scan_runs_read on scan_runs;
create policy scan_runs_read on scan_runs for select to anon, authenticated using (true);

-- v2 (per-pair AI analysis on the Scanner cards): run this part once if the tables already exist
alter table scan_rows add column if not exists ai text;
alter table scan_rows add column if not exists ai_model text;
alter table scan_rows add column if not exists ai_at timestamptz;
