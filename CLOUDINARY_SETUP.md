# Cloudinary Setup Guide

## Quick Start

### 1. Create Cloudinary Account
1. Go to [cloudinary.com](https://cloudinary.com)
2. Sign up for a free account
3. Verify your email

### 2. Get Your Credentials

After logging in to your Cloudinary dashboard:

1. **Cloud Name**: Found at the top of your dashboard
   - Example: `my-photography-site`

2. **Create Upload Preset**:
   - Go to Settings → Upload
   - Scroll to "Upload presets"
   - Click "Add upload preset"
   - Set these options:
     - **Preset name**: `photography_upload` (or any name you like)
     - **Signing mode**: Select **"Unsigned"** (important!)
     - **Folder**: `photography-portfolio` (optional)
     - **Use filename**: Yes
     - **Unique filename**: Yes
   - Click "Save"

### 3. Update Your Configuration

Open `cloudinary-uploader.js` and replace the placeholder values:

```javascript
const cloudinaryUploader = new CloudinaryUploader({
    cloudName: 'YOUR_CLOUD_NAME',           // Replace with your cloud name
    uploadPreset: 'YOUR_UNSIGNED_PRESET',   // Replace with your preset name
    folder: 'photography-portfolio'
});
```

### Example Configuration

```javascript
const cloudinaryUploader = new CloudinaryUploader({
    cloudName: 'my-photography-site',      // Your actual cloud name
    uploadPreset: 'photography_upload',     // Your actual preset name
    folder: 'photography-portfolio'
});
```

## How It Works

1. **Upload**: When you click "Upload Image" in the editor
2. **Progress**: Real-time upload percentage shown
3. **Cloudinary**: Image is uploaded to your Cloudinary account
4. **URL**: Cloudinary returns a URL (not base64)
5. **Save**: URL is saved in your JSON data

## Benefits

✅ **No Base64**: Images are stored as URLs (much smaller JSON files)
✅ **Fast Loading**: Images served from Cloudinary CDN
✅ **Automatic Optimization**: Cloudinary optimizes images automatically
✅ **Transformations**: Can resize/crop images on-the-fly
✅ **Progress Tracking**: See upload percentage in real-time

## Free Plan Limits

- **Storage**: 25 GB
- **Bandwidth**: 25 GB/month
- **Transformations**: 25,000/month
- More than enough for a photography portfolio!

## Testing

1. Open `editor.html` in your browser
2. Try uploading an image
3. Check the progress bar
4. Verify the Cloudinary URL is saved
5. Check your Cloudinary dashboard to see the uploaded image

## Troubleshooting

### Upload fails with CORS error
- Make sure your upload preset is set to "Unsigned"
- Check that you're using the correct cloud name

### Upload fails with "Invalid preset"
- Double-check the preset name in your Cloudinary settings
- Make sure the preset exists and is active

### Images not loading
- Check the URL in your JSON file
- Make sure the images are public in Cloudinary
- Check browser console for errors

## Advanced Features

### Get Transformed Images

```javascript
// Get thumbnail (300px wide)
const thumb = cloudinaryUploader.getThumbnailUrl(publicId, 300);

// Get custom size
const custom = cloudinaryUploader.getTransformedUrl(publicId, {
    width: 800,
    height: 600,
    crop: 'fill',
    quality: 'auto',
    format: 'webp'
});
```

### Validate Before Upload

```javascript
const validation = cloudinaryUploader.validateFile(file, 10); // 10MB max
if (!validation.valid) {
    alert(validation.error);
}
```

## Migration from Base64

Your existing base64 images will still work! The system now supports both:
- **Base64 URLs**: Still work (data:image/jpeg;base64,...)
- **Cloudinary URLs**: New uploads (https://res.cloudinary.com/...)

You can gradually replace base64 images by:
1. Opening editor
2. Clicking "Upload Image" for each image
3. Saving the JSON

## Need Help?

- [Cloudinary Documentation](https://cloudinary.com/documentation)
- [Upload Presets Guide](https://cloudinary.com/documentation/upload_presets)
- [Image Transformations](https://cloudinary.com/documentation/image_transformations)
