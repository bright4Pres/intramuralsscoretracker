# Panagsangka Intramural Scoreboard

A real-time scoreboard and leaderboard system built for the Panagsangka 2026 intramural games at PSHS-ZRC. Tracks points across four teams (Shinobi, Pegasus, Chimera, Phoenix) across sports, esports, LITMUS events, minigames, and Mr. & Miss Pisay.

Built with Django. No frontend framework, just Django templates, vanilla JS, and a REST-ish API that the frontend polls every few seconds.

---

## What it does

**Main scoreboard (`/`)** -- big four-quadrant display showing each team's current points. Has a countdown timer that shows "Panagsangka 2026 Starting Soon..." until the event date. Once the countdown hits zero it hides itself and shows the scoreboard. Points update in real time via polling.

**Leaderboard (`/leaderboard/`)** -- tabbed view showing all games and their current placements. Tabs for Sports, Esports, LITMUS, Mr. & Miss Pisay, and Minigames. Each game row shows team logos for 1st/2nd/3rd/4th place with gold/silver/bronze borders. Placement data is pulled from the API every 5 seconds. The Mr. & Miss Pisay tab has a special awards section below each event showing individual awards (Best in Evening Gown, etc.) with 5 points each.

**Score logs (`/logs/`)** -- table of every scoring action with timestamp, team, points, event, and result. Shows relative timestamps ("2h ago", "Yesterday, 3:00 PM"). Updates every 2 seconds.

**Admin dashboard (`/admin/`)** -- password protected (single hardcoded password). Lets you set game placements and award points. Setting a game result automatically calculates points from the game's point structure and logs everything.

---

## Data models

**Team** -- four teams: shinobi, pegasus, chimera, phoenix. Each has a name, points total, and color hex. Points are updated directly on the model whenever scoring actions happen.

**Game** -- represents a single event/competition. Has a type (sports/litmus/minigame), a category (major/minor), and a point structure for each placement (1st, 2nd, 3rd, 4th, DQ). Games are seeded into the database, not created through the UI.

**GameResult** -- maps a team to a placement in a game. Unique per game+team combination. The `save()` method auto-calculates and adds points to the team when a new result is created. The `delete()` method refunds those points. This means you shouldn't manually edit GameResult rows in the DB without understanding the side effects.

**ScoreLog** -- append-only log of every scoring action. Stores team, points, event name, opponent (if applicable), scores, reason (for deductions), and timestamp. Nothing deletes from this table except a full reset.

**SpecialAward** -- for Mr. & Miss Pisay events specifically. Each award (e.g., "Best in Formal Wear") is tied to a game and a team. Each award is worth 5 points. The `save()` method handles changing the team assignment by refunding the old team and awarding the new one, so you can reassign awards safely.

---

## API endpoints

All the frontend polling goes through these:

```
GET  /api/scores/          -- current points for all teams
GET  /api/logs/            -- full score log history
GET  /api/game-results/    -- all game placements, keyed by game ID
GET  /api/special-awards/<game_id>/  -- special awards for a specific game

POST /api/add-points/      -- manually add/deduct points to a team
POST /api/add-game-result/ -- set a team's placement in a game (auto-calculates points)
POST /api/set-game-result/ -- set multiple placements for a game at once (admin use)
POST /api/reset/           -- reset all scores and clear logs
POST /api/add-special-award/       -- assign a special award to a team
POST /api/delete-special-award/<id>/  -- clear a special award assignment
```

There's no token auth on the POST endpoints, they just check the session for `is_admin`. The admin session is set by logging in at `/admin/login/` with the hardcoded password.

---

## How scoring works

When you set a game result through the admin, it:

1. Creates or updates a `GameResult` record
2. The model's `save()` method looks up the point value for that placement from the `Game` record
3. Adds those points directly to the `Team.points` field
4. Creates a `ScoreLog` entry for the record

If you delete a game result, the `delete()` method runs the reverse -- subtracts the points and logs the refund.

For manual point adjustments (the `add_points` endpoint), it skips the game result system entirely and just directly modifies `Team.points` and logs it. This is also how deductions work -- you pass a negative points value with a required reason field.

Special awards work similarly to game results but live on the `SpecialAward` model. Reassigning an award to a different team automatically refunds the old team.

---

## Tech stack

- Django (Python)
- SQLite
- Vanilla JS with `setInterval` polling (no websockets)
- `Black Ops One` from Google Fonts
- Canvas Confetti (loaded from CDN, used on the scoreboard)
- No build step, no bundler

---

## Setup

```bash
git clone https://github.com/yourusername/panagsangka.git
cd panagsangka

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install django

python manage.py migrate
python manage.py runserver
```

You'll need to seed the teams and games into the database. The four teams need to exist in the `Team` table before anything works. You can do this through the Django admin (`/django-admin/`) after creating a superuser, or write a data migration / management command to seed them.

```bash
python manage.py createsuperuser
```

The admin password for the custom dashboard is hardcoded in `views.py`:

```python
ADMIN_PASSWORD = "ZRC2026!intramsnibright"
```

Change this before deploying obviously.

---

## Countdown timer

The target date is hardcoded in `home.html`:

```javascript
const targetDate = new Date('2026-01-18T00:00:00').getTime();
```

Change this to whatever the actual event date is. When the countdown hits zero the overlay hides itself and shows the scoreboard underneath.

---

## Notes / known issues

- The admin auth is a single shared password stored in plaintext in `views.py`. It's fine for a one-day event but you'd want something better for anything longer-term.
- Points are stored as a running total on the `Team` model. If you manually edit game results in the database without going through the model's save/delete methods, the team points will get out of sync. Always go through the admin dashboard or the API.
- Esports games (Mobile Legends, Call of Duty Mobile, Valorant) are filtered out of the Sports tab in the leaderboard view and shown in their own Esports tab. This filtering is done by hardcoded name matching in the `leaderboard` view, so if you rename those games in the DB the filter breaks.
- The scoreboard polls every 5 seconds, logs poll every 2 seconds. Fine for a local network event, probably too aggressive for anything over the internet.
- The `home.html` has a serialized team map hardcoded in a `<script type="application/json">` tag with points all set to 0. This looks like it was meant for the JS to use as initial state but the actual points shown on the scoreboard come from the Django template context (`{{ teams.shinobi.points }}`), so the JSON block may be unused or leftover from an earlier version.