
    document.addEventListener('DOMContentLoaded', function() {
      const urlParams = new URLSearchParams(window.location.search);
      const registered = urlParams.get('registered');

      if (registered) {
          alert('You are already registered as ' + '{{ user.username }}');
      }
  });





      function watchLatest() {
      window.open("https://youtube.com/@IShowSpeed", "_blank");
    }




    function visitMerchStore() {
      window.open("https://www.ishowspeed.store/", "_blank");
    }

    $(document).ready(function() {
      const images = $('.hypnosis-image');
      let currentIndex = 0;

      // Initialize - show first image
      $(images[currentIndex]).addClass('active');

      setInterval(function() {
        // Get current and next image
        const currentImage = $(images[currentIndex]);
        const nextIndex = (currentIndex + 1) % images.length;
        const nextImage = $(images[nextIndex]);

        // Start fade out current image
        currentImage.removeClass('active').addClass('fade-out');

        // After fade out completes, reset and prepare for next appearance
        setTimeout(function() {
          currentImage.removeClass('fade-out');
          currentImage.css('opacity', '0');

          // Show next image with appear animation
          nextImage.addClass('active');

          // Update current index
          currentIndex = nextIndex;
        }, 3000);

      }, 8000);
    });


     // Comments slider functionality
  $(document).ready(function() {
    const commentGroups = $('.comment-group');
    let currentGroup = 0;

    // Show first group
    $(commentGroups[currentGroup]).addClass('active');

    // Auto-rotate comments every 8 seconds
    setInterval(function() {
      // Fade out current group
      $(commentGroups[currentGroup]).removeClass('active');

      // Calculate next group
      currentGroup = (currentGroup + 1) % commentGroups.length;

      // Fade in next group
      $(commentGroups[currentGroup]).addClass('active');
    }, 8000);
  });


  document.getElementById('myVideo').addEventListener('ended', function() {
    this.currentTime = 0;
    this.play();
  });

$(document).ready(function() {
  // Initialize carousel
  const cardsContainer = $('#cardsContainer');
  const cards = $('.speed-card');
  const leftArrow = $('.arrow-left');
  const rightArrow = $('.arrow-right');
  const wrapper = $('.cards-wrapper');

  if (cardsContainer.length === 0 || cards.length === 0) return;

  // State
  let currentIndex = 0;
  let autoSlideInterval;
  const gap = 28;
  let cardWidth = cards[0].offsetWidth;
  let touchStartX = 0;
  let touchEndX = 0;
  let isDragging = false;
  let dragOffset = 0;
  let wrapperWidth = wrapper.width();

  // Calculate max scroll position
  function calculateMaxScroll() {
    wrapperWidth = wrapper.width();
    const totalWidth = (cards.length * (cardWidth + gap)) - gap;
    return Math.max(0, totalWidth - wrapperWidth);
  }

  // Update carousel position
  function updateCards() {
    const maxScroll = calculateMaxScroll();
    let translateX = -currentIndex * (cardWidth + gap) + dragOffset;

    // Ensure we don't scroll past the last card
    if (currentIndex >= cards.length - Math.floor(wrapperWidth / (cardWidth + gap))) {
      translateX = -maxScroll;
    }

    cardsContainer.css('transform', `translateX(${translateX}px)`);
  }

  // Move carousel manually
  function moveCarousel(step) {
    clearInterval(autoSlideInterval);

    const visibleCards = Math.floor(wrapperWidth / (cardWidth + gap));
    const maxIndex = cards.length - visibleCards;

    currentIndex += step;

    // Boundary checks with loop
    if (currentIndex < 0) {
      currentIndex = maxIndex;
    } else if (currentIndex > maxIndex) {
      currentIndex = 0;
    }

    dragOffset = 0;
    updateCards();
    startAutoSlide();
  }

  // Auto-slide function
  function startAutoSlide() {
    clearInterval(autoSlideInterval);
    autoSlideInterval = setInterval(function() {
      moveCarousel(1);
    }, 5000);
  }

  // Event listeners for arrows
  leftArrow.on('click', function() {
    moveCarousel(-1);
  });

  rightArrow.on('click', function() {
    moveCarousel(1);
  });

  // Touch event handlers for mobile swipe
  cardsContainer.on('touchstart', function(e) {
    clearInterval(autoSlideInterval);
    touchStartX = e.originalEvent.touches[0].clientX;
    isDragging = true;
  });

  cardsContainer.on('touchmove', function(e) {
    if (!isDragging) return;
    touchEndX = e.originalEvent.touches[0].clientX;
    dragOffset = touchEndX - touchStartX;
    updateCards();
  });

  cardsContainer.on('touchend', function() {
    if (!isDragging) return;
    isDragging = false;

    if (Math.abs(dragOffset) > 50) {
      if (dragOffset > 0) {
        moveCarousel(-1);
      } else {
        moveCarousel(1);
      }
    } else {
      dragOffset = 0;
      updateCards();
      startAutoSlide();
    }
  });

  // Handle window resize
  function handleResize() {
    cardWidth = cards[0].offsetWidth;
    wrapperWidth = wrapper.width();
    updateCards();
  }

  // Initialize
  handleResize();
  startAutoSlide();
  $(window).on('resize', handleResize);
});


document.addEventListener("DOMContentLoaded", function () {
  let animationStarted = false;

  function isElementInViewport(el, offset = 100) {
    const rect = el.getBoundingClientRect();
    return (
      rect.top <= (window.innerHeight || document.documentElement.clientHeight) - offset
    );
  }

  function animateCounter(element, target, duration) {
    let start = 0;
    const startTime = performance.now();

    function update(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const value = Math.floor(progress * target);
      element.textContent = value;

      if (progress < 1) {
        requestAnimationFrame(update);
      } else {
        element.textContent = target; // Final value
      }
    }

    requestAnimationFrame(update);
  }

  function startAnimations() {
    const countElement = document.querySelector(".count-number");
    if (countElement) {
      const target = parseInt(countElement.getAttribute("data-count"));
      animateCounter(countElement, target, 3000); // 3 seconds
    }
  }

  window.addEventListener("scroll", function () {
    const targetSection = document.querySelector(".user-count-section");
    if (!targetSection) return;

    if (!animationStarted && isElementInViewport(targetSection, 100)) {
      animationStarted = true;
      startAnimations();
    }
  });
});