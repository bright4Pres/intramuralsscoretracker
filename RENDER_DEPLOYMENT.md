# Render Deployment Guide for Score Tracker

## Prerequisites
1. GitHub account
2. Render account (sign up at https://render.com)
3. Cloudinary account with API credentials

## Step 1: Push to GitHub

1. Initialize git if not already done:
```bash
cd /path/to/scoretracker
git init
git add .
git commit -m "Prepare for Render deployment"
```

2. Create a new repository on GitHub

3. Push your code:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

## Step 2: Create PostgreSQL Database on Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Fill in:
   - **Name**: `scoretracker-db`
   - **Database**: `scoretracker`
   - **User**: (auto-generated)
   - **Region**: Choose closest to you
   - **Plan**: Free
4. Click **"Create Database"**
5. Wait for it to provision (2-3 minutes)
6. Copy the **Internal Database URL** (starts with `postgresql://`)

## Step 3: Create Web Service on Render

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Fill in:
   - **Name**: `scoretracker` (or your preferred name)
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: (leave blank)
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn scoretracker.scoretracker.wsgi:application`
   - **Plan**: Free

## Step 4: Set Environment Variables

In the Render dashboard for your web service, go to **"Environment"** tab and add:

```
SECRET_KEY = your-secret-key-here-generate-a-new-one
DEBUG = False
ALLOWED_HOSTS = your-app-name.onrender.com
DATABASE_URL = (paste the Internal Database URL from Step 2)
CLOUDINARY_CLOUD_NAME = dwiynqoyd
CLOUDINARY_API_KEY = 628443394577536
CLOUDINARY_API_SECRET = IPwWMyr8WCX8WsJg8FHE_rmvjJ8
```

**Generate a new SECRET_KEY**:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Step 5: Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Run migrations
   - Collect static files
   - Start your application
3. Wait 5-10 minutes for first deploy

## Step 6: Create Superuser

After deployment, you need to create an admin user:

1. In Render dashboard, go to your web service
2. Click **"Shell"** tab
3. Run:
```bash
cd scoretracker
python manage.py createsuperuser
```

## Step 7: Keep App Awake (Optional)

Render free tier apps sleep after 15 minutes of inactivity.

### Using UptimeRobot (Recommended):
1. Sign up at https://uptimerobot.com
2. Add new monitor:
   - **Type**: HTTP(s)
   - **URL**: `https://your-app-name.onrender.com/health/`
   - **Interval**: 5 minutes
3. Done! Your app will stay awake

## Your Live URLs

After deployment:
- **Main Site**: `https://your-app-name.onrender.com/`
- **Admin Panel**: `https://your-app-name.onrender.com/admin/`
- **Health Check**: `https://your-app-name.onrender.com/health/`

## Troubleshooting

### Build fails
- Check logs in Render dashboard
- Ensure `build.sh` has execute permissions: `chmod +x build.sh`
- Verify all dependencies in `requirements.txt`

### Database connection error
- Verify DATABASE_URL is correct in environment variables
- Use Internal Database URL, not External

### Static files not loading
- Check that `STATIC_ROOT` is set correctly
- Verify WhiteNoise is in MIDDLEWARE
- Run `python manage.py collectstatic` manually in Shell

### Cloudinary uploads fail
- Verify all three Cloudinary credentials in environment variables
- Check Cloudinary account is active

## Updating Your App

To deploy updates:
```bash
git add .
git commit -m "Your update message"
git push origin main
```

Render will automatically redeploy!

## Important Notes

1. **Never commit `.env` file** - it's in `.gitignore`
2. **Use Render environment variables** for sensitive data
3. **Database backups** - Render free PostgreSQL doesn't include automatic backups
4. **Free tier limitations**:
   - Apps sleep after 15 minutes
   - 750 hours/month of running time
   - Database: 1GB storage limit

## Support

- Render Docs: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
