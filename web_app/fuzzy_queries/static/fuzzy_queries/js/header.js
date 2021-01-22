$(document).scroll(function() {
    navbarScroll();
  });
  
  function navbarScroll() {
    var y = window.scrollY;
    if (y > 10) {
      $('.header').addClass('small');
      $('.header_logo').addClass('small');
      $('.header_sentence').addClass('small');
      $('.foot').addClass('small');
    } else if (y < 10) {
      $('.header').removeClass('small');
      $('.header_logo').removeClass('small');
      $('.header_sentence').removeClass('small');
      $('.foot').removeClass('small');
    }
  }