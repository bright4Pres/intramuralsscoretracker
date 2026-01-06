# PythonAnywhere Deployment Guide

## Files to Upload

1. Upload your entire `scoretracker` project folder
2. Make sure these files are included:
   - `requirements.txt`
   - `db.sqlite3` (your database with team data)
   - All Django files

## Step-by-Step Deployment

### 1. Create PythonAnywhere Account
- Go to https://www.pythonanywhere.com
- Sign up for a free account
- Note your username (e.g., `yourname`)

### 2. Upload Files
Go to **Files** tab:
```
/home/yourname/scoretracker/
```
Upload all your project files there.

### 3. Create Virtual Environment
Open a **Bash console**:
```bash
cd ~
python3.10 -m venv myenv
source myenv/bin/activate
pip install -r scoretracker/requirements.txt
```

### 4. Configure Web App
Go to **Web** tab → "Add a new web app":
- Choose "Manual configuration"
- Python 3.10
- Click Next

### 5. Configure WSGI File
In the **Web** tab, click on the WSGI configuration file link.

Replace everything with:
```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/YOURUSERNAME/scoretracker/scoretracker'
if path not in sys.path:
    sys.append(path)

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'scoretracker.settings'

# Activate virtual environment
activate_this = '/home/YOURUSERNAME/myenv/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Replace `YOURUSERNAME` with your actual PythonAnywhere username!**

### 6. Set Virtual Environment Path
In the **Web** tab, under "Virtualenv":
```
/home/YOURUSERNAME/myenv
```

### 7. Configure Static Files
In the **Web** tab, under "Static files":
- URL: `/static/`
- Directory: `/home/YOURUSERNAME/scoretracker/scoretracker/static`

### 8. Update Django Settings
Edit `settings.py`:
```python
# Add your PythonAnywhere domain
ALLOWED_HOSTS = ['YOURUSERNAME.pythonanywhere.com', 'localhost', '127.0.0.1']

# Optional: Set DEBUG to False for production
DEBUG = False  # Change to False after testing
```

### 9. Initialize Database
In Bash console:
```bash
cd ~/scoretracker/scoretracker
source ~/myenv/bin/activate
python manage.py migrate
python manage.py init_teams
```

### 10. Reload Web App
- Go back to **Web** tab
- Click the big green **Reload** button

## Your Site Will Be Live At:
```
https://YOURUSERNAME.pythonanywhere.com
```

## Admin Dashboard Access:
```
https://YOURUSERNAME.pythonanywhere.com/admin-login/
Password: ZRC2026!intramsnibright
```

## Updating Your Site Later

When you make changes:
1. Upload changed files via **Files** tab
2. Click **Reload** button on **Web** tab

## Troubleshooting

If something goes wrong:
- Check the **Error log** in the Web tab
- Check the **Server log** in the Web tab
- Make sure all paths use your correct username
- Make sure database file has correct permissions

## Free Tier Limits
- Renew every 3 months (they'll email you)
- No sleep/hibernation (always-on!)
- 512 MB storage
- 100k daily hits (plenty for intramurals)
