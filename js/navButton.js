/**
 * @description Toggles the visibility of the navigation bar, with a smooth transition effect.
 *              Disables the provided button during the transition.
 * 
 * @param {HTMLButtonElement} button - The button triggering the navigation toggle.
 */
function toggleNavigation(button) {
  button.disabled = true;

  const elements = document.querySelectorAll('.NotCurrent, .current');
  
  for (let i = 0; i < elements.length; i++) {
    const elem = elements[i];
    elem.style.transition = 'opacity 0.5s ease-in-out, margin-top 0.5s ease-in-out, visibility 0.5s ease-in-out';
    if (button.dataset.navShown === 'true') {
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

  let currentLanguage = getCurrentSiteLanguage();

  if (button.dataset.navShown === 'true') {
    if(currentLanguage === 'es'){
      button.textContent = 'Mostrar Barra';
    } else {
      button.textContent = 'Show Nav Bar';
    }
  } else {
    if(currentLanguage === 'es'){
      button.textContent = 'Ocultar Barra';
    } else {
      button.textContent = 'Hide Nav Bar';
    }
  }

  setTimeout(function() {
    if (button.dataset.navShown === 'true') {
      button.dataset.navShown = 'false';
    } else {
      button.dataset.navShown = 'true';
    }
    button.disabled = false;
  }, 500);
}
