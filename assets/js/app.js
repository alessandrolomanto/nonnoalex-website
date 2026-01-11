/**
 * Alessandro Lo Manto - Portfolio
 * Scroll animations and micro-interactions
 */

(function() {
  'use strict';

  /**
   * Intersection Observer for scroll animations
   */
  function initScrollAnimations() {
    const observerOptions = {
      root: null,
      rootMargin: '0px 0px -80px 0px',
      threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
          // Add staggered delay for multiple elements
          const delay = entry.target.dataset.delay || 0;
          setTimeout(() => {
            entry.target.classList.add('visible');
          }, delay * 100);
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    // Observe all elements with data-animate attribute
    const animatedElements = document.querySelectorAll('[data-animate]');
    animatedElements.forEach((el, index) => {
      el.dataset.delay = index % 3; // Stagger in groups of 3
      observer.observe(el);
    });

    // Observe service cards
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach((card, index) => {
      card.style.transitionDelay = `${index * 0.08}s`;
      observer.observe(card);
    });

    // Observe web3 cards
    const web3Cards = document.querySelectorAll('.web3-card');
    web3Cards.forEach((card, index) => {
      card.style.transitionDelay = `${index * 0.1}s`;
      observer.observe(card);
    });

    // Observe certs
    const certs = document.querySelectorAll('.cert');
    certs.forEach((cert, index) => {
      cert.style.transitionDelay = `${index * 0.08}s`;
      observer.observe(cert);
    });

    // Observe blog cards
    const blogCards = document.querySelectorAll('.blog-card');
    blogCards.forEach((card, index) => {
      card.style.transitionDelay = `${index * 0.1}s`;
      observer.observe(card);
    });
  }

  /**
   * Smooth scroll for anchor links
   */
  function initSmoothScroll() {
    const scrollLinks = document.querySelectorAll('a[href^="#"]');
    
    scrollLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        const targetId = link.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
          e.preventDefault();
          const offset = 20;
          const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - offset;
          
          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
          });
        }
      });
    });
  }

  /**
   * Subtle parallax effect on hero
   */
  function initHeroParallax() {
    const hero = document.querySelector('.hero');
    const heroGrid = document.querySelector('.hero-grid');
    
    if (!hero || !heroGrid) return;

    let ticking = false;

    function updateParallax() {
      const scrolled = window.pageYOffset;
      const rate = scrolled * 0.3;
      
      if (scrolled < window.innerHeight) {
        heroGrid.style.transform = `translateY(${rate}px)`;
        heroGrid.style.opacity = 1 - (scrolled / window.innerHeight);
      }
      
      ticking = false;
    }

    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(updateParallax);
        ticking = true;
      }
    }, { passive: true });
  }

  /**
   * Nav background on scroll
   */
  function initNavScroll() {
    const nav = document.querySelector('.nav');
    if (!nav) return;

    let lastScroll = 0;

    window.addEventListener('scroll', () => {
      const currentScroll = window.pageYOffset;
      
      if (currentScroll > 100) {
        nav.style.background = 'rgba(10, 10, 15, 0.9)';
        nav.style.backdropFilter = 'blur(10px)';
        nav.style.borderBottom = '1px solid rgba(255, 255, 255, 0.05)';
      } else {
        nav.style.background = 'transparent';
        nav.style.backdropFilter = 'none';
        nav.style.borderBottom = 'none';
      }
      
      lastScroll = currentScroll;
    }, { passive: true });
  }

  /**
   * Initialize everything when DOM is ready
   */
  function init() {
    initScrollAnimations();
    initSmoothScroll();
    initHeroParallax();
    initNavScroll();
  }

  // Start when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
