/**
 * Web Scraper Test Sites - Main JavaScript
 * Handles navigation toggle, dropdown menus, and interactive elements
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // ===================================
    // Mobile Navigation Toggle
    // ===================================
    const navbarToggler = document.getElementById('navbarToggler');
    const navbarMenu = document.getElementById('navbarMenu');
    
    if (navbarToggler && navbarMenu) {
        navbarToggler.addEventListener('click', function() {
            // Toggle active class on toggler for animation
            this.classList.toggle('active');
            
            // Toggle active class on menu to show/hide
            navbarMenu.classList.toggle('active');
            
            // Prevent body scroll when menu is open
            document.body.style.overflow = navbarMenu.classList.contains('active') ? 'hidden' : '';
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            const isClickInsideNav = navbarToggler.contains(event.target) || navbarMenu.contains(event.target);
            
            if (!isClickInsideNav && navbarMenu.classList.contains('active')) {
                navbarToggler.classList.remove('active');
                navbarMenu.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }
    
    // ===================================
    // Dropdown Menu Functionality
    // ===================================
    const learnDropdown = document.getElementById('learnDropdown');
    const learnDropdownMenu = document.getElementById('learnDropdownMenu');
    
    if (learnDropdown && learnDropdownMenu) {
        // For mobile: toggle dropdown on click
        learnDropdown.addEventListener('click', function(e) {
            if (window.innerWidth <= 768) {
                e.preventDefault();
                learnDropdownMenu.classList.toggle('active');
            }
        });
        
        // For desktop: show on hover (handled by CSS)
        // But we can add click functionality for better UX
        if (window.innerWidth > 768) {
            learnDropdown.addEventListener('click', function(e) {
                e.preventDefault();
                learnDropdownMenu.classList.toggle('active');
            });
            
            // Close dropdown when clicking outside
            document.addEventListener('click', function(event) {
                if (!learnDropdown.contains(event.target) && !learnDropdownMenu.contains(event.target)) {
                    learnDropdownMenu.classList.remove('active');
                }
            });
        }
    }
    
    // ===================================
    // Smooth Scroll for Anchor Links
    // ===================================
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Only handle if it's a valid anchor (not just #)
            if (href !== '#' && href.length > 1) {
                e.preventDefault();
                
                const targetId = href.substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    // Close mobile menu if open
                    if (navbarMenu && navbarMenu.classList.contains('active')) {
                        navbarToggler.classList.remove('active');
                        navbarMenu.classList.remove('active');
                        document.body.style.overflow = '';
                    }
                    
                    // Smooth scroll to target
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // ===================================
    // Navbar Scroll Effect
    // ===================================
    const navbar = document.getElementById('navbar');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Add shadow when scrolled
        if (scrollTop > 10) {
            navbar.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
        } else {
            navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        }
        
        lastScrollTop = scrollTop;
    });
    
    // ===================================
    // Card Image Lazy Loading (Optional Enhancement)
    // ===================================
    const cardImages = document.querySelectorAll('.card-image img');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    
                    // Add loaded class for animation
                    img.classList.add('loaded');
                    
                    // Stop observing this image
                    observer.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px'
        });
        
        cardImages.forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // ===================================
    // Handle Window Resize
    // ===================================
    let resizeTimer;
    window.addEventListener('resize', function() {
        // Clear the timeout
        clearTimeout(resizeTimer);
        
        // Set a new timeout
        resizeTimer = setTimeout(function() {
            // Close mobile menu if window is resized to desktop
            if (window.innerWidth > 768) {
                if (navbarMenu && navbarMenu.classList.contains('active')) {
                    navbarToggler.classList.remove('active');
                    navbarMenu.classList.remove('active');
                    document.body.style.overflow = '';
                }
                
                // Reset dropdown for desktop
                if (learnDropdownMenu) {
                    learnDropdownMenu.classList.remove('active');
                }
            }
        }, 250);
    });
    
    // ===================================
    // Accessibility: Keyboard Navigation
    // ===================================
    
    // ESC key to close mobile menu
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            if (navbarMenu && navbarMenu.classList.contains('active')) {
                navbarToggler.classList.remove('active');
                navbarMenu.classList.remove('active');
                document.body.style.overflow = '';
            }
            
            if (learnDropdownMenu && learnDropdownMenu.classList.contains('active')) {
                learnDropdownMenu.classList.remove('active');
            }
        }
    });
    
    // Focus trap for mobile menu
    if (navbarMenu) {
        const focusableElements = navbarMenu.querySelectorAll(
            'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])'
        );
        
        if (focusableElements.length > 0) {
            const firstFocusable = focusableElements[0];
            const lastFocusable = focusableElements[focusableElements.length - 1];
            
            navbarMenu.addEventListener('keydown', function(e) {
                if (e.key === 'Tab' && navbarMenu.classList.contains('active')) {
                    if (e.shiftKey) {
                        // Shift + Tab
                        if (document.activeElement === firstFocusable) {
                            e.preventDefault();
                            lastFocusable.focus();
                        }
                    } else {
                        // Tab
                        if (document.activeElement === lastFocusable) {
                            e.preventDefault();
                            firstFocusable.focus();
                        }
                    }
                }
            });
        }
    }
    
    // ===================================
    // Console Welcome Message
    // ===================================
    console.log('%c🚀 Web Scraper Test Sites', 'font-size: 20px; font-weight: bold; color: #31C3DB;');
    console.log('%cBuilt with HTML, CSS, and Vanilla JavaScript', 'font-size: 12px; color: #6c757d;');
    console.log('%cNo frameworks, just pure web development!', 'font-size: 12px; color: #6c757d;');
});

// ===================================
// Service Worker Registration (Optional)
// ===================================
if ('serviceWorker' in navigator) {
    // Uncomment to enable service worker for offline functionality
    // window.addEventListener('load', function() {
    //     navigator.serviceWorker.register('/sw.js').then(
    //         function(registration) {
    //             console.log('ServiceWorker registration successful');
    //         },
    //         function(err) {
    //             console.log('ServiceWorker registration failed: ', err);
    //         }
    //     );
    // });
}

// Made with Bob
