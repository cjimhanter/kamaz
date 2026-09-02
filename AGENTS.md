# Kamaz gravel site

Small lead site for a family dump-truck business. Read this file before changing product, stack, or copy.

Owner of the truck: the user's father. He works **turnkey**: drives to the quarry, buys the material, delivers it, unloads, collects one payment for stone + haul. Not "transport only". Geography: **Irkutsk and Irkutsk Oblast**.

## Product

v0 is a public landing + request form. A customer should understand in 30 seconds: they do not go to the quarry. They leave a phone number or call. The driver gets the lead while in the cab.

v1 is a lead journal (status, address, amount).

v2 is a private circle of haulier acquaintances (invite-only overflow). Not a public freight exchange. Not Avito. Not Yandex.Gruzovik.

## Hard decisions (do not reopen unless the user asks)

- Copy and UI: Russian.
- Notifications in v0: **VK and MAX only**. Do not add Telegram until v0 is live and the user asks.
- Do not publish quarry prices. They move. Price is spoken on the phone as one sum.
- Volume is "one truck" / cubic meters / sotki in the customer's words. Do not invent tons on the site.
- No card payments, no SPA, no Nuxt, no Postgres, no Redis, no GPS product, no mobile app in v0.
- Do not ship to the public internet until: a real phone is in `.env`, at least one of VK/MAX is configured, and a personal-data consent checkbox exists (phone collection, 152-FZ). Placeholder phone is `+7 900 000-00-00`.
- Hosting later: VPS in Russia, HTTPS, `.ru` domain. Not a foreign PaaS as the default.

## Stack

| Layer | Choice |
| --- | --- |
| App | FastAPI + Jinja2, server-rendered HTML |
| CSS | `app/static/styles.css`, mobile first, sticky call/request bar |
| Leads | SQLite via aiosqlite (`data/leads.db`, gitignored) |
| Config | `.env` via pydantic-settings (`SITE_*`, `VK_*`, `MAX_*`) |
| Notify | `app/notify.py` - VK `messages.send`, MAX `platform-api2.max.ru` |
| Run | `uv`, Python 3.12+ |

Layout:

- `app/main.py` - routes `/`, `/spasibo`, `POST /zayavka`
- `app/templates/` - `base.html`, `index.html`, `thanks.html`
- `app/db.py` - schema + insert
- `app/settings.py` - env
- `README.md` - how to get VK/MAX tokens

Notes in the Obsidian vault (`__temp__/01 Projects/грузоперевозки/`) are background. This repo is the source of truth for building.

## Run

```bash
cp .env.example .env
uv sync
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Without notify tokens, the form still saves to SQLite. Empty VK/MAX credentials must not crash a submit.

## What is still missing

- Real `SITE_PHONE` / `SITE_PHONE_TEL`
- VK and/or MAX tokens (`README.md`)
- Truck photo (placeholder block on the landing)
- Quarry name (only if the father allows it on the site)
- Body volume in cubic meters
- Consent checkbox + short personal-data page
- Docker / Caddy / domain

Next implementation order: phone in env, then notify, then 152-FZ consent, then deploy. Do not start v2 first.

## Engineering rules

- Prefer a thin vertical slice over new frameworks.
- Reproduce bugs as the customer would: open the page, submit the form, check SQLite and (if configured) VK/MAX.
- Keep the landing readable in 30 seconds. Large tap targets. Phone-first.
- Never commit `.env` or `data/leads.db`.
- Do not add the agent name as a git co-author.
- Do not use the em dash character. Use a plain hyphen.
- Do not add tests unless the user asks.
- User-facing answers: if the vault `AGENTS.md` is in context, follow it. Product copy on the site stays Russian even if the agent replies in English.

## Copy tone

Direct, local, not a corporate landing. Honest about what we do not know (price, exact tons). Draft notice in the footer stays until phone and photo are real; remove it at launch.
