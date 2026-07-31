# Zifang secrets hygiene

This is a local operations note for credentials used by the untracked Supabase admin scripts.

## Current rule

- Public client credentials that are meant to ship in the browser stay in `index.html`.
- Supabase `service_role` credentials do **not** live inline in scripts.
- Local upload/migration scripts read credentials from the untracked project-root `.env`.

## Required env vars

- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`

## Local workflow

1. Keep the real values only in `/Users/cubicleaf/Documents/Chinese shit/.env`.
2. Run upload or migration scripts from the project root so they can read that file.
3. If a script says a required env var is missing, restore or recreate `.env` before retrying.

## Rotation posture

- As of 2026-07-31, no public leak is confirmed.
- Rotation is hygiene-only unless a real exposure is later confirmed.
- If a leak is ever confirmed, rotate the key in Supabase first, then update `.env`, then rerun any admin scripts as needed.

## Why the scripts stay gitignored

Even without inline secrets, they are local admin tooling and should not be swept into the public repo by accident.
