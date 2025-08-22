/**
 * Mobile Navigation Component for ZenDegenAcademy
 * Provides bottom tab navigation for mobile devices
 */

class MobileNavigation {
    constructor() {
        this.currentPage = 'dashboard';
        this.init();
    }

    init() {
        this.createNavigation();
        this.setupEventListeners();
        this.updateActiveState();
    }

    createNavigation() {
        // Remove existing mobile nav if present
        const existing = document.querySelector('.mobile-bottom-nav');
        if (existing) {
            existing.remove();
        }

        // Create navigation HTML
        const navHTML = `
            <div class="mobile-bottom-nav">
                <div class="mobile-nav-items">
                    <div class="mobile-nav-item" data-page="dashboard">
                        <div class="mobile-nav-icon">🏠</div>
                        <div class="mobile-nav-label">Start</div>
                    </div>
                    <div class="mobile-nav-item" data-page="lesson">
                        <div class="mobile-nav-icon">📚</div>
                        <div class="mobile-nav-label">Nauka</div>
                    </div>
                    <div class="mobile-nav-item" data-page="skills">
                        <div class="mobile-nav-icon">🌳</div>
                        <div class="mobile-nav-label">Mapa</div>
                    </div>
                    <div class="mobile-nav-item" data-page="profile">
                        <div class="mobile-nav-icon">👤</div>
                        <div class="mobile-nav-label">Profil</div>
                        <div class="mobile-nav-badge" style="display: none;">!</div>
                    </div>
                </div>
            </div>
        `;

        // Insert navigation into DOM
        document.body.insertAdjacentHTML('beforeend', navHTML);
    }

    setupEventListeners() {
        const navItems = document.querySelectorAll('.mobile-nav-item');
        
        navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const targetPage = item.dataset.page;
                this.navigateToPage(targetPage);
            });

            // Add touch feedback
            item.addEventListener('touchstart', () => {
                item.style.transform = 'scale(0.95)';
            });

            item.addEventListener('touchend', () => {
                setTimeout(() => {
                    item.style.transform = '';
                }, 100);
            });
        });
    }

    navigateToPage(pageName) {
        // Update current page
        this.currentPage = pageName;
        
        // Update visual state
        this.updateActiveState();
        
        // Trigger Streamlit page change
        this.triggerStreamlitNavigation(pageName);
        
        // Add page transition effect
        this.addPageTransition();
    }

    updateActiveState() {
        const navItems = document.querySelectorAll('.mobile-nav-item');
        
        navItems.forEach(item => {
            item.classList.remove('active');
            if (item.dataset.page === this.currentPage) {
                item.classList.add('active');
            }
        });
    }

    triggerStreamlitNavigation(pageName) {
        // Map page names to Streamlit session state
        const pageMapping = {
            'dashboard': 'dashboard',
            'lesson': 'lesson', 
            'skills': 'lesson', // Skills are in lesson view
            'profile': 'profile'
        };

        const streamlitPage = pageMapping[pageName] || 'dashboard';
        
        // Try to trigger Streamlit navigation via session state
        if (window.parent && window.parent.streamlit) {
            try {
                window.parent.streamlit.setComponentValue({
                    action: 'navigate',
                    page: streamlitPage
                });
            } catch (e) {
                console.log('Streamlit integration not available, using fallback');
                this.fallbackNavigation(streamlitPage);
            }
        } else {
            this.fallbackNavigation(streamlitPage);
        }
    }

    fallbackNavigation(pageName) {
        // Fallback: try to click corresponding buttons or simulate navigation
        const buttons = document.querySelectorAll('button');
        const pageButtons = {
            'dashboard': ['Start', 'Dashboard', '🏠'],
            'lesson': ['Nauka', 'Lekcje', '📚'],
            'profile': ['Profil', 'Profile', '👤']
        };

        const targetTexts = pageButtons[pageName] || [];
        
        for (const button of buttons) {
            const buttonText = button.textContent.trim();
            if (targetTexts.some(text => buttonText.includes(text))) {
                button.click();
                break;
            }
        }
    }

    addPageTransition() {
        const mainContent = document.querySelector('.main');
        if (mainContent) {
            mainContent.classList.remove('page-transition');
            // Force reflow
            mainContent.offsetHeight;
            mainContent.classList.add('page-transition');
        }
    }

    // Public methods for external control
    setCurrentPage(pageName) {
        this.currentPage = pageName;
        this.updateActiveState();
    }

    showBadge(pageName, count = '') {
        const item = document.querySelector(`[data-page="${pageName}"]`);
        if (item) {
            const badge = item.querySelector('.mobile-nav-badge');
            if (badge) {
                badge.textContent = count;
                badge.style.display = count ? 'flex' : 'none';
            }
        }
    }

    hideBadge(pageName) {
        this.showBadge(pageName, '');
    }

    // Detect current page from URL or DOM
    detectCurrentPage() {
        // Try to detect from Streamlit session state or DOM
        const title = document.title.toLowerCase();
        const url = window.location.href.toLowerCase();
        
        if (title.includes('lesson') || title.includes('nauka') || url.includes('lesson')) {
            return 'lesson';
        } else if (title.includes('profile') || title.includes('profil') || url.includes('profile')) {
            return 'profile';
        } else if (title.includes('skills') || url.includes('skills')) {
            return 'skills';
        } else {
            return 'dashboard';
        }
    }
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize on mobile/tablet devices
    if (window.innerWidth <= 1024) {
        window.mobileNav = new MobileNavigation();
        
        // Detect current page
        const currentPage = window.mobileNav.detectCurrentPage();
        window.mobileNav.setCurrentPage(currentPage);
    }
});

// Handle window resize
window.addEventListener('resize', () => {
    if (window.innerWidth <= 1024) {
        // Initialize if not already present
        if (!window.mobileNav) {
            window.mobileNav = new MobileNavigation();
        }
    } else {
        // Remove mobile nav on desktop
        if (window.mobileNav) {
            const nav = document.querySelector('.mobile-bottom-nav');
            if (nav) nav.remove();
            window.mobileNav = null;
        }
    }
});

// Export for manual control
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MobileNavigation;
}
