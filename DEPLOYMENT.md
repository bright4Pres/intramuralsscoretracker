# PythonAnywhere Deployment Guide (from GitHub)

## Prerequisites

1. Your code is pushed to GitHub
2. PythonAnywhere free account created

## Quick Deploy Steps

### 1. Open Bash Console
Go to PythonAnywhere → **Consoles** tab → Start a new **Bash** console

### 2. Clone Your Repository
```bash
cd ~
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 3. Create Virtual Environment
```bash
python3.10 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

### 4. Setup Database
```bash
cd scoretracker
python manage.py migrate
python manage.py init_teams
cd ~
```

### 5. Configure Web App
Go to **Web** tab → "Add a new web app":
- Choose "Manual configuration"
- Python 3.10
- Click Next

### 6. Set Virtual Environment Path
In the **Web** tab, under "Virtualenv" section:
```
/home/YOURUSERNAME/myenv
```

### 7. Configure WSGI File
In the **Web** tab, click on the WSGI configuration file link.

Replace everything with:
```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/YOURUSERNAME/YOUR_REPO_NAME/scoretracker'
if path not in sys.path:
    sys.path.append(path)

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

**Replace:**
- `YOURUSERNAME` with your PythonAnywhere username
- `YOUR_REPO_NAME` with your GitHub repo name

### 8. Configure Static Files
In the **Web** tab, under "Static files" section, click "Enter URL" and add:
- URL: `/static/`
- Directory: `/home/YOURUSERNAME/YOUR_REPO_NAME/scoretracker/static`

### 9. Update Django Settings
Edit `settings.py` in the bash console:
```bash
cd ~/YOUR_REPO_NAME/scoretracker/scoretracker
nano settings.py
```

Find `ALLOWED_HOSTS` and update:
```python
ALLOWED_HOSTS = ['YOURUSERNAME.pythonanywhere.com', 'localhost', '127.0.0.1']
```

Press `Ctrl+X`, then `Y`, then `Enter` to save.

### 10. Reload Web App
- Go back to **Web** tab
- Click the big green **Reload** button

## Your Site Is Live! 🎉
```
https://YOURUSERNAME.pythonanywhere.com
```

## Admin Dashboard Access:
```
https://YOURUSERNAME.pythonanywhere.com/admin-login/
Password: ZRC2026!intramsnibright
```

## Updating Your Site Later

When you push changes to GitHub:
```bash
cd ~/YOUR_REPO_NAME
git pull
source ~/myenv/bin/activate
pip install -r requirements.txt  # if requirements changed
cd scoretracker
python manage.py migrate  # if models changed
```

Then click **Reload** on the Web tab.

## Common Issues & Fixes

### Issue: "No module named 'scoretracker'"
Fix: Check the path in WSGI file matches your repo name

### Issue: Static files not loading
Fix: Double-check static files path in Web tab

### Issue: Database missing teams
Fix: Run `python manage.py init_teams` in bash console

### Issue: "DisallowedHost" error
Fix: Add your domain to ALLOWED_HOSTS in settings.py

## Free Tier Limits
- Renew every 3 months (they'll email you)
- No sleep/hibernation (always-on!)
- 512 MB storage
- 100k daily hits (plenty for intramurals)
