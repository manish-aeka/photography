// Site theme for the Tailwind-based admin pages (editor, Cloudinary test).
// Load right after the Tailwind CDN script. Remaps the gray and blue palettes to the
// homepage's forest green / brass colours and swaps in its fonts (see assets/css/style.css).
tailwind.config = {
    theme: {
        extend: {
            colors: {
                gray: {
                    50: '#F3F0E7', 100: '#E8E4D8', 200: '#DCE0D6', 300: '#C9D0C4', 400: '#8B9587',
                    500: '#6E7A6F', 600: '#3A473F', 700: '#26382D', 800: '#1B211E', 900: '#151A17', 950: '#111512'
                },
                blue: {
                    50: '#F7F3EA', 100: '#EDE4D1', 200: '#E0D2B5', 300: '#D2BF98', 400: '#C9B48C',
                    500: '#B6A079', 600: '#8C7650', 700: '#6F5D3E', 800: '#54462F', 900: '#3B3222'
                }
            },
            fontFamily: {
                sans: ['Manrope', 'Helvetica Neue', 'Arial', 'sans-serif'],
                serif: ['Cormorant Garamond', 'Georgia', 'serif']
            }
        }
    }
};

(function () {
    var fonts = document.createElement('link');
    fonts.rel = 'stylesheet';
    fonts.href = 'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Manrope:wght@400;500;600;700&display=swap';
    document.head.appendChild(fonts);
    var style = document.createElement('style');
    style.textContent = 'h1,h2{font-family:"Cormorant Garamond",Georgia,serif;font-weight:600;letter-spacing:.01em}input{accent-color:#B6A079}:focus,:focus-visible{outline-color:#B6A079}';
    document.head.appendChild(style);
})();
