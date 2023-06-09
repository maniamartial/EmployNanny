 var ratingStars = document.querySelectorAll('.rating .fa-star');

    ratingStars.forEach(function(star) {
      star.addEventListener('click', function() {
        var starsContainer = this.parentElement;
        var starsInput = starsContainer.nextElementSibling;
        var starsCount = parseInt(this.getAttribute('data-star'));
        starsInput.value = starsCount;
        for (var i = 0; i < ratingStars.length; i++) {
          if (i < starsCount) {
            ratingStars[i].classList.add('checked');
          } else {
            ratingStars[i].classList.remove('checked');
          }
        }
      });
      
      star.addEventListener('mouseover', function() {
        var starsCount = parseInt(this.getAttribute('data-star'));
        for (var i = 0; i < ratingStars.length; i++) {
          if (i < starsCount) {
            ratingStars[i].classList.add('hover');
          } else {
            ratingStars[i].classList.remove('hover');
          }
        }
      });
      
      star.addEventListener('mouseout', function() {
        for (var i = 0; i < ratingStars.length; i++) {
          ratingStars[i].classList.remove('hover');
        }
      });
    });