//import { setCookie } from './cookies.js';

/**
 * @description Toggles the visibility of the navigation bar menu, with a smooth transition effect.
 *              Disables the provided button during the transition.
 * 
 * @param {HTMLButtonElement} button - The button triggering the navigation toggle.
 */
function toggleMenu(button) {
  if (button.dataset.navShown === 'true') {
    hideMenu(button,true);
  } else {
    showMenu(button);
  }
}

/**
 * @description Hides the navigation bar with a smooth transition effect.
 *              Disables the provided button during the transition.
 * 
 * @param {HTMLButtonElement} button - The button triggering the hide operation.
 */
function hideMenu(button, animation) {
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

  button.textContent = getCurrentSiteLanguage() === 'es' ? 'Mostrar Menú' : 'Show Menu';
  setCookie('menuStatus', 'hidden', 30);

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
function showMenu(button) {
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

  button.textContent = getCurrentSiteLanguage() === 'es' ? 'Ocultar Menú' : 'Hide Menu';
  setCookie('menuStatus', 'shown', 30);

  setTimeout(function() {
    button.dataset.navShown = 'true';
    button.disabled = false;
  }, 500);
}


/**
 * @description Initializes the menu status. 
 */
document.addEventListener('DOMContentLoaded', () => {
  const menuButton = document.getElementById('menuButton');

  // Check if the 'menuStatus' cookie exists
  if (cookieExists('menuStatus')) {
    const menuStatus = getCookie('menuStatus');

    // Check the status and update the button text accordingly
    if (menuStatus === 'hidden') {
      hideMenu(menuButton, false);
      menuButton.textContent = getCurrentSiteLanguage() === 'es' ? 'Mostrar Menú' : 'Show Menu';
    } else {
      menuButton.textContent = getCurrentSiteLanguage() === 'es' ? 'Ocultar Menú' : 'Hide Menu';
    }
  } else {
    // Default: Navigation bar is visible
    menuButton.textContent = getCurrentSiteLanguage() === 'es' ? 'Ocultar Menú' : 'Hide Menu';
  }
});
