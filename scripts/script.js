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
    fetch("../data/anupam-dutta-photography-data-set.json")
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
                    document.querySelectorAll('.logo-img').forEach(logoImg => {
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
                            window.location.href = `category.html?category=${categoryIndex}`;
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
    fetch("../data/anupam-dutta-photography-data-set.json")
        .then(res => res.json())
        .then(data => {
            const gallery = document.getElementById('gallery');
            if (!gallery || !data['gallery-images']) return;
            gallery.innerHTML = '';
            data['gallery-images'].forEach((img, i) => {
                const wrapper = document.createElement('div');

                // Create collage pattern with varying spans and heights
                let spanClass = '';
                let heightClass = 'h-64';

                // Pattern: large, medium, small repeating for visual interest
                if (i % 8 === 0) {
                    spanClass = 'sm:col-span-2 sm:row-span-2';
                    heightClass = 'h-96';
                } else if (i % 8 === 1 || i % 8 === 2) {
                    spanClass = 'sm:col-span-1';
                    heightClass = 'h-48';
                } else if (i % 8 === 3) {
                    spanClass = 'sm:col-span-2';
                    heightClass = 'h-72';
                } else if (i % 8 === 4 || i % 8 === 5) {
                    spanClass = 'sm:col-span-1';
                    heightClass = 'h-80';
                } else if (i % 8 === 6) {
                    spanClass = 'sm:col-span-1 sm:row-span-2';
                    heightClass = 'h-96';
                } else {
                    spanClass = 'sm:col-span-1';
                    heightClass = 'h-64';
                }

                wrapper.className = `group relative overflow-hidden rounded-2xl cursor-pointer transform transition-all duration-500 hover:scale-[1.02] hover:z-10 ${spanClass}`;

                wrapper.innerHTML = `
                    <!-- Image -->
                    <img src="${img}" 
                         class="w-full ${heightClass} object-cover object-center pointer-events-none" 
                         data-img="${img}" 
                         alt="Gallery Image ${i + 1}" />
                    
                    <!-- Overlay with gradient -->
                    <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none">
                        <div class="absolute inset-0 flex items-center justify-center">
                            <div class="transform translate-y-4 group-hover:translate-y-0 transition-transform duration-500">
                                <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7"></path>
                                </svg>
                            </div>
                        </div>
                        
                        <!-- Bottom accent line -->
                        <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-[#1C5BAE] via-[#1DA6E1] to-[#1C5BAE]"></div>
                    </div>
                    
                    <!-- Corner accent -->
                    <div class="absolute top-3 right-3 w-8 h-8 border-t-2 border-r-2 border-[#1C5BAE] opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>
                `;

                // Add click event for popup - make entire wrapper clickable
                wrapper.addEventListener('click', function (e) {
                    e.stopPropagation();
                    console.log('Image clicked, index:', i);
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
    fetch("../data/anupam-dutta-photography-data-set.json")
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
                            window.location.href = `category.html?category=${categoryIndex}`;
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
fetch("../data/anupam-dutta-photography-data-set.json")
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
