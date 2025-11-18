document.addEventListener("DOMContentLoaded", async () => {
    /* 
        NAVBAR SCROLL EFFECT
   */
    const navbar = document.querySelector("nav");

    function handleNavbarBg() {
        if (window.scrollY > 10) {
            navbar.classList.add("bg-gray-900", "shadow-md");
        } else {
            navbar.classList.remove("bg-gray-900", "shadow-md");
        }
    }
    window.addEventListener("scroll", handleNavbarBg);
    handleNavbarBg();

    
    let data;
    try {
        const res = await fetch("images.json");
        data = await res.json();
    } catch (err) {
        console.error("Error loading images.json:", err);
        return;
    }

  
    const sliderImage = document.getElementById("slider-image");
    const dotsContainer = document.getElementById("dots");
    let currentIndex = 0;
    function changeSlide(index) {
        currentIndex = index;

        sliderImage.classList.remove("opacity-100");
        sliderImage.classList.add("opacity-0");

        setTimeout(() => {
            sliderImage.src = data["slider-images"][index];
            sliderImage.classList.remove("kenburns-zoom");
            void sliderImage.offsetWidth;
            sliderImage.classList.remove("opacity-0");
            sliderImage.classList.add("opacity-100");
            sliderImage.classList.add("kenburns-zoom");
        }, 400);

        updateDots();
    }

    function createDots() {
        data["slider-images"].forEach((_, i) => {
            const dot = document.createElement("div");
            dot.className = `w-3 h-3 rounded-full cursor-pointer transition ${i === 0 ? "bg-white" : "bg-white/50"}`;
            dot.addEventListener("click", () => changeSlide(i));
            dotsContainer.appendChild(dot);
        });
    }

    function updateDots() {
        Array.from(dotsContainer.children).forEach((dot, i) => {
            dot.className = "w-3 h-3 rounded-full cursor-pointer transition " + (i === currentIndex ? "bg-white" : "bg-white/50");
        });
    }

    // Initialize slider
    sliderImage.src = data["slider-images"][0];
    createDots();
    setInterval(() => {
        currentIndex = (currentIndex + 1) % data["slider-images"].length;
        changeSlide(currentIndex);
    }, 8000);

    /*
        CATEGORY CARDS - BIG & BEAUTIFUL LAYOUT
   */
    const container = document.getElementById("categories-container");
    container.innerHTML = "";

    data.categories.forEach((category, index) => {
        const isEven = index % 2 === 0;
        
        const card = document.createElement("div");
        card.className = `category-card w-full max-w-7xl mx-auto my-6  transition-all duration-1000 transform ${isEven ? '-translate-x-20' : 'translate-x-20'} opacity-0`;
        
        card.innerHTML = `
            <div class="flex flex-col overflow-hidden ${isEven ? 'md:flex-row' : 'md:flex-row-reverse'} items-center gap-10">
                <!-- Image Section -->
                <div class="w-full  md:w-1/2 ${isEven ? 'md:pr-8' : 'md:pl-8'}">
                    <div class="${isEven ? 'slide-in-image-left' : 'slide-in-image-right'} transform ${isEven ? 'translate-x-[-100px]' : 'translate-x-[100px]'} opacity-0 transition-all overflow-hidden duration-1000 delay-300">
                        <img class="w-full h-[300px] md:h-[500px] object-cover rounded-2xl shadow-2xl hover:shadow-3xl transition-all duration-700 shadow-lg hover:scale-105" 
                             src="${category.image}" 
                             alt="${category.title}">
                    </div>
                </div>
                
                <!-- Text Content Section -->
                <div class="w-full md:w-1/2 ${isEven ? 'md:pl-8' : 'md:pr-8'}">
                    <div class="${isEven ? 'slide-in-text-left' : 'slide-in-text-right'} transform ${isEven ? 'translate-x-[-80px]' : 'translate-x-[80px]'} opacity-0 transition-all duration-1000 delay-500">
                        <h3 class="text-4xl md:text-5xl font-bold mb-6 text-gray-100 font-serif">${category.title}</h3>
                        <p class="text-gray-300 text-lg md:text-xl leading-relaxed mb-8 font-light">${category.description}</p>
                        <button class="explore-btn px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl font-semibold text-md">
                            Explore ${category.title} →
                        </button>
                    </div>
                </div>
            </div>
        `;

        // Explore button click
        const exploreBtn = card.querySelector(".explore-btn");
        exploreBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            window.location.href = category.url;
        });

        container.appendChild(card);
    });

    /*
        SMOOTH CATEGORY SCROLL REVEAL - FIXED VERSION
     */
    const categoryCards = document.querySelectorAll(".category-card");

    const cardObserver = new IntersectionObserver(
        (entries, obs) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    // Animate main card immediately
                    entry.target.classList.add("translate-x-0", "opacity-100");
                    
                    // Find image and text elements
                    const imageElement = entry.target.querySelector('.slide-in-image-left, .slide-in-image-right');
                    const textElement = entry.target.querySelector('.slide-in-text-left, .slide-in-text-right');
                    
                    // Animate image with delay
                    if (imageElement) {
                        setTimeout(() => {
                            imageElement.classList.add('translate-x-0', 'opacity-100');
                        }, 300);
                    }
                    
                    // Animate text with longer delay
                    if (textElement) {
                        setTimeout(() => {
                            textElement.classList.add('translate-x-0', 'opacity-100');
                        }, 600);
                    }
                    
                    obs.unobserve(entry.target);
                }
            });
        },
        { 
            threshold: 0.1,
            rootMargin: "0px 0px -100px 0px"
        }
    );

    categoryCards.forEach((card) => cardObserver.observe(card));

    /* ==============================
       GALLERY SECTION
    ============================== */
    const gallery = document.getElementById("gallery");
gallery.innerHTML = "";

data["gallery-images"].forEach((img, i) => {
    const extra = i % 6 === 0 ? "row-span-2 col-span-2" : 
                 i % 5 === 0 ? "row-span-2" : 
                 i % 4 === 0 ? "col-span-2" : "";
    
    const galleryItem = document.createElement("div");
    galleryItem.className = `overflow-hidden rounded-lg ${extra} cursor-pointer gallery-item transform translate-y-10 opacity-0 transition-all duration-700 relative group`;
    galleryItem.innerHTML = `
        <img src="${img}" 
             class="w-full h-full object-cover gallery-img hover:scale-110 transition-transform duration-500" 
             data-img="${img}" />
        <!-- Simple Click to View Text -->
        <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none">
    <span class="text-white text-xs font-medium bg-gray-500 bg-opacity-40 px-3 py-1.5 rounded-md backdrop-blur-sm">
        Click to view
    </span>
</div>
    `;
    
    gallery.appendChild(galleryItem);
});

    /* GALLERY SCROLL REVEAL */
    const galleryItems = document.querySelectorAll(".gallery-item");
    const galleryObserver = new IntersectionObserver(
        (entries, obs) => {
            entries.forEach((entry, i) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.classList.add("translate-y-0", "opacity-100");
                    }, i * 100);
                    obs.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.1 }
    );

    galleryItems.forEach((item) => galleryObserver.observe(item));

    /*
        MODAL
     */
    const modal = document.getElementById("image-modal");
    const modalImg = document.getElementById("modal-img");
    const closeBtn = document.getElementById("close-modal");

    gallery.addEventListener("click", (e) => {
        if (e.target.classList.contains("gallery-img")) {
            modalImg.src = e.target.dataset.img;
            modal.classList.remove("hidden");
            setTimeout(() => {
                modal.classList.add("show");
                modalImg.classList.add("show");
            }, 10);
        }
    });

    function closeModal() {
        modalImg.classList.remove("show");
        modal.classList.remove("show");
        setTimeout(() => modal.classList.add("hidden"), 400);
    }

    closeBtn.addEventListener("click", closeModal);
    modal.addEventListener("click", (e) => {
        if (e.target === modal) closeModal();
    });
    window.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && !modal.classList.contains("hidden")) closeModal();
    });

    /*
       CONTACT FORM
     */
    const form = document.getElementById("contact-form");
    if (form) {
        form.addEventListener("submit", (e) => {
            e.preventDefault();
            const name = form.querySelector('input[placeholder="Your name"]').value;
            const email = form.querySelector('input[type="email"]').value;
            const subject = form.querySelector('input[placeholder="Photography inquiry"]').value;
            const message = form.querySelector("textarea").value;

            const mailto = `mailto:manish7479dlp@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent("Name: " + name + "\nEmail: " + email + "\n\n" + message)}`;
            window.location.href = mailto;
        });
    }
});