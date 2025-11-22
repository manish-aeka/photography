// --- ALL DOMContentLoaded LOGIC COMBINED ---
document.addEventListener('DOMContentLoaded', function () {
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
    fetch("images.json")
        .then(res => res.json())
        .then(data => {
            // Render categories
            if (data.categories && Array.isArray(data.categories)) {
                const container = document.getElementById('categories-container');
                container.innerHTML = '';
                data.categories.forEach(category => {
                    const card = document.createElement('div');
                    card.className = "w-[420px] min-h-[420px] bg-white text-gray-900 max-w-2xl rounded-xl overflow-hidden shadow-lg hover:scale-105 transition-transform duration-300";
                    card.setAttribute('data-category-url', category.url);

                    // Truncate description to 200 chars
                    const fullDesc = category.description;
                    const shortDesc = fullDesc.length > 200 ? fullDesc.slice(0, 200) + '...' : fullDesc;

                    card.innerHTML = `
                        <img class="w-full h-[280px] object-cover rounded-t-xl" src="${category.image}" alt="${category.title}">
                        <div class="px-8 py-6">
                            <div class="font-bold text-2xl mb-3">${category.title}</div>
                            <p class="text-gray-700 text-lg card-desc">${shortDesc}</p>
                            ${fullDesc.length > 200 ? `
                                <button class=\"mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 read-more-btn\">Read More</button>
                                <button class=\"mt-4 px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400 show-less-btn\" style=\"display:none\">Show Less</button>
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
    fetch("images.json")
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
fetch("images.json")
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
    fetch("images.json")
        .then(res => res.json())
        .then(data => {
            // Render categories
            if (data.categories && Array.isArray(data.categories)) {
                const container = document.getElementById('categories-container');
                container.innerHTML = '';
                data.categories.forEach(category => {
                    const card = document.createElement('div');
                    card.className = "w-[420px] min-h-[420px] bg-white text-gray-900 max-w-2xl rounded-xl overflow-hidden shadow-lg hover:scale-105 transition-transform duration-300";
                    card.setAttribute('data-category-url', category.url);

                    // Truncate description to 200 chars
                    const fullDesc = category.description;
                    const shortDesc = fullDesc.length > 200 ? fullDesc.slice(0, 200) + '...' : fullDesc;

                    card.innerHTML = `
                        <img class="w-full h-[280px] object-cover rounded-t-xl" src="${category.image}" alt="${category.title}">
                        <div class="px-8 py-6">
                            <div class="font-bold text-2xl mb-3">${category.title}</div>
                            <p class="text-gray-700 text-lg card-desc">${shortDesc}</p>
                            ${fullDesc.length > 200 ? `
                                <button class=\"mt-4 px-4 py-2 bg-indigo-500 text-white rounded hover:bg-indigo-600 read-more-btn\">Read More</button>
                                <button class=\"mt-4 px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400 show-less-btn\" style=\"display:none\">Show Less</button>
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
fetch("images.json")
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
