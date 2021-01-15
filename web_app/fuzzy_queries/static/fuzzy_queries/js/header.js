$(document).scroll(function() {
    navbarScroll();
  });
  
  function navbarScroll() {
    var y = window.scrollY;
    if (y > 10) {
      $('.header').addClass('small');
      $('.header_logo').addClass('small');
    } else if (y < 10) {
      $('.header').removeClass('small');
      $('.header_logo').removeClass('small');
    }
  }