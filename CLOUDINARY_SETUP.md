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

3. **Create .env File**
   - Navigate to `scoretracker/scoretracker/` directory
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open the `.env` file and add your Cloudinary credentials:
     ```
     CLOUDINARY_CLOUD_NAME=your_actual_cloud_name
     CLOUDINARY_API_KEY=your_actual_api_key
     CLOUDINARY_API_SECRET=your_actual_api_secret
     ```
   - **Important**: Never commit the `.env` file to git! It's already in `.gitignore`

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
