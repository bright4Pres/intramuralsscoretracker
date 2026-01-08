# Cloudinary Setup Instructions

This project uses Cloudinary to store contestant photos and advocacy videos.

## Setup Steps:

1. **Create a Cloudinary Account**
   - Go to https://cloudinary.com/
   - Sign up for a free account

2. **Get Your Credentials**
   - After logging in, go to your Dashboard
   - You'll see your credentials:
     - Cloud Name
     - API Key
     - API Secret

3. **Update settings.py**
   - Open `scoretracker/scoretracker/settings.py`
   - Find the `CLOUDINARY_STORAGE` section (around line 135)
   - Replace the placeholder values:
     ```python
     CLOUDINARY_STORAGE = {
         'CLOUD_NAME': 'your_cloud_name',  # Replace with your actual cloud name
         'API_KEY': 'your_api_key',        # Replace with your actual API key
         'API_SECRET': 'your_api_secret',  # Replace with your actual API secret
     }
     ```

4. **Test the Setup**
   - Go to the Django admin panel: http://localhost:8080/admin/
   - Navigate to Contestants
   - Try uploading a photo - it should upload to Cloudinary
   - Try uploading a video - it should upload to Cloudinary

## Features:

- **Photos**: Uploaded to Cloudinary and displayed on contestant cards
- **Advocacy Videos**: Uploaded to Cloudinary and played when clicking on a card
- **Empire Styling**: Each card is styled with their empire's colors and banner
- **Click Interaction**: 
  - Click on a contestant's card to view their advocacy video
  - Other cards fade out while the video plays
  - Click the X or outside the modal to close and return to the carousel

## Card Display:

- Cards display the contestant's name at the bottom
- Each card has a border colored based on their empire (Shinobi=red, Pegasus=yellow, Chimera=indigo, Phoenix=orange)
- Empire banners appear behind each card with transparency
- Cards are arranged in a circular carousel that you can drag to rotate

## Admin Panel:

Use the Django admin to add contestants:
1. Go to http://localhost:8080/admin/
2. Click on "Contestants"
3. Add a new contestant with:
   - Name
   - Empire (select from dropdown)
   - Photo (upload image to Cloudinary)
   - Advocacy Video (upload video to Cloudinary)
   - Order (number for carousel ordering)
   - Is Active (checkbox to show/hide)
