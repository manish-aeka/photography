// --- ALL DOMContentLoaded LOGIC COMBINED ---
document.addEventListener('DOMContentLoaded', function () {
    // Hide loading overlay
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        setTimeout(() => {
            loadingOverlay.style.opacity = '0';
            loadingOverlay.style.transition = 'opacity 0.5s ease-out';
            setTimeout(() => {
                loadingOverlay.style.display = 'none';
            }, 500);
        }, 500);
    }

    // Navbar scroll background toggle
    const navbar = document.querySelector('nav');
    function handleNavbarBg() {
        if (window.scrollY > 10) {
            navbar.classList.add('bg-gray-900');
        } else {
            navbar.classList.remove('bg-gray-900');
        }
    }
    window.addEventListener('scroll', handleNavbarBg);
    // Run once on load
    handleNavbarBg();
    // Contact Form Mailto Feature
    const form = document.getElementById('contact-form');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const inputs = form.querySelectorAll('input[type="text"]');
            let name = '', subject = '';
            if (inputs.length === 1) {
                name = inputs[0].value;
            } else if (inputs.length > 1) {
                name = inputs[0].value;
                subject = inputs[1].value;
            }
            const email = form.querySelector('input[type="email"]').value;
            if (!subject) {
                // fallback: try to get subject by label
                const subjectInput = Array.from(form.querySelectorAll('input')).find(input => input.previousElementSibling && input.previousElementSibling.textContent.trim().toLowerCase() === 'subject');
                if (subjectInput) subject = subjectInput.value;
            }
            const message = form.querySelector('textarea').value;
            const mailto = `mailto:anupam.d1@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent('Name: ' + name + '\nEmail: ' + email + '\n\n' + message)}`;
            window.location.href = mailto;
        });
    }

    // --- CATEGORY CARD RENDER & CLICK REDIRECT ---
    fetch("anupam-dutta-photography-data-set.json")
        .then(res => res.json())
        .then(data => {
            // Populate Hero Content from slider-content
            if (data['slider-content']) {
                const heroHeading = document.getElementById('heroHeading');
                const heroDescription = document.getElementById('heroDescription');
                const heroButton = document.getElementById('heroButton');

                if (heroHeading && data['slider-content'].heading) {
                    heroHeading.textContent = data['slider-content'].heading;
                }
                if (heroDescription && data['slider-content'].description) {
                    heroDescription.textContent = data['slider-content'].description;
                }
                if (heroButton && data['slider-content']['show-latest-collections-button'] === false) {
                    heroButton.style.display = 'none';
                } else if (heroButton) {
                    heroButton.innerHTML = `<span class="relative z-10 flex items-center gap-2">
                        Explore Latest Collections
                        <svg class="w-5 h-5 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path>
                        </svg>
                    </span>`;

                    // Scroll to Featured Work (gallery) section
                    heroButton.onclick = function () {
                        const featuredWorkSection = document.getElementById('featured-work');
                        if (featuredWorkSection) {
                            featuredWorkSection.scrollIntoView({ behavior: 'smooth' });
                        }
                    };
                }
            }

            // Set logo URL if available
            if (data['logo-url']) {
                document.querySelectorAll('.logo-img').forEach(logoImg => {
                    logoImg.src = data['logo-url'];
                });
                // Also update favicon
                const favicon = document.querySelector('link[rel="icon"]');
                const appleTouchIcon = document.querySelector('link[rel="apple-touch-icon"]');
                if (favicon) favicon.href = data['logo-url'];
                if (appleTouchIcon) appleTouchIcon.href = data['logo-url'];
            }

            // Populate About section
            if (data.about) {
                const aboutTitle = document.getElementById('about-title');
                const aboutDesc = document.getElementById('about-description');

                if (aboutTitle && data.about.title) {
                    aboutTitle.textContent = data.about.title;
                }
                if (aboutDesc && data.about.description) {
                    aboutDesc.textContent = data.about.description;
                }

                // Populate About Card/Content Box
                if (data.about.card) {
                    const cardContainer = document.getElementById('about-card');
                    const cardImage = document.getElementById('about-card-image');
                    const cardTitle = document.getElementById('about-card-title');
                    const cardDesc = document.getElementById('about-card-description');
                    const cardSubDesc = document.getElementById('about-card-subdescription');

                    // Show/hide card based on visibility flag
                    if (cardContainer && data.about.card['is-card-visible'] !== undefined) {
                        if (data.about.card['is-card-visible']) {
                            cardContainer.style.display = 'flex';
                        } else {
                            cardContainer.style.display = 'none';
                        }
                    }

                    if (cardImage && data.about.card.url) {
                        cardImage.src = data.about.card.url;
                    }
                    if (cardTitle && data.about.card.title) {
                        cardTitle.textContent = data.about.card.title;
                    }
                    if (cardDesc && data.about.card.description) {
                        cardDesc.textContent = data.about.card.description;
                    }
                    if (cardSubDesc && data.about.card['sub-description']) {
                        cardSubDesc.textContent = data.about.card['sub-description'];
                    }
                }
            }

            // Render categories
            if (data.categories && Array.isArray(data.categories)) {
                const container = document.getElementById('categories-container');
                container.innerHTML = '';
                data.categories.forEach(category => {
                    const card = document.createElement('div');
                    card.className = "group relative w-full max-w-md bg-gradient-to-br from-white/5 via-white/10 to-white/5 backdrop-blur-xl border border-white/20 rounded-3xl shadow-2xl overflow-hidden transition-all duration-500 hover:shadow-indigo-500/20 hover:border-indigo-500/30 cursor-pointer";
                    card.setAttribute('data-category-url', category.url);

                    // Truncate description to 200 chars
                    const fullDesc = category.description;
                    const shortDesc = fullDesc.length > 200 ? fullDesc.slice(0, 200) + '...' : fullDesc;

                    card.innerHTML = `
                        <!-- Animated Background Gradient -->
                        <div class="absolute inset-0 bg-gradient-to-br from-indigo-600/5 via-purple-600/5 to-pink-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                        
                        <!-- Image Section with Overlay -->
                        <div class="relative overflow-hidden">
                            <div class="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                            <img class="relative w-full h-72 object-cover transform group-hover:scale-105 transition-transform duration-700" src="${category.image}" alt="${category.title}">
                            <div class="absolute bottom-0 left-0 right-0 z-20 opacity-0 group-hover:opacity-100 transition-opacity duration-500 p-4">
                                <div class="w-full h-1 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full"></div>
                            </div>
                        </div>
                        
                        <!-- Content Section -->
                        <div class="relative p-8 z-10">
                            <h3 class="text-2xl md:text-3xl font-bold text-white tracking-wide leading-tight mb-3">${category.title}</h3>
                            <div class="w-16 h-1 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full mb-4"></div>
                            <p class="text-gray-200 leading-relaxed card-desc">${shortDesc}</p>
                            ${fullDesc.length > 200 ? `
                                <button class="mt-6 px-6 py-2.5 bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-xl font-semibold hover:from-indigo-600 hover:to-purple-600 transition-all shadow-lg read-more-btn">Read More</button>
                                <button class="mt-6 px-6 py-2.5 bg-gradient-to-r from-gray-600 to-gray-700 text-white rounded-xl font-semibold hover:from-gray-700 hover:to-gray-800 transition-all shadow-lg show-less-btn" style="display:none">Show Less</button>
                            ` : ''}
                        </div>
                    `;
                    // Card click (except button)
                    card.addEventListener('click', function (e) {
                        if (e.target.classList.contains('read-more-btn') || e.target.classList.contains('show-less-btn')) return;
                        if (category.url) {
                            window.location.href = category.url;
                        }
                    });
                    // Read More / Show Less button logic
                    const btnRead = card.querySelector('.read-more-btn');
                    const btnLess = card.querySelector('.show-less-btn');
                    if (btnRead && btnLess) {
                        btnRead.addEventListener('click', function (e) {
                            e.stopPropagation();
                            card.querySelector('.card-desc').textContent = fullDesc;
                            btnRead.style.display = 'none';
                            btnLess.style.display = 'inline-block';
                        });
                        btnLess.addEventListener('click', function (e) {
                            e.stopPropagation();
                            card.querySelector('.card-desc').textContent = shortDesc;
                            btnRead.style.display = 'inline-block';
                            btnLess.style.display = 'none';
                        });
                    }
                    container.appendChild(card);
                });
            }
        });
    // (Keep old click handler for static cards if any remain)
    document.querySelectorAll('.category-card').forEach(card => {
        card.addEventListener('click', function () {
            const url = card.getAttribute('data-category-url');
            if (url) {
                window.location.href = url;
            }
        });
    });

    // --- GALLERY MASONRY/COLLAGE RENDER ---
    fetch("anupam-dutta-photography-data-set.json")
        .then(res => res.json())
        .then(data => {
            const gallery = document.getElementById('gallery');
            if (!gallery || !data['gallery-images']) return;
            gallery.innerHTML = '';
            data['gallery-images'].forEach((img, i) => {
                // Vary the row/col span for collage effect
                let extra = '';
                if (i % 6 === 0) extra = 'row-span-2 col-span-2';
                else if (i % 5 === 0) extra = 'row-span-2';
                else if (i % 4 === 0) extra = 'col-span-2';
                gallery.innerHTML += `
                        <div class="overflow-hidden rounded-lg ${extra} cursor-pointer gallery-img-wrapper">
                            <img src="${img}" class="w-full h-full object-cover gallery-img" data-img="${img}" />
                        </div>
                    `;
            });
            // Add click event for popup
            document.querySelectorAll('.gallery-img').forEach(imgEl => {
                imgEl.addEventListener('click', function (e) {
                    e.stopPropagation();
                    const modal = document.getElementById('image-modal');
                    const modalImg = document.getElementById('modal-img');
                    modalImg.src = imgEl.getAttribute('data-img');
                    modal.classList.remove('hidden');
                });
            });
            // Close modal logic
            const closeBtn = document.getElementById('close-modal');
            const modal = document.getElementById('image-modal');
            closeBtn.addEventListener('click', function () {
                modal.classList.add('hidden');
                document.getElementById('modal-img').src = '';
            });
            // Also close modal on background click
            modal.addEventListener('click', function (e) {
                if (e.target === modal) {
                    modal.classList.add('hidden');
                    document.getElementById('modal-img').src = '';
                }
            });
        });
});
// --- GALLERY MASONRY/COLLAGE RENDER ---
fetch("anupam-dutta-photography-data-set.json")
    .then(res => res.json())
    .then(data => {
        const gallery = document.getElementById('gallery');
        if (!gallery || !data['gallery-images']) return;
        gallery.innerHTML = '';
        data['gallery-images'].forEach((img, i) => {
            // Vary the row/col span for collage effect
            let extra = '';
            if (i % 6 === 0) extra = 'row-span-2 col-span-2';
            else if (i % 5 === 0) extra = 'row-span-2';
            else if (i % 4 === 0) extra = 'col-span-2';
            gallery.innerHTML += `
                    <div class="overflow-hidden rounded-lg ${extra} cursor-pointer gallery-img-wrapper">
                        <img src="${img}" class="w-full h-full object-cover gallery-img" data-img="${img}" />
                    </div>
                `;
        });
        // Add click event for popup
        document.querySelectorAll('.gallery-img').forEach(imgEl => {
            imgEl.addEventListener('click', function (e) {
                e.stopPropagation();
                const modal = document.getElementById('image-modal');
                const modalImg = document.getElementById('modal-img');
                modalImg.src = imgEl.getAttribute('data-img');
                modal.classList.remove('hidden');
            });
        });
        // Close modal logic
        const closeBtn = document.getElementById('close-modal');
        const modal = document.getElementById('image-modal');
        closeBtn.addEventListener('click', function () {
            modal.classList.add('hidden');
            document.getElementById('modal-img').src = '';
        });
        // Also close modal on background click
        modal.addEventListener('click', function (e) {
            if (e.target === modal) {
                modal.classList.add('hidden');
                document.getElementById('modal-img').src = '';
            }
        });
    });
// --- CATEGORY CARD RENDER & CLICK REDIRECT ---
document.addEventListener('DOMContentLoaded', function () {
    fetch("anupam-dutta-photography-data-set.json")
        .then(res => res.json())
        .then(data => {
            // Render categories
            if (data.categories && Array.isArray(data.categories)) {
                const container = document.getElementById('categories-container');
                container.innerHTML = '';
                data.categories.forEach(category => {
                    const card = document.createElement('div');
                    card.className = "group relative w-full max-w-md bg-gradient-to-br from-white/5 via-white/10 to-white/5 backdrop-blur-xl border border-white/20 rounded-3xl shadow-2xl overflow-hidden transition-all duration-500 hover:shadow-indigo-500/20 hover:border-indigo-500/30 cursor-pointer";
                    card.setAttribute('data-category-url', category.url);

                    // Truncate description to 200 chars
                    const fullDesc = category.description;
                    const shortDesc = fullDesc.length > 200 ? fullDesc.slice(0, 200) + '...' : fullDesc;

                    card.innerHTML = `
                        <!-- Animated Background Gradient -->
                        <div class="absolute inset-0 bg-gradient-to-br from-indigo-600/5 via-purple-600/5 to-pink-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                        
                        <!-- Image Section with Overlay -->
                        <div class="relative overflow-hidden">
                            <div class="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                            <img class="relative w-full h-72 object-cover transform group-hover:scale-105 transition-transform duration-700" src="${category.image}" alt="${category.title}">
                            <div class="absolute bottom-0 left-0 right-0 z-20 opacity-0 group-hover:opacity-100 transition-opacity duration-500 p-4">
                                <div class="w-full h-1 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full"></div>
                            </div>
                        </div>
                        
                        <!-- Content Section -->
                        <div class="relative p-8 z-10">
                            <h3 class="text-2xl md:text-3xl font-bold text-white tracking-wide leading-tight mb-3">${category.title}</h3>
                            <div class="w-16 h-1 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full mb-4"></div>
                            <p class="text-gray-200 leading-relaxed card-desc">${shortDesc}</p>
                            ${fullDesc.length > 200 ? `
                                <button class="mt-6 px-6 py-2.5 bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-xl font-semibold hover:from-indigo-600 hover:to-purple-600 transition-all shadow-lg read-more-btn">Read More</button>
                                <button class="mt-6 px-6 py-2.5 bg-gradient-to-r from-gray-600 to-gray-700 text-white rounded-xl font-semibold hover:from-gray-700 hover:to-gray-800 transition-all shadow-lg show-less-btn" style="display:none">Show Less</button>
                            ` : ''}
                        </div>
                    `;
                    // Card click (except button)
                    card.addEventListener('click', function (e) {
                        if (e.target.classList.contains('read-more-btn') || e.target.classList.contains('show-less-btn')) return;
                        if (category.url) {
                            window.location.href = category.url;
                        }
                    });
                    // Read More / Show Less button logic
                    const btnRead = card.querySelector('.read-more-btn');
                    const btnLess = card.querySelector('.show-less-btn');
                    if (btnRead && btnLess) {
                        btnRead.addEventListener('click', function (e) {
                            e.stopPropagation();
                            card.querySelector('.card-desc').textContent = fullDesc;
                            btnRead.style.display = 'none';
                            btnLess.style.display = 'inline-block';
                        });
                        btnLess.addEventListener('click', function (e) {
                            e.stopPropagation();
                            card.querySelector('.card-desc').textContent = shortDesc;
                            btnRead.style.display = 'inline-block';
                            btnLess.style.display = 'none';
                        });
                    }
                    container.appendChild(card);
                });
            }
        });
    // (Keep old click handler for static cards if any remain)
    document.querySelectorAll('.category-card').forEach(card => {
        card.addEventListener('click', function () {
            const url = card.getAttribute('data-category-url');
            if (url) {
                window.location.href = url;
            }
        });
    });
});
let slider_images = [];
let current_slider_image = 0;

// Load JSON images
fetch("anupam-dutta-photography-data-set.json")
    .then(res => res.json())
    .then(data => {
        slider_images = data["slider-images"];
        loadImage();
        createDots();
    });

// Load image into slider
function loadImage() {
    const img = document.getElementById("slider-image");
    img.classList.remove("fade");

    setTimeout(() => {
        img.src = slider_images[current_slider_image];
        img.classList.add("fade");
    }, 100);

    updateDots();
}

// Auto slide every 4 seconds
setInterval(() => {
    current_slider_image = (current_slider_image + 1) % slider_images.length;
    loadImage();
}, 4000);

// --- DOTS ---
function createDots() {
    const dotContainer = document.getElementById("dots");
    slider_images.forEach((_, i) => {
        const dot = document.createElement("div");
        dot.className = "w-3 h-3 bg-white/60 rounded-full cursor-pointer";
        dot.addEventListener("click", () => {
            current_slider_image = i;
            loadImage();
        });
        dotContainer.appendChild(dot);
    });
}

function updateDots() {
    const dotContainer = document.getElementById("dots").children;
    for (let i = 0; i < dotContainer.length; i++) {
        dotContainer[i].className =
            "w-3 h-3 rounded-full cursor-pointer " +
            (i === current_slider_image ? "bg-white" : "bg-white/50");
    }
}
