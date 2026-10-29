# Sunday data refresh (runbook)

The owner runs this every Sunday until the season ends. It updates live data only. Never change site code, settings, colors, statuses the staff set, or anything the owner didn't ask for (see CLAUDE.md, owner rule). Accuracy over speed: check every step before moving on.

## Before starting
- The session must be linked to the owner's computer, and the built-in browser must be signed in to:
  - PFF Ultimate (`ultimate.pff.com`)
  - Tracking Football
  - NextGen Prospect
  - Roster Lab (`agent219dc.github.io/roster-lab`), as the owner
- If a site isn't signed in, or its sign-in has expired, skip that part. Say so in the report; never guess data.
- Keep Firestore reads modest. Open Roster Lab once and reuse that tab. Never reload it in a loop. Never load test copies of the site.
- Back up first. Before writing anything, save a JSON snapshot of every doc you'll touch to the run's scratch folder: the `*_players` collections, `hs_players`, `analytics/sbc` and `shared/season`. If a write goes wrong, restore from it.

## 1. Marshall games played
- Look up Marshall's current record, for example on warrennolan.com.
- Set `shared/season.teamGames` to the number of games played.

## 2. Portal boards (all 11 position boards, targets and our own players)
- Every board doc has `pffId`, `season` and `thru` (games played by his team).
- In PFF Ultimate, find the stats API the site uses: open a player's season page and watch the network requests. Then pull 2026 regular-season data for each `pffId`.
- Group the rows the way `tools/pff_metrics.py` expects and compute `db` and `m` with `metrics(p, k)`. `k` is the board key: QB, RB, WR, TE, IOL, OT, DT, DE, LB, SAF or CB.
- Set `thru` to his team's games played through this week.
- Only update players whose `db`, `m` or `thru` changed.
- Write the update through the site's own logic, in the Roster Lab tab, so grade history and the trend arrow stay right:
  - `ex` = the current doc
  - `p` = a clone of `ex` with the new `db`, `m` and `thru`
  - run `withTrend(p, ex)`
  - set `p.updatedAt` and `p.updatedBy` = owner uid
  - write `p` to `<k>_players/<id>`
- Never touch `notes`, `status`, `star`, `role`, `elig` or any other staff field.
- Skip docs with `ref` or `deleted`.
- Report players with no PFF match, or with stats that look off. The site's `oddStats(p)` flags values far outside the usual range.

## 3. High school board (2027 class: commits plus every offer)
- Each prospect has `src.tf` (Tracking Football slug) and `src.ng` (NextGen key).
- Pull the latest Tracking Football and NextGen data for every prospect. Also pull any new Marshall offers or commits.
- Build one JSON array in the same shape as the existing `hs_players` docs. Open a few docs to copy the field names: `tests[]`, `outside.tf`, `outside.ng`, `offers`, `p4`, `commitTo`, `pulledAt`, `sources` and so on.
- Import it through the site: Settings → High school model → Import prospects. Set the file on `#hsImportFile` with a DataTransfer and fire `change`.
- The import never overwrites film, notes, position, status, `hsRank`, star, Hudl, recruiting data or staff corrections.
- Report new offers, commits, decommits, and new test results.

## 4. Sun Belt snapshot
- Update the 2026 two-deeps and the portal class in `analytics/sbc` from PFF, in the structure described in CLAUDE.md. Keep staff position calls. A player with `posNote` keeps his staff-set `pos` and `k` (for example, Jalen Slappy is OT, Braydin Ward is DE), and the two-deep is built with him at that position. A player with `staffDep` stays starter (1) or backup (2) whatever his snaps say, and `nic` stays as set for Marshall (staff calls: Braydin Ward DE starter over Cole Funderburk, Josh Pierre-Louis nickel, Brayden Hall outside CB).
- Update team records, then set `dataAsOf` and `recAsOf`.
- Never write budgets there. Budgets live in `owner/sbc` only.
- Don't press "Update portal odds" unless the owner asks.

## 5. Check, then report
- Re-open each page once and confirm there are no errors and no blank or NaN values.
- Spot-check 5 updated players against PFF.
- Send the owner a short summary: what was updated, grade moves of 3 or more points, new offers and commits, anything skipped and why, and anything that looked wrong.
