// Global Fallback Image Handler
(function () {
    'use strict';

    let fallbackImageUrl = 'https://placehold.co/150x150.webp?text=No+Image';

    // Function to load fallback image from JSON settings
    async function loadFallbackImage() {
        try {
            const response = await fetch('anupam-dutta-photography-data-set.json');
            if (!response.ok) return;

            const data = await response.json();

            if (data.settings && data.settings['fallback-image']) {
                fallbackImageUrl = data.settings['fallback-image'];
            }

            // Apply fallback to all existing images
            applyFallbackToImages();

        } catch (error) {
            console.log('Using default fallback image');
            applyFallbackToImages();
        }
    }

    // Apply fallback handler to all images on the page
    function applyFallbackToImages() {
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            if (!img.dataset.fallbackApplied) {
                img.dataset.fallbackApplied = 'true';
                img.addEventListener('error', function () {
                    if (this.src !== fallbackImageUrl) {
                        this.src = fallbackImageUrl;
                    }
                });
            }
        });
    }

    // Observe DOM for dynamically added images
    function observeNewImages() {
        const observer = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === 1) { // Element node
                        if (node.tagName === 'IMG') {
                            if (!node.dataset.fallbackApplied) {
                                node.dataset.fallbackApplied = 'true';
                                node.addEventListener('error', function () {
                                    if (this.src !== fallbackImageUrl) {
                                        this.src = fallbackImageUrl;
                                    }
                                });
                            }
                        }
                        // Check for images in child nodes
                        const imgs = node.querySelectorAll('img');
                        imgs.forEach(img => {
                            if (!img.dataset.fallbackApplied) {
                                img.dataset.fallbackApplied = 'true';
                                img.addEventListener('error', function () {
                                    if (this.src !== fallbackImageUrl) {
                                        this.src = fallbackImageUrl;
                                    }
                                });
                            }
                        });
                    }
                });
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // Export for use in other scripts
    window.getFallbackImageUrl = function () {
        return fallbackImageUrl;
    };

    window.setImageWithFallback = function (imgElement, url) {
        imgElement.src = url;
        if (!imgElement.dataset.fallbackApplied) {
            imgElement.dataset.fallbackApplied = 'true';
            imgElement.addEventListener('error', function () {
                if (this.src !== fallbackImageUrl) {
                    this.src = fallbackImageUrl;
                }
            });
        }
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            loadFallbackImage();
            observeNewImages();
        });
    } else {
        loadFallbackImage();
        observeNewImages();
    }

})();
