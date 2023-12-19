let navShown = true;

function toggleNavigation(button) {
  button.disabled = true;

  const elements = document.querySelectorAll('.NotCurrent, .current');
  
  for (let i = 0; i < elements.length; i++) {
    const elem = elements[i];
    elem.style.transition = 'opacity 0.5s ease-in-out, margin-top 0.5s ease-in-out, visibility 0.5s ease-in-out';
    if (navShown) {
      elem.style.visibility = 'hidden';
      elem.style.opacity = 0;
      elem.style.marginTop = '-25%'; 
      elem.style.pointerEvents = 'none';
    } else {
      elem.style.visibility = 'visible';
      elem.style.opacity = 1;
      elem.style.marginTop = '0%';
      setTimeout(function(){
        elem.style.pointerEvents = 'auto';
      }, 500);
    }
  }

  setTimeout(function() {
    navShown = !navShown;
    button.disabled = false;
  }, 500);
}
    