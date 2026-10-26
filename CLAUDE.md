# Player Tool repo notes

- `index.html` is the entire app: the shared Player Tool page plus a Firebase shim (sign-in gate, `window.claude.use()` stand-in for db/user/downloads). Edit it directly.
- Owner email is set in two places: `OWNER_EMAIL` in index.html and `isOwner()` in firestore.rules. Keep them in sync.
- Staff emails live in Firestore at `config/staff` (`emails` array), managed from Owner tools → Staff access.
- Never commit player data or backup JSON files; this repo is public.
- After changing `firestore.rules`, tell the owner to paste it into Firebase → Firestore → Rules → Publish.
- Pages are tabs (`data-page` on each section, `go(tab)` router, `#tab` in the URL). Owner-only data (budget, asking prices) lives in Firestore `owner/*`, which the rules restrict to the owner; never put money in `config/`, `shared/` or player docs.
- Depth charts live in `shared/depth` (this season) and `shared/depth_next`; saves send only changed spots (`groups.<spot>`). Starters on Overview and the Big Board come from each spot's depth chart #1.
- Trademark rule (owner's call): the Marshall logo is used inside the website (header, school logos) and on the PDF printouts, which the owner approved. Never use it for the favicon, home-screen/app icons, or anywhere else outside the site without asking the owner first.
- Player cards show ESPN headshots (`headshotHtml`, initials fallback) for players with an `espnId`.
- Player cards load ESPN live on open (`fillEspnLive`): season line, game log, and totals vs. FBS opponents (FBS team ids from ESPN's core API, cached in localStorage). Nothing from it is saved to Firestore.
- School logos come from ESPN team search (`teamDrain`, cached per browser); ESPN's full team list is blocked by CORS.
- Coach notes live on each player doc as `notes[]` ({id,t,at,by,byName}); staff can add, authors (and the owner) can delete. Form saves carry `notes` over (`withTrend`), so editing a player never drops them.
- High School side: the header's Portal / High School switch flips the tab row. HS tabs are `hsboard`, `hsbig`, `hsset` (the `HS` module near the end of index.html). Prospects live in Firestore `hs_players` (covered by the existing `*_players` rule); HS settings live in `config/hs` (owner writes). Film grades are stored per coach on each prospect as `film.<uid>`. Prospect import files (.json) are loaded from HS Settings and must never be committed here.
- HS extras: Prospect board order is `hsRank` on each prospect; `star` (same field and ☆/★ look as the portal) and coach `notes[]` live on the prospect too (an old string `notes` shows as a "Profile note"). Imports never overwrite hsRank, priority, notes or film. HS Needs (`hsneeds` tab) reads/writes `config/hs.needs` as `{<class>:{QB:n,...}}`, falling back to `NEED_DEF`. The Prospects list uses portal-style row checkboxes for Compare selected (2–4) and Print selected. `ignoreTests` (array of test keys) on a prospect is a staff call to not count a test; imports never overwrite it. The Settings backup includes `hs_players` and `config/hs`. The header search covers portal and HS (`HS.search`, `HS.open`).
