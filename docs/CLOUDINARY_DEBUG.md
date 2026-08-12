# Cloudinary Upload Debugging Guide

## Quick Test Steps

### 1. Open Test Page
Open `test-cloudinary.html` in your browser to test the upload functionality.

### 2. Open Editor with Console
1. Open `editor.html` in your browser
2. Press `F12` to open Developer Tools
3. Go to the **Console** tab
4. Try uploading an image (e.g., About Card section)

## What to Look For in Console

### ✅ Expected Success Messages:
```
✅ Cloudinary uploader loaded successfully
📋 Cloud Name: ddyo9iiz9
📋 Upload Preset: anupam-photography
📋 Folder: photography
🚀 Starting Cloudinary upload...
📊 Upload Progress: 10%, 20%, 30%...
✅ Upload successful!
```

### ❌ Common Error Messages:

#### 1. Upload Preset Not Found
```
Error: Invalid upload preset
```
**Fix:** Go to Cloudinary Dashboard → Settings → Upload → Upload Presets
- Verify `anupam-photography` preset exists
- Make sure it's set to **"Unsigned"**
- If not exists, create a new unsigned preset

#### 2. Network/CORS Error
```
Network error during upload
```
**Fix:** 
- Check internet connection
- Cloudinary API may be blocked by firewall
- Try a different network

#### 3. File Size Exceeded
```
File size exceeds 10MB limit
```
**Fix:** Use a smaller image (< 10MB)

#### 4. Invalid Format
```
File format not supported
```
**Fix:** Use JPEG, PNG, WebP, or GIF only

## Cloudinary Setup Checklist

### Required Settings:
1. **Cloud Name:** `ddyo9iiz9` ✅ (Already configured)
2. **Upload Preset:** `anupam-photography` ⚠️ (Needs verification)
3. **Preset Type:** Must be "Unsigned" ⚠️ (Needs verification)
4. **Folder:** `photography` ✅ (Already configured)

### How to Create/Verify Upload Preset:

1. **Go to Cloudinary Dashboard**
   - URL: https://cloudinary.com/console
   - Login with your account

2. **Navigate to Upload Settings**
   - Click **Settings** (gear icon)
   - Go to **Upload** tab
   - Scroll to **Upload presets** section

3. **Check for `anupam-photography` preset**
   - Look in the list of presets
   - Click on it to view details

4. **Verify Settings**
   - **Signing Mode:** Must be **"Unsigned"**
   - **Folder:** Can be empty or set to `photography`
   - **Tags:** Optional

5. **If Preset Doesn't Exist**
   - Click **"Add upload preset"**
   - **Preset name:** `anupam-photography`
   - **Signing mode:** Select **"Unsigned"**
   - **Folder:** (Optional) Enter `photography`
   - Click **Save**

## Testing Process

### Step 1: Verify Configuration
Open browser console and check for:
```javascript
✅ Cloudinary uploader loaded successfully
```

### Step 2: Try Upload
1. Click "Upload Image" button on any section
2. Select a small test image (< 1MB)
3. Watch the console for messages

### Step 3: Check Progress
You should see:
- Progress overlay appear on the image
- Progress bar filling up
- Percentage increasing (0% → 100%)

### Step 4: Verify Success
- Progress overlay turns green with checkmark
- Image appears in the preview
- URL is updated in the input field

## Common Issues & Solutions

| Issue | Console Message | Solution |
|-------|----------------|----------|
| Preset doesn't exist | "Invalid upload preset" | Create unsigned preset in Cloudinary dashboard |
| Wrong cloud name | "Not found" or 404 | Verify cloud name is `ddyo9iiz9` |
| Network blocked | "Network error" | Check internet/firewall |
| File too large | "File size exceeds" | Use smaller image |
| Wrong format | "File format not supported" | Use JPEG/PNG/WebP/GIF |
| CORS issue | "CORS policy" | Cloudinary handles CORS automatically for unsigned uploads |

## Manual Test with Curl (Advanced)

Test your Cloudinary credentials directly:

```bash
curl -X POST https://api.cloudinary.com/v1_1/ddyo9iiz9/image/upload \
  -F "file=@path/to/your/image.jpg" \
  -F "upload_preset=anupam-photography"
```

**Expected Response:** JSON with `secure_url`, `public_id`, etc.

**Error Response:** JSON with `error` object containing the issue

## Still Not Working?

1. **Check browser console** for exact error message
2. **Try test-cloudinary.html** first (simpler to debug)
3. **Verify upload preset exists** in Cloudinary dashboard
4. **Try a different image** (small JPEG < 1MB)
5. **Check network tab** (F12 → Network) for failed requests
6. **Copy exact error message** and share for further help

## Contact Support

If still having issues, provide:
- ❌ Exact error message from console
- 🖼️ Screenshot of Cloudinary upload preset settings
- 🌐 Network tab showing the failed request
- 📱 Browser version and OS
