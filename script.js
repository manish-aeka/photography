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

        // Fade out (do NOT remove kenburns-zoom here!)
        sliderImage.classList.remove("opacity-100");
        sliderImage.classList.add("opacity-0");

        setTimeout(() => {
            // Change image
            sliderImage.src = data["slider-images"][index];

            // Reset animation properly so it starts clean
            sliderImage.classList.remove("kenburns-zoom");
            void sliderImage.offsetWidth; // IMPORTANT — forces reflow

            // Fade in + restart zoom-in animation
            sliderImage.classList.remove("opacity-0");
            sliderImage.classList.add("opacity-100");
            sliderImage.classList.add("kenburns-zoom");
        }, 400); // Fade duration (match with CSS opacity duration)

        updateDots();
    }

    function createDots() {
        data["slider-images"].forEach((_, i) => {
            const dot = document.createElement("div");
            dot.className = `w-3 h-3 rounded-full cursor-pointer transition ${i === 0 ? "bg-white" : "bg-white/50"
                }`;
            dot.addEventListener("click", () => changeSlide(i));
            dotsContainer.appendChild(dot);
        });
    }

    function updateDots() {
        Array.from(dotsContainer.children).forEach((dot, i) => {
            dot.className =
                "w-3 h-3 rounded-full cursor-pointer transition " +
                (i === currentIndex ? "bg-white" : "bg-white/50");
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
        CATEGORY CARDS (Dynamic) with LEFT SLIDE ANIMATION
   */
    const container = document.getElementById("categories-container");
    container.innerHTML = "";

    data.categories.forEach((category, index) => {
        const card = document.createElement("div");
        card.className =
            `category-card w-[420px] bg-white text-gray-900 rounded-xl overflow-hidden shadow-lg transition-all duration-700 transform translate-x-[-100px] opacity-0 ${index % 2 === 0 ? 'slide-in-left' : 'slide-in-right'}`;
        card.setAttribute("data-category-url", category.url);

        const fullDesc = category.description;
        const shortDesc =
            fullDesc.length > 200 ? fullDesc.slice(0, 200) + "..." : fullDesc;

        card.innerHTML = `
      <img class="w-full h-[280px] object-cover" src="${category.image}" alt="${category.title}">
      <div class="px-6 py-4">
        <h3 class="text-2xl font-bold mb-2">${category.title}</h3>
        <p class="text-gray-700 text-lg card-desc">${shortDesc}</p>
        ${fullDesc.length > 200
                ? `
              <button class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 read-more-btn">
                Read More
              </button>
              <button class="mt-4 px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400 show-less-btn hidden">
                Show Less
              </button>`
                : ""
            }
      </div>
    `;

        // Card click navigation
        card.addEventListener("click", (e) => {
            if (
                e.target.classList.contains("read-more-btn") ||
                e.target.classList.contains("show-less-btn")
            )
                return;
            window.location.href = category.url;
        });

        // Read More / Show Less logic
        const btnRead = card.querySelector(".read-more-btn");
        const btnLess = card.querySelector(".show-less-btn");
        if (btnRead && btnLess) {
            btnRead.addEventListener("click", (e) => {
                e.stopPropagation();
                card.querySelector(".card-desc").textContent = fullDesc;
                btnRead.classList.add("hidden");
                btnLess.classList.remove("hidden");
            });
            btnLess.addEventListener("click", (e) => {
                e.stopPropagation();
                card.querySelector(".card-desc").textContent = shortDesc;
                btnRead.classList.remove("hidden");
                btnLess.classList.add("hidden");
            });
        }

        container.appendChild(card);
    });

    /*
        CATEGORY SCROLL REVEAL - SMOOTH LEFT SLIDE
     */
    const categoryCards = document.querySelectorAll(".category-card");

    const cardObserver = new IntersectionObserver(
        (entries, obs) => {
            entries.forEach((entry, i) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.classList.add("translate-x-0", "opacity-100");
                    }, i * 200); // staggered delay
                    obs.unobserve(entry.target);
                }
            });
        },
        { 
            threshold: 0.1,
            rootMargin: "0px 0px -50px 0px"
        }
    );

    categoryCards.forEach((card) => cardObserver.observe(card));

    /* ==============================
       🏞️ GALLERY SECTION - HANGING ANIMATION
    ============================== */
    const gallery = document.getElementById("gallery");
    gallery.innerHTML = "";

    data["gallery-images"].forEach((img, i) => {
        const extra =
            i % 6 === 0
                ? "row-span-2 col-span-2"
                : i % 5 === 0
                    ? "row-span-2"
                    : i % 4 === 0
                        ? "col-span-2"
                        : "";
        
        const galleryItem = document.createElement("div");
        galleryItem.className = `overflow-hidden rounded-lg ${extra} cursor-pointer gallery-item transform translate-y-[-50px] opacity-0 scale-95 transition-all duration-1000`;
        galleryItem.innerHTML = `<img src="${img}" class="w-full h-full object-cover gallery-img hover:scale-110 transition-transform duration-700" data-img="${img}" />`;
        
        gallery.appendChild(galleryItem);
    });

    /* 
        GALLERY SCROLL REVEAL - HANGING STAGGERED ANIMATION
    */
    const galleryItems = document.querySelectorAll(".gallery-item");

    const galleryObserver = new IntersectionObserver(
        (entries, obs) => {
            entries.forEach((entry, i) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.classList.add(
                            "translate-y-0", 
                            "opacity-100", 
                            "scale-100",
                            "hang-animation"
                        );
                    }, i * 150); // staggered hanging effect
                    obs.unobserve(entry.target);
                }
            });
        },
        { 
            threshold: 0.1,
            rootMargin: "0px 0px -50px 0px"
        }
    );

    galleryItems.forEach((item) => galleryObserver.observe(item));

    /*
        CINEMATIC MODAL
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
       CONTACT FORM MAILTO
     */
    const form = document.getElementById("contact-form");
    if (form) {
        form.addEventListener("submit", (e) => {
            e.preventDefault();
            const name = form.querySelector('input[placeholder="Your name"]').value;
            const email = form.querySelector('input[type="email"]').value;
            const subject = form.querySelector(
                'input[placeholder="Photography inquiry"]'
            ).value;
            const message = form.querySelector("textarea").value;

            const mailto = `mailto:manish7479dlp@gmail.com?subject=${encodeURIComponent(
                subject
            )}&body=${encodeURIComponent(
                "Name: " + name + "\nEmail: " + email + "\n\n" + message
            )}`;
            window.location.href = mailto;
        });
    }
});