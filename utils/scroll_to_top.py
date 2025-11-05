"""
Scroll to Top Button Component
Adds a floating button in the bottom-right corner that scrolls to top
"""

import streamlit as st
import streamlit.components.v1 as components


def render_scroll_to_top_button():
    """
    Renders a floating scroll-to-top button that appears after scrolling down.
    Should be called once in the main layout (e.g., in main.py or sidebar).
    """
    
    scroll_to_top_html = """
    <div id="scroll-to-top-container">
        <button id="scroll-to-top-btn" title="Przewiń na górę">
            ⬆️
        </button>
    </div>
    
    <script>
    (function() {
        // Get or create button
        let scrollBtn = document.getElementById('scroll-to-top-btn');
        
        if (!scrollBtn) {
            // Button doesn't exist in DOM yet (Streamlit initial load)
            return;
        }
        
        // Get main Streamlit container
        const getMainContainer = () => {
            return parent.document.querySelector('.main') || 
                   parent.document.querySelector('[data-testid="stAppViewContainer"]') ||
                   parent.window;
        };
        
        const mainContainer = getMainContainer();
        
        // Show/hide button based on scroll position
        const toggleButtonVisibility = () => {
            const scrollTop = mainContainer.scrollTop || parent.window.pageYOffset;
            
            if (scrollTop > 300) {
                scrollBtn.style.display = 'block';
                // Fade in animation
                setTimeout(() => {
                    scrollBtn.style.opacity = '1';
                }, 10);
            } else {
                scrollBtn.style.opacity = '0';
                setTimeout(() => {
                    scrollBtn.style.display = 'none';
                }, 300);
            }
        };
        
        // Scroll to top function
        const scrollToTop = () => {
            const scrollTarget = mainContainer.scrollTop !== undefined ? mainContainer : parent.window;
            
            scrollTarget.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        };
        
        // Event listeners
        if (mainContainer.addEventListener) {
            mainContainer.addEventListener('scroll', toggleButtonVisibility);
        } else {
            parent.window.addEventListener('scroll', toggleButtonVisibility);
        }
        
        scrollBtn.addEventListener('click', scrollToTop);
        
        // Initial check
        toggleButtonVisibility();
        
        // Handle Streamlit reruns
        const observer = new MutationObserver(() => {
            toggleButtonVisibility();
        });
        
        observer.observe(parent.document.body, {
            childList: true,
            subtree: true
        });
    })();
    </script>
    
    <style>
    #scroll-to-top-btn {
        opacity: 0;
        transition: opacity 0.3s ease, transform 0.3s ease;
    }
    </style>
    """
    
    components.html(scroll_to_top_html, height=0)
