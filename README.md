# 📸 Anupam Dutta Photography Portfolio

> A modern, dynamic photography portfolio showcasing wildlife and nature photography with an integrated content management system.

[![Live Site](https://img.shields.io/badge/Live-anupamdutta.in-1C5BAE?style=for-the-badge)](https://anupamdutta.in)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

## 🌟 Overview

A fully responsive, JSON-driven photography portfolio with built-in content editor and automated deployment tools. Features wildlife photography categorized by themes, with Cloudinary-powered image hosting and a sleek, modern UI built with Tailwind CSS.

### ✨ Key Features

- 🎨 **Modern Responsive Design** - Beautiful UI optimized for all devices
- 📝 **Visual Content Editor** - Manage your portfolio without touching code
- ☁️ **Cloudinary Integration** - Professional image hosting with automatic optimization
- 🚀 **One-Click Deployment** - Automated Git deployment via bash script or GUI app
- 🎯 **JSON-Based Content** - Easy data management with structured JSON
- 🖼️ **Dynamic Galleries** - Categorized photo collections with lightbox viewing
- 🌙 **Multiple Categories** - Showcase different photography themes
- ⚡ **Fast Loading** - Optimized images and lazy loading
- 📱 **Mobile-First** - Responsive design that works on any screen size

## 🚀 Quick Start

### Prerequisites

- **Web Browser** - Modern browser (Chrome, Firefox, Safari, Edge)
- **Git** - For deployment ([Download](https://git-scm.com/))
- **Code Editor** - VS Code, Sublime Text, or any editor (for customization)
- **Cloudinary Account** - Free account for image hosting ([Sign up](https://cloudinary.com/))

### Basic Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/photography.git
   cd photography
   ```

2. **Configure Cloudinary**
   - Follow the [Cloudinary Setup Guide](docs/CLOUDINARY_SETUP.md)
   - Update your cloud name and upload preset in `scripts/cloudinary-uploader.js`

3. **Open locally**
   ```bash
   # Simple HTTP server (Python 3)
   python -m http.server 8000
   
   # Or use VS Code Live Server extension
   # Right-click index.html → Open with Live Server
   ```

4. **Access the site**
   - Portfolio: `http://localhost:8000`
   - Editor: `http://localhost:8000/pages/editor.html`

### Using the Editor

1. Open `pages/editor.html` in your browser
2. Edit content, upload images, manage categories
3. Click **Download JSON** to save your data
4. Replace `data/anupam-dutta-photography-data-set.json` with the downloaded file
5. Deploy using one of the methods below

## 📦 Project Structure

```
photography/
├── index.html                    # Main portfolio page
├── CNAME                         # Custom domain configuration
├── assets/
│   └── css/
│       └── style.css            # Custom styles and animations
├── data/
│   └── anupam-dutta-photography-data-set.json  # Portfolio content
├── deployment/                   # Deployment tools
│   ├── deploy.sh                # Bash script for Git deployment
│   ├── deploy-app.py            # Python GUI deployment app
│   ├── setup.sh                 # Setup Python environment
│   ├── run-deploy.sh            # Launch deployment app
│   ├── build.sh                 # Build standalone executable
│   ├── build-mac.sh             # Build macOS app bundle
│   ├── requirements.txt         # Python dependencies
│   ├── README.md                # Deployment app documentation
│   └── README-deploy-sh.md      # Deploy.sh documentation
├── docs/                        # Documentation
│   ├── CLOUDINARY_SETUP.md      # Cloudinary configuration guide
│   ├── IMPLEMENTATION_SUMMARY.md # Technical implementation details
│   ├── DEPLOY-APP-README.md     # Deployment app guide
│   └── QUICK_REFERENCE.txt      # Quick reference guide
├── images/                      # Local images (if any)
├── pages/
│   ├── editor.html              # Visual content editor
│   ├── category.html            # Category page template
│   └── test-cloudinary.html     # Cloudinary upload tester
└── scripts/
    ├── script.js                # Main application logic
    ├── cloudinary-uploader.js   # Cloudinary upload handler
    └── fallback-handler.js      # Image fallback handling
```

## 🎨 Features in Detail

### 📝 Content Editor

A fully-featured visual editor for managing your portfolio:

- **About Section** - Edit bio, description, and profile image
- **Slider Management** - Add/remove/reorder hero slider images
- **Category Management** - Create and organize photo categories
- **Image Upload** - Direct upload to Cloudinary with progress tracking
- **Gallery Builder** - Manage individual photo collections
- **Real-time Preview** - See changes as you make them
- **JSON Export** - Download your complete data structure

**Access:** Open `pages/editor.html` in your browser

### ☁️ Cloudinary Integration

Professional image hosting with automatic optimization:

- ✅ Direct browser uploads (no server needed)
- ✅ Automatic image optimization and compression
- ✅ Responsive image delivery
- ✅ Thumbnail generation
- ✅ Progress tracking during uploads
- ✅ 10MB max file size validation
- ✅ Support for JPEG, PNG, WebP, GIF

**Setup Guide:** [docs/CLOUDINARY_SETUP.md](docs/CLOUDINARY_SETUP.md)

### 🚀 Deployment Options

Two deployment methods to push your changes:

#### Option 1: Bash Script (Quick & Simple)

```bash
cd deployment
chmod +x deploy.sh
./deploy.sh "Updated portfolio with new photos"
```

**Features:**
- Auto-detects changes in data files
- Custom or auto-generated commit messages
- Color-coded terminal output
- Validates before deploying

**Documentation:** [deployment/README-deploy-sh.md](deployment/README-deploy-sh.md)

#### Option 2: Python GUI App (User-Friendly)

```bash
cd deployment
./setup.sh      # One-time setup
./run-deploy.sh # Launch GUI
```

**Features:**
- Beautiful graphical interface
- Visual file selection
- Progress bars and status updates
- Error handling and validation
- Cross-platform (Windows, macOS, Linux)

**Documentation:** [deployment/README.md](deployment/README.md)

## 🎯 Usage Guide

### Managing Content

1. **Edit Portfolio Data**
   - Open `pages/editor.html`
   - Make your changes
   - Click "Download JSON"
   - Save as `data/anupam-dutta-photography-data-set.json`

2. **Upload Images**
   - Use the editor's image upload feature
   - Images automatically upload to Cloudinary
   - URLs are inserted into your JSON data
   - No manual file management needed

3. **Add New Category**
   - In editor, scroll to "Categories" section
   - Click "Add Category"
   - Fill in title, description, cover image
   - Add photos to the category
   - Download and save JSON

4. **Deploy Changes**
   ```bash
   # Quick deploy with bash
   cd deployment
   ./deploy.sh "Added new wildlife category"
   
   # Or use GUI
   ./run-deploy.sh
   ```

### Customizing Design

1. **Colors and Theme**
   - Edit CSS variables in `assets/css/style.css`
   - Primary color: `#1C5BAE`
   - Secondary color: `#1DA6E1`

2. **Layout Changes**
   - Modify `index.html` for structure
   - Uses Tailwind CSS utility classes
   - Responsive breakpoints: `sm:`, `md:`, `lg:`, `xl:`

3. **JavaScript Behavior**
   - Main logic in `scripts/script.js`
   - Cloudinary uploads in `scripts/cloudinary-uploader.js`
   - Fallback handling in `scripts/fallback-handler.js`

## 🛠️ Configuration

### Cloudinary Setup

Edit `scripts/cloudinary-uploader.js`:

```javascript
const cloudinaryUploader = new CloudinaryUploader({
    cloudName: 'YOUR_CLOUD_NAME',      // Your Cloudinary cloud name
    uploadPreset: 'YOUR_PRESET_NAME',  // Unsigned upload preset
    folder: 'photography-portfolio'     // Upload folder name
});
```

**Full Setup Guide:** [docs/CLOUDINARY_SETUP.md](docs/CLOUDINARY_SETUP.md)

### Custom Domain

The site uses `anupamdutta.in`. To change:

1. Edit `CNAME` file with your domain
2. Configure DNS with your provider
3. Point to GitHub Pages (if using GitHub Pages)

### Deployment Configuration

Edit `deployment/deploy.sh` to configure:

```bash
# Target branch (empty = current branch)
TARGET_BRANCH=""

# Files to include in deployment
INCLUDE_FILES=(
    "data/*.json"
)
```

## 📱 Browser Support

- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🐛 Troubleshooting

### Images Not Loading

1. Check Cloudinary configuration in `cloudinary-uploader.js`
2. Verify upload preset is set to "unsigned"
3. Check browser console for errors
4. Test upload at `pages/test-cloudinary.html`

### Editor Not Saving

1. Make sure you clicked "Download JSON"
2. Replace the file in `data/` folder
3. Verify JSON is valid (use [JSONLint](https://jsonlint.com/))
4. Clear browser cache and refresh

### Deployment Fails

```bash
# Check Git status
git status

# Verify remote is configured
git remote -v

# Test authentication
git fetch origin

# See detailed errors
./deploy.sh 2>&1 | tee deploy.log
```

### Python Deployment App Issues

```bash
# Reinstall dependencies
cd deployment
rm -rf .venv
./setup.sh

# Check Python version
python --version  # Should be 3.8+
```

## 📚 Documentation

- **[Cloudinary Setup Guide](docs/CLOUDINARY_SETUP.md)** - Configure image hosting
- **[Deploy.sh Documentation](deployment/README-deploy-sh.md)** - Bash deployment guide
- **[Deployment App Guide](deployment/README.md)** - Python GUI deployment
- **[Implementation Summary](docs/IMPLEMENTATION_SUMMARY.md)** - Technical details
- **[Quick Reference](docs/QUICK_REFERENCE.txt)** - Command quick reference

## 🚀 Deployment

### GitHub Pages

1. Push to GitHub
2. Go to Settings → Pages
3. Select branch (usually `main`)
4. Save and wait for deployment

### Custom Hosting

Upload these files to your web server:
- `index.html`
- `CNAME` (if using custom domain)
- `assets/`
- `data/`
- `images/`
- `pages/`
- `scripts/`

### Automated Deployment

Set up GitHub Actions or use the included deployment tools for continuous deployment.

## 🔒 Security Notes

- ⚠️ Editor is client-side only (no authentication)
- ⚠️ Keep `deployment/` folder out of production
- ⚠️ Use environment variables for sensitive data
- ✅ Cloudinary unsigned uploads are safe for client-side use
- ✅ No server-side code = no backend vulnerabilities

## 🎓 Learning Resources

- **Tailwind CSS**: [tailwindcss.com](https://tailwindcss.com)
- **Cloudinary Docs**: [cloudinary.com/documentation](https://cloudinary.com/documentation)
- **JSON Structure**: See `data/anupam-dutta-photography-data-set.json`
- **Git Basics**: [git-scm.com/doc](https://git-scm.com/doc)

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Anupam Dutta**
- Website: [anupamdutta.in](https://anupamdutta.in)
- Portfolio: Wildlife & Nature Photography

## 🙏 Acknowledgments

- **Tailwind CSS** - Utility-first CSS framework
- **Cloudinary** - Image hosting and optimization
- **GitHub Pages** - Free hosting platform

## 📞 Support

If you encounter any issues:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review documentation in `docs/` folder
3. Search existing [GitHub Issues](https://github.com/yourusername/photography/issues)
4. Open a new issue with detailed description

---

**Built with ❤️ for photographers who love their craft**

*Star ⭐ this repo if you found it useful!*
