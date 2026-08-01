-- Run once in Supabase Dashboard > SQL Editor for Horizon player search.
create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text not null,
  avatar_color integer not null default 0 check (avatar_color between 0 and 2),
  status text not null default 'Ready to play',
  created_at timestamptz not null default now()
);

alter table public.profiles enable row level security;
drop policy if exists "Profiles can be searched" on public.profiles;
create policy "Profiles can be searched" on public.profiles for select to authenticated using (true);
drop policy if exists "Players edit their profile" on public.profiles;
create policy "Players edit their profile" on public.profiles for update to authenticated using (auth.uid() = id) with check (auth.uid() = id);

create or replace function public.create_horizon_profile()
returns trigger language plpgsql security definer set search_path=public as $$
begin
  insert into public.profiles(id,display_name)
  values(new.id,coalesce(new.raw_user_meta_data->>'display_name',split_part(new.email,'@',1)))
  on conflict(id) do nothing;
  return new;
end; $$;

drop trigger if exists horizon_profile_on_signup on auth.users;
create trigger horizon_profile_on_signup after insert on auth.users
for each row execute function public.create_horizon_profile();

insert into public.profiles(id,display_name)
select id,coalesce(raw_user_meta_data->>'display_name',split_part(email,'@',1)) from auth.users
on conflict(id) do nothing;

create table if not exists public.friend_requests (
  sender_id uuid not null references auth.users(id) on delete cascade,
  receiver_id uuid not null references auth.users(id) on delete cascade,
  status text not null default 'pending' check (status in ('pending','accepted','declined')),
  created_at timestamptz not null default now(),
  primary key(sender_id,receiver_id),
  check(sender_id <> receiver_id)
);
alter table public.friend_requests enable row level security;
drop policy if exists "Players view their requests" on public.friend_requests;
create policy "Players view their requests" on public.friend_requests for select to authenticated using (auth.uid()=sender_id or auth.uid()=receiver_id);
drop policy if exists "Players send requests" on public.friend_requests;
create policy "Players send requests" on public.friend_requests for insert to authenticated with check (auth.uid()=sender_id);
drop policy if exists "Players manage received requests" on public.friend_requests;
create policy "Players manage received requests" on public.friend_requests for update to authenticated using (auth.uid()=receiver_id);
