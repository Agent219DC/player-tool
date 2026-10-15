# Player Tool repo notes

- `index.html` is the entire app: the shared Player Tool page plus a Firebase shim (sign-in gate, `window.claude.use()` stand-in for db/user/downloads). Edit it directly.
- Owner email is set in two places: `OWNER_EMAIL` in index.html and `isOwner()` in firestore.rules. Keep them in sync.
- Staff emails live in Firestore at `config/staff` (`emails` array), managed from Owner tools → Staff access.
- Never commit player data or backup JSON files; this repo is public.
- After changing `firestore.rules`, tell the owner to paste it into Firebase → Firestore → Rules → Publish.
