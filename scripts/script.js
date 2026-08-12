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
            const recipientEmail = form.dataset.email || 'anupam.d1@gmail.com';
            const mailto = `mailto:${recipientEmail}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent('Name: ' + name + '\nEmail: ' + email + '\n\n' + message)}`;
            window.location.href = mailto;
        });
    }

    // --- CATEGORY CARD RENDER & CLICK REDIRECT ---
    fetch("./data/anupam-dutta-photography-data-set.json")
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

            // Apply settings data dynamically
            if (data.settings) {
                const settings = data.settings;

                // Set logo URL
                if (settings['logo-url']) {
                    // Update all logo images including navbar and loading overlay
                    document.querySelectorAll('.logo-img, #loading-overlay img').forEach(logoImg => {
                        logoImg.src = settings['logo-url'];
                    });
                    // Also update favicon
                    const favicon = document.querySelector('link[rel="icon"]');
                    const appleTouchIcon = document.querySelector('link[rel="apple-touch-icon"]');
                    if (favicon) favicon.href = settings['logo-url'];
                    if (appleTouchIcon) appleTouchIcon.href = settings['logo-url'];
                }

                // Set navbar title
                if (settings['navbar-title']) {
                    const navbarTitles = document.querySelectorAll('nav h1, .navbar-title');
                    navbarTitles.forEach(title => {
                        if (title.tagName === 'H1') {
                            title.textContent = settings['navbar-title'];
                        }
                    });
                }

                // Set email links
                if (settings.email) {
                    document.querySelectorAll('a[href^="mailto:"]').forEach(emailLink => {
                        emailLink.href = `mailto:${settings.email}`;
                        if (emailLink.textContent.includes('@')) {
                            emailLink.textContent = settings.email;
                        }
                    });
                    // Update form mailto
                    const form = document.getElementById('contact-form');
                    if (form) {
                        form.dataset.email = settings.email;
                    }
                }

                // Set phone number
                if (settings.phone) {
                    document.querySelectorAll('a[href^="tel:"]').forEach(phoneLink => {
                        phoneLink.href = `tel:${settings.phone}`;
                        phoneLink.textContent = settings.phone;
                    });
                }

                // Set address/location
                if (settings.address) {
                    const locationElements = document.querySelectorAll('.location-text, [data-location]');
                    locationElements.forEach(element => {
                        element.textContent = settings.address;
                    });
                    // Also find the location in the contact section
                    const contactDivs = document.querySelectorAll('.text-lg.font-semibold.text-white');
                    contactDivs.forEach(div => {
                        if (div.textContent.includes('Kolkata')) {
                            div.textContent = settings.address;
                        }
                    });
                }

                // Set page title and footer brand name
                if (settings['navbar-title']) {
                    document.title = settings['navbar-title'];
                    const footerTitles = document.querySelectorAll('footer h3');
                    footerTitles.forEach(title => {
                        if (title.textContent.includes('Anupam Dutta')) {
                            title.textContent = settings['navbar-title'];
                        }
                    });
                }

                // Set Instagram links
                if (settings['instagram-url']) {
                    document.querySelectorAll('a[href*="instagram.com"], .instagram-link').forEach(igLink => {
                        igLink.href = settings['instagram-url'];
                    });
                }

                // Set Instagram username display
                if (settings['instagram-username']) {
                    document.querySelectorAll('.instagram-username').forEach(igUsername => {
                        igUsername.textContent = settings['instagram-username'];
                    });
                }
            }

            // Apply slider content data dynamically
            if (data['slider-content']) {
                const sliderContent = data['slider-content'];

                // Set slider heading
                if (sliderContent.heading) {
                    const heroHeading = document.getElementById('heroHeading');
                    if (heroHeading) {
                        heroHeading.textContent = sliderContent.heading;
                        // Show/hide based on flag
                        if (sliderContent['show-heading'] === false) {
                            heroHeading.style.display = 'none';
                        } else {
                            heroHeading.style.display = 'block';
                        }
                    }
                }

                // Set slider description
                if (sliderContent.description) {
                    const heroDescription = document.getElementById('heroDescription');
                    if (heroDescription) {
                        heroDescription.textContent = sliderContent.description;
                        // Show/hide based on flag
                        if (sliderContent['show-description'] === false) {
                            heroDescription.style.display = 'none';
                        } else {
                            heroDescription.style.display = 'block';
                        }
                    }
                }

                // Show/hide latest collections button
                if (sliderContent['show-latest-collections-button'] !== undefined) {
                    const heroButton = document.getElementById('heroButton');
                    if (heroButton) {
                        if (sliderContent['show-latest-collections-button'] === false) {
                            heroButton.style.display = 'none';
                        } else {
                            heroButton.style.display = 'inline-block';
                        }
                    }
                }
            }

            // Apply slider images dynamically
            if (data['slider-images'] && data['slider-images'].length > 0) {
                const sliderImage = document.getElementById('slider-image');
                if (sliderImage) {
                    // Set the first image as the current image
                    sliderImage.src = data['slider-images'][0];

                    // Store all images in a data attribute or global variable for slider functionality
                    window.sliderImagesData = data['slider-images'];

                    // If you have existing slider next/prev functions, they can now use window.sliderImagesData
                }
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
                data.categories.forEach((category, index) => {
                    const card = document.createElement('div');
                    card.className = "group relative w-full max-w-md bg-gradient-to-br from-white/5 via-white/10 to-white/5 backdrop-blur-xl border border-white/20 rounded-3xl shadow-2xl overflow-hidden transition-all duration-500 hover:shadow-[#1C5BAE]/20 hover:border-[#1C5BAE]/30 cursor-pointer";
                    card.setAttribute('data-category-index', index);

                    // Truncate description to 200 chars
                    const fullDesc = category.description;
                    const shortDesc = fullDesc.length > 200 ? fullDesc.slice(0, 200) + '...' : fullDesc;

                    card.innerHTML = `
                        <!-- Animated Background Gradient -->
                        <div class="absolute inset-0 bg-gradient-to-br from-[#1C5BAE]/5 via-[#1DA6E1]/5 to-[#1C5BAE]/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                        
                        <!-- Image Section with Overlay -->
                        <div class="relative overflow-hidden">
                            <div class="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                            <img class="relative w-full h-72 object-cover transform group-hover:scale-105 transition-transform duration-700" src="${category.image}" alt="${category.title}">
                            <div class="absolute bottom-0 left-0 right-0 z-20 opacity-0 group-hover:opacity-100 transition-opacity duration-500 p-4">
                                <div class="w-full h-1 bg-gradient-to-r from-[#1C5BAE] to-[#1DA6E1] rounded-full"></div>
                            </div>
                        </div>
                        
                        <!-- Content Section -->
                        <div class="relative p-8 z-10">
                            <h3 class="text-2xl md:text-3xl font-bold text-white tracking-wide leading-tight mb-3">${category.title}</h3>
                            <div class="w-16 h-1 bg-gradient-to-r from-[#1C5BAE] to-[#1DA6E1] rounded-full mb-4"></div>
                            <p class="text-gray-200 leading-relaxed card-desc">${shortDesc}</p>
                            ${fullDesc.length > 200 ? `
                                <button class="mt-6 px-6 py-2.5 bg-gradient-to-r from-[#1C5BAE] to-[#1DA6E1] text-white rounded-xl font-semibold hover:from-[#1DA6E1] hover:to-[#1C5BAE] transition-all shadow-lg read-more-btn">Read More</button>
                                <button class="mt-6 px-6 py-2.5 bg-gradient-to-r from-gray-600 to-gray-700 text-white rounded-xl font-semibold hover:from-gray-700 hover:to-gray-800 transition-all shadow-lg show-less-btn" style="display:none">Show Less</button>
                            ` : ''}
                        </div>
                    `;
                    // Card click (except button)
                    card.addEventListener('click', function (e) {
                        if (e.target.classList.contains('read-more-btn') || e.target.classList.contains('show-less-btn')) return;
                        const categoryIndex = card.getAttribute('data-category-index');
                        if (categoryIndex !== null) {
                            window.location.href = `./pages/category.html?category=${categoryIndex}`;
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

    // --- GALLERY MASONRY RENDER ---
    fetch("./data/anupam-dutta-photography-data-set.json")
        .then(res => res.json())
        .then(data => {
            const gallery = document.getElementById('gallery');
            if (!gallery || !data['gallery-images']) return;
            gallery.innerHTML = '';

            data['gallery-images'].forEach((img, i) => {
                const wrapper = document.createElement('div');
                const pad = String(i + 1).padStart(2, '0');

                wrapper.className = 'group relative overflow-hidden rounded-xl cursor-pointer mb-3 break-inside-avoid transition-all duration-300 hover:shadow-2xl hover:shadow-black/60';
                wrapper.style.animationDelay = `${i * 60}ms`;

                wrapper.innerHTML = `
                    <img src="${img}"
                         class="w-full h-auto object-cover transition-transform duration-700 group-hover:scale-[1.04]"
                         data-img="${img}"
                         alt="Gallery Image ${i + 1}"
                         loading="lazy" />

                    <!-- Hover overlay -->
                    <div class="absolute inset-0 bg-gradient-to-t from-black/75 via-black/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-400 pointer-events-none">
                        <!-- Photo number top-left -->
                        <div class="absolute top-3 left-3 text-white/60 text-xs font-mono tracking-wider">${pad}</div>

                        <!-- View icon center -->
                        <div class="absolute inset-0 flex items-center justify-center">
                            <div class="w-10 h-10 rounded-full bg-white/15 backdrop-blur-sm border border-white/30 flex items-center justify-center transform scale-75 group-hover:scale-100 transition-transform duration-500">
                                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                </svg>
                            </div>
                        </div>

                        <!-- Bottom accent bar -->
                        <div class="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-[#1C5BAE] via-[#1DA6E1] to-[#1C5BAE]"></div>
                    </div>

                    <!-- Subtle ring on hover -->
                    <div class="absolute inset-0 rounded-xl ring-0 group-hover:ring-1 ring-[#1C5BAE]/40 transition-all duration-300 pointer-events-none"></div>
                `;

                wrapper.addEventListener('click', function (e) {
                    e.stopPropagation();
                    openModal(i);
                });

                gallery.appendChild(wrapper);
            });

            // Modal navigation logic
            let currentImageIndex = 0;
            const images = data['gallery-images'];
            console.log('Gallery loaded with', images.length, 'images');

            function openModal(index) {
                console.log('Opening modal for image index:', index);
                currentImageIndex = index;
                const modal = document.getElementById('image-modal');
                const modalImg = document.getElementById('modal-img');
                const currentCounter = document.getElementById('current-image');
                const totalCounter = document.getElementById('total-images');

                console.log('Modal elements:', { modal, modalImg, currentCounter, totalCounter });

                if (modal && modalImg && currentCounter && totalCounter) {
                    modalImg.src = images[currentImageIndex];
                    currentCounter.textContent = currentImageIndex + 1;
                    totalCounter.textContent = images.length;
                    modal.classList.remove('hidden');
                    console.log('Modal opened successfully');
                } else {
                    console.error('Modal elements not found!');
                }
            }

            function showNextImage() {
                currentImageIndex = (currentImageIndex + 1) % images.length;
                const modalImg = document.getElementById('modal-img');
                const currentCounter = document.getElementById('current-image');
                if (modalImg && currentCounter) {
                    modalImg.src = images[currentImageIndex];
                    currentCounter.textContent = currentImageIndex + 1;
                }
            }

            function showPrevImage() {
                currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
                const modalImg = document.getElementById('modal-img');
                const currentCounter = document.getElementById('current-image');
                if (modalImg && currentCounter) {
                    modalImg.src = images[currentImageIndex];
                    currentCounter.textContent = currentImageIndex + 1;
                }
            }

            function closeModal() {
                const modal = document.getElementById('image-modal');
                const modalImg = document.getElementById('modal-img');
                if (modal && modalImg) {
                    modal.classList.add('hidden');
                    modalImg.src = '';
                }
            }

            // Event listeners - only add if elements exist
            const closeBtn = document.getElementById('close-modal');
            const modal = document.getElementById('image-modal');
            const nextBtn = document.getElementById('next-modal');
            const prevBtn = document.getElementById('prev-modal');

            if (closeBtn) {
                closeBtn.addEventListener('click', function (e) {
                    e.stopPropagation();
                    closeModal();
                });
            }

            if (nextBtn) {
                nextBtn.addEventListener('click', function (e) {
                    e.stopPropagation();
                    showNextImage();
                });
            }

            if (prevBtn) {
                prevBtn.addEventListener('click', function (e) {
                    e.stopPropagation();
                    showPrevImage();
                });
            }

            // Close on background click
            if (modal) {
                modal.addEventListener('click', function (e) {
                    if (e.target === modal) {
                        closeModal();
                    }
                });
            }

            // Keyboard navigation
            document.addEventListener('keydown', function (e) {
                const modal = document.getElementById('image-modal');
                if (modal && !modal.classList.contains('hidden')) {
                    if (e.key === 'ArrowRight') showNextImage();
                    if (e.key === 'ArrowLeft') showPrevImage();
                    if (e.key === 'Escape') closeModal();
                }
            });
        });
});
// --- CATEGORY CARD RENDER & CLICK REDIRECT ---
document.addEventListener('DOMContentLoaded', function () {
    fetch("./data/anupam-dutta-photography-data-set.json")
        .then(res => res.json())
        .then(data => {
            // Render categories
            if (data.categories && Array.isArray(data.categories)) {
                const container = document.getElementById('categories-container');
                container.innerHTML = '';
                data.categories.forEach((category, index) => {
                    const card = document.createElement('div');
                    card.className = "group relative w-full max-w-md bg-gradient-to-br from-white/5 via-white/10 to-white/5 backdrop-blur-xl border border-white/20 rounded-3xl shadow-2xl overflow-hidden transition-all duration-500 hover:shadow-[#1C5BAE]/20 hover:border-[#1C5BAE]/30 cursor-pointer";
                    card.setAttribute('data-category-index', index);

                    // Truncate description to 200 chars
                    const fullDesc = category.description;
                    const shortDesc = fullDesc.length > 200 ? fullDesc.slice(0, 200) + '...' : fullDesc;

                    card.innerHTML = `
                        <!-- Animated Background Gradient -->
                        <div class="absolute inset-0 bg-gradient-to-br from-[#1C5BAE]/5 via-[#1DA6E1]/5 to-[#1C5BAE]/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                        
                        <!-- Image Section with Overlay -->
                        <div class="relative overflow-hidden">
                            <div class="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                            <img class="relative w-full h-72 object-cover transform group-hover:scale-105 transition-transform duration-700" src="${category.image}" alt="${category.title}">
                            <div class="absolute bottom-0 left-0 right-0 z-20 opacity-0 group-hover:opacity-100 transition-opacity duration-500 p-4">
                                <div class="w-full h-1 bg-gradient-to-r from-[#1C5BAE] to-[#1DA6E1] rounded-full"></div>
                            </div>
                        </div>
                        
                        <!-- Content Section -->
                        <div class="relative px-6 py-8 md:px-8 md:py-10 z-10 space-y-4">
                            <h3 class="text-2xl md:text-3xl font-bold text-white tracking-wide leading-tight">${category.title}</h3>
                            <div class="w-20 h-1 bg-gradient-to-r from-[#1C5BAE] to-[#1DA6E1] rounded-full"></div>
                            <p class="text-gray-200 leading-relaxed text-base md:text-lg pt-2 card-desc">${shortDesc}</p>
                            ${fullDesc.length > 200 ? `
                                <button class="mt-2 px-6 py-3 bg-gradient-to-r from-[#1C5BAE] to-[#1DA6E1] text-white rounded-xl font-semibold hover:from-[#1DA6E1] hover:to-[#1C5BAE] transition-all shadow-lg hover:shadow-xl transform hover:scale-105 read-more-btn">Read More</button>
                                <button class="mt-2 px-6 py-3 bg-gradient-to-r from-gray-600 to-gray-700 text-white rounded-xl font-semibold hover:from-gray-700 hover:to-gray-800 transition-all shadow-lg hover:shadow-xl transform hover:scale-105 show-less-btn" style="display:none">Show Less</button>
                            ` : ''}
                        </div>
                    `;
                    // Card click (except button)
                    card.addEventListener('click', function (e) {
                        if (e.target.classList.contains('read-more-btn') || e.target.classList.contains('show-less-btn')) return;
                        const categoryIndex = card.getAttribute('data-category-index');
                        if (categoryIndex !== null) {
                            window.location.href = `./pages/category.html?category=${categoryIndex}`;
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
fetch("./data/anupam-dutta-photography-data-set.json")
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

// --- USEFUL LINKS SECTION ---
fetch("./data/anupam-dutta-photography-data-set.json")
    .then(res => res.json())
    .then(data => {
        const usefulLinksContainer = document.getElementById('useful-links-container');
        if (!usefulLinksContainer || !data['useful-links']) return;
        
        usefulLinksContainer.innerHTML = '';
        
        data['useful-links'].forEach((link, index) => {
            let domain = '';
            try {
                domain = new URL(link.url).hostname.replace(/^www\./, '');
            } catch (e) {
                domain = link.url;
            }

            const linkCard = document.createElement('div');
            linkCard.className = 'group relative bg-gradient-to-br from-white/5 to-white/10 backdrop-blur-xl border border-white/20 rounded-2xl p-6 hover:shadow-2xl hover:shadow-[#1C5BAE]/20 transition-all duration-300 transform hover:scale-105 hover:-translate-y-1';

            linkCard.innerHTML = `
                <a href="${link.url}" target="_blank" rel="noopener noreferrer" class="block">
                    <div class="flex items-center gap-4">
                        <!-- Icon -->
                        <div class="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-[#1C5BAE] to-[#1DA6E1] rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"></path>
                            </svg>
                        </div>

                        <!-- Content -->
                        <div class="flex-1 min-w-0">
                            <p class="text-xs font-semibold tracking-widest uppercase text-[#1DA6E1] mb-0.5">${link.title}</p>
                            <h3 class="text-base md:text-lg font-bold text-white truncate group-hover:text-[#1DA6E1] transition-colors duration-300">
                                ${domain}
                            </h3>
                            <p class="text-gray-400 text-xs flex items-center gap-1 mt-1">
                                Read article
                                <svg class="w-3 h-3 transform group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path>
                                </svg>
                            </p>
                        </div>

                        <!-- External arrow -->
                        <svg class="w-5 h-5 text-gray-600 group-hover:text-[#1DA6E1] transition-colors flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
                        </svg>
                    </div>

                    <!-- Animated border on hover -->
                    <div class="absolute inset-0 rounded-2xl border-2 border-transparent group-hover:border-[#1C5BAE]/50 transition-all duration-300 pointer-events-none"></div>
                </a>
            `;

            usefulLinksContainer.appendChild(linkCard);
        });
    })
    .catch(error => console.error('Error loading useful links:', error));
