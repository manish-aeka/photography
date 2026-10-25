# Anupam Dutta Photography

Wildlife and bird photography portfolio, live at [anupamdutta.in](https://anupamdutta.in) (GitHub Pages, see `CNAME`).

A static site with no backend. Every page reads its content from one JSON file, and photos are hosted on Cloudinary.

## Structure

```
index.html                     Homepage (hero slideshow, featured work, passion, collections, about, contact)
pages/category.html            One collection's gallery: ?category=<index in the JSON>
pages/editor.html              Admin editor for the JSON (linked as "Admin" in the footer)
pages/test-cloudinary.html     Manual Cloudinary upload test
pages/index.html               Redirects to the homepage
data/anupam-dutta-photography-data-set.json   All site content
assets/css/style.css           Design system for the public pages (colours, fonts, layout)
assets/portrait.jpg            Default About portrait, used when about.portrait is empty
scripts/cloudinary-uploader.js Browser uploads to Cloudinary (cloud name + unsigned preset at the bottom)
scripts/tailwind-theme.js      Site colours/fonts for the Tailwind-based admin pages
scripts/fallback-handler.js    Placeholder for broken images in the editor
```

## Run locally

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000` for the site and `http://localhost:8000/pages/editor.html` for the editor. Opening the HTML files directly (`file://`) won't work, because the pages `fetch` the JSON.

## Updating content

1. Open the editor and log in.
2. Edit the sections. They follow the homepage from top to bottom. Uploaded photos go straight to Cloudinary.
3. Click **Save JSON**. This downloads `anupam-dutta-photography-data-set.json`.
4. Replace `data/anupam-dutta-photography-data-set.json` with the downloaded file, then commit and push:

   ```bash
   git add data/anupam-dutta-photography-data-set.json
   git commit -m "Update site content"
   git push
   ```

GitHub Pages publishes the change within a minute or two.

## Design

The colours and fonts are CSS variables at the top of `assets/css/style.css`: forest green `#151A17` / `#26382D`, brass accent `#B6A079`, Cormorant Garamond headings and Manrope body text. The admin pages get the same palette from `scripts/tailwind-theme.js`.

Gallery captions (e.g. "Cerulean, Bali") are a small lookup (`CAPTIONS`) in the script at the bottom of `index.html`, keyed by the photo's file name.

## Editor password

The editor's password check runs in the browser against a SHA-256 hash in `settings.password`. Anyone can read that JSON file, so treat this as a lock on the editor screen, not real security. The editor can only download a file. Publishing still needs push access to this repo.
