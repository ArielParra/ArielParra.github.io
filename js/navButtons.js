/**
 * @description Toggles the visibility of the navigation bar, with a smooth transition effect.
 *              Disables the provided button during the transition.
 * 
 * @param {HTMLButtonElement} button - The button triggering the navigation toggle.
 */
function toggleNavigation(button) {
  if (button.dataset.navShown === 'true') {
    hideNavBar(button,true);
  } else {
    showNavBar(button);
  }
}

/**
 * @description Hides the navigation bar with a smooth transition effect.
 *              Disables the provided button during the transition.
 * 
 * @param {HTMLButtonElement} button - The button triggering the hide operation.
 */
function hideNavBar(button, animation) {
  button.disabled = true;

  const elements = document.querySelectorAll('.NotCurrent, .current');
  
 
  for (let i = 0; i < elements.length; i++) {
    const elem = elements[i];
    if(animation === true){
      elem.style.transition = 'opacity 0.5s ease-in-out, margin-top 0.5s ease-in-out, visibility 0.5s ease-in-out';
    }
    elem.style.visibility = 'hidden';
    elem.style.opacity = 0;
    elem.style.marginTop = '-25%'; 
    elem.style.pointerEvents = 'none';
  }

  button.textContent = getCurrentSiteLanguage() === 'es' ? 'Mostrar Menú' : 'Show Nav Bar';
  setCookie('navStatus', 'hidden', 30);

  setTimeout(function() {
    button.dataset.navShown = 'false';
    button.disabled = false;
  }, 500);
}

/**
 * @description Shows the navigation bar with a smooth transition effect.
 *              Disables the provided button during the transition.
 * 
 * @param {HTMLButtonElement} button - The button triggering the show operation.
 */
function showNavBar(button) {
  button.disabled = true;

  const elements = document.querySelectorAll('.NotCurrent, .current');
  
  for (let i = 0; i < elements.length; i++) {
    const elem = elements[i];
    elem.style.transition = 'opacity 0.5s ease-in-out, margin-top 0.5s ease-in-out, visibility 0.5s ease-in-out';
    elem.style.visibility = 'visible';
    elem.style.opacity = 1;
    elem.style.marginTop = '0%';
    setTimeout(function(){
      elem.style.pointerEvents = 'auto';
    }, 500);
  }

  button.textContent = getCurrentSiteLanguage() === 'es' ? 'Ocultar Menú' : 'Hide Nav Bar';
  setCookie('navStatus', 'shown', 30);

  setTimeout(function() {
    button.dataset.navShown = 'true';
    button.disabled = false;
  }, 500);
}
