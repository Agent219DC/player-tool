# Roster Lab

Transfer-portal grading board for football staff.

Live site: https://agent219dc.github.io/roster-lab/

- `index.html` – the whole app (one page). Data and sign-in run on Firebase project `marshall-player-tool`.
- `firestore.rules` – database security rules. Paste into Firebase → Firestore → Rules and Publish whenever this file changes.

Only signed-in staff on the owner's Staff access list can read or write the board. Player data is never stored in this repository.
