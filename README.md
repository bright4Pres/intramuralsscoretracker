# Score Tracker - Intramural Competition

A real-time scoreboard application for tracking intramural competition scores across four teams.

## Teams
- **Shinobi** (Purple)
- **Pegasus** (Blue)
- **Chimera** (Red)
- **Phoenix** (Orange)

## Setup

1. Create virtual environment and install Django:
```bash
python -m venv .env
.env\Scripts\activate  # On Windows
pip install django
```

2. Run migrations:
```bash
cd scoretracker
python manage.py migrate
```

3. Initialize teams:
```bash
python manage.py init_teams
```

4. Run the server:
```bash
python manage.py runserver
```

## Usage

### Public Scoreboard
- Visit: `http://localhost:8000/`
- Real-time updates every 2 seconds
- No login required

### Admin Dashboard
- Visit: `http://localhost:8000/admin-login/`
- **Default Password:** `admin123`
- Features:
  - Add points to any team
  - Reset all scores
  - View current scores
  - Real-time updates

### Changing the Admin Password

Edit the `ADMIN_PASSWORD` variable in `scoretracker/scoring/views.py`:

```python
ADMIN_PASSWORD = "your_new_password_here"
```

## API Endpoints

- `GET /api/scores/` - Get current scores for all teams
- `POST /api/add-points/` - Add points to a team
- `POST /api/reset-scores/` - Reset all scores to 0

## Features

- ✅ Real-time score updates without page refresh
- ✅ Password-protected admin dashboard
- ✅ SQLite database for score persistence
- ✅ Responsive design
- ✅ Animated score changes
- ✅ Session-based authentication
