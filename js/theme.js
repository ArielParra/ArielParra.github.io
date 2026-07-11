/* eslint-disable no-unused-vars */
// import { setCookie, getCookie, cookieExists } from './cookies.js';
/**
 * @description Sets the theme of the website.
 *
 * @param {string} selectedTheme - The theme to set. This should be either 'theme-dark' or 'theme-light'.
 */
function setTheme(selectedTheme) {
  setCookie("theme", selectedTheme, 30);
  document.documentElement.className = selectedTheme;
}

/**
 * @description Toggles the theme of the website between 'theme-dark' and 'theme-light'.
 *
 * @param {HTMLButtonElement} button - The button that triggered the theme change.
 */
function toggleTheme(button) {
  let newTheme;
  if (getCookie("theme") === "theme-dark") {
    newTheme = "theme-light";
    button.textContent = " 🌙 ";
  } else {
    newTheme = "theme-dark";
    button.textContent = " ☀️ ";
  }
  setTheme(newTheme);
}

/**
 * @description Checks if the browser prefers the light theme.
 *
 * @returns {boolean} - Returns true if the browser prefers the light theme, false otherwise.
 */
function browserPrefersLight() {
  if (window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches) {
    return true;
  }
  return false;
}

/**
 * @description Initializes the theme of the website.
 */
document.addEventListener("DOMContentLoaded", () => {
  const themeButton = document.getElementById("themeButton");
  if (themeButton) {
    themeButton.addEventListener("click", () => toggleTheme(themeButton));
  }
  let theme;
  if (cookieExists("theme")) {
    theme = getCookie("theme");
  } else { /* no cookie */
    if (browserPrefersLight() === true) {
      theme = "theme-light";
    } else {
      theme = "theme-dark";
    }
  }
  /* default button icon */
  if (theme === "theme-light") {
    themeButton.textContent = " 🌙 ";
  } else {
    themeButton.textContent = " ☀️ ";
  }

  setTheme(theme);
});
