/* eslint-disable no-unused-vars */
// import { setCookie } from './cookies.js';

/**
 * @description Toggles the visibility of the navigation bar menu, with a smooth transition effect.
 *              Disables the provided button during the transition.
 *
 * @param {HTMLButtonElement} button - The button triggering the navigation toggle.
 */
function toggleMenu(button) {
  if (button.dataset.navShown === "true") {
    hideMenu(button, true);
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

  const elements = document.querySelectorAll(".NotCurrent, .current");

  for (let i = 0; i < elements.length; i++) {
    const elem = elements[i];
    if (animation === true) {
      elem.style.transition = "opacity 0.5s ease-in-out, margin-top 0.5s ease-in-out, visibility 0.5s ease-in-out";
    }
    elem.style.visibility = "hidden";
    elem.style.opacity = 0;
    elem.style.marginTop = "-25%";
    elem.style.pointerEvents = "none";
  }

  const span = button.querySelector("span");
  if (span) {
    span.innerHTML = button.getAttribute("data-text-show");
  }

  setCookie("menuStatus", "hidden", 30);

  setTimeout(() => {
    button.dataset.navShown = "false";
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

  const elements = document.querySelectorAll(".NotCurrent, .current");

  for (let i = 0; i < elements.length; i++) {
    const elem = elements[i];
    elem.style.transition = "opacity 0.5s ease-in-out, margin-top 0.5s ease-in-out, visibility 0.5s ease-in-out";
    elem.style.visibility = "visible";
    elem.style.opacity = 1;
    elem.style.marginTop = "0%";
    setTimeout(() => {
      elem.style.pointerEvents = "auto";
    }, 500);
  }

  const span = button.querySelector("span");
  if (span) {
    span.innerHTML = button.getAttribute("data-text-hide");
  }

  setCookie("menuStatus", "shown", 30);

  setTimeout(() => {
    button.dataset.navShown = "true";
    button.disabled = false;
  }, 500);
}

/**
 * @description Initializes the menu status.
 */
document.addEventListener("DOMContentLoaded", () => {
  const menuButton = document.getElementById("menu-button");
  if (menuButton) {
    menuButton.addEventListener("click", () => toggleMenu(menuButton));
  }

  // Check if the 'menuStatus' cookie exists
  if (cookieExists("menuStatus")) {
    const menuStatus = getCookie("menuStatus");

    // Check the status and update the button text accordingly
    if (menuStatus === "hidden") {
      hideMenu(menuButton, false);
      const span = menuButton.querySelector("span");
      if (span) {
        span.innerHTML = menuButton.getAttribute("data-text-show");
      }
    }
  }
});
