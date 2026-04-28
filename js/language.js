/* eslint-disable no-unused-vars */
// import { setCookie, getCookie, cookieExists } from './cookies.js';

/**
 * @description Changes the language of the website and updates the URL path accordingly.
 *
 * @param {string} language - The language code to set ('es' for Spanish, 'en' for English).
 */
function applyLanguage(language) {
  document.documentElement.lang = language;
  document.querySelectorAll(".i18n").forEach((el) => {
    el.innerHTML = el.getAttribute(`data-i18n-${language}`);
  });
  document.querySelectorAll("[data-i18n-en]").forEach((el) => {
    const attrEn = el.getAttribute("data-i18n-en");
    const attrEs = el.getAttribute("data-i18n-es");
    if (attrEn && attrEs) {
      const attrName = el.tagName === "IMG" ? "alt" : "title";
      el.setAttribute(attrName, el.getAttribute(`data-i18n-${language}`));
    }
  });
  document.querySelectorAll("[data-i18n-alt-en]").forEach((el) => {
    el.setAttribute("alt", el.getAttribute(`data-i18n-alt-${language}`));
  });
  document.querySelectorAll("[data-i18n-title-en]").forEach((el) => {
    el.setAttribute("title", el.getAttribute(`data-i18n-title-${language}`));
  });

  // Update page title

  const titleEn = document.documentElement.getAttribute("data-i18n-title-en");
  const titleEs = document.documentElement.getAttribute("data-i18n-title-es");
  if (titleEn && titleEs) {
    document.title = language === "en" ? titleEn : titleEs;
  }

  // Update meta tags
  const metaKeywords = document.querySelector("meta[name=\"keywords\"]");
  if (metaKeywords) {
    metaKeywords.setAttribute("content", metaKeywords.getAttribute(`data-i18n-keywords-${language}`));
  }
  const metaDescription = document.querySelector("meta[name=\"description\"]");
  if (metaDescription) {
    metaDescription.setAttribute("content", metaDescription.getAttribute(`data-i18n-description-${language}`));
  }
}

function changeLanguage(language) {
  setCookie("language", language, 30);
  applyLanguage(language);
  updateLangButton(language);
  updateMenuButtonLanguage(language);
  window.dispatchEvent(new CustomEvent("languageChanged", { detail: { language } }));
}

function updateLangButton(language) {
  const langBtnElem = document.getElementById("langButton");
  if (langBtnElem) {
    const i18nSpan = langBtnElem.querySelector(".i18n");
    if (i18nSpan) {
      i18nSpan.innerHTML = i18nSpan.getAttribute(`data-i18n-${language}`);
    } else {
      langBtnElem.textContent = language === "en" ? "Español" : "English";
    }
  }
}
/**
 * @description Returns the opposite language code.
 *
 * @param {string} language - The current language code.
 * @returns {string}        - The opposite language code ('es' if 'en' and vice versa).
 */
function oppositeLanguage(language) {
  if (language === "en") {
    return "es";
  }
  return "en";
}

/**
 * @description Handles the click event for a language button, changing the language and disabling the button temporarily.
 *
 * @param {HTMLButtonElement} button - The language button that triggered the event.
 */
function langButton(button) {
  button.disabled = true;
  let currentLanguage;
  if (cookieExists("language")) {
    currentLanguage = getCookie("language");
  } else {
    currentLanguage = getCurrentSiteLanguage();
  }

  changeLanguage(oppositeLanguage(currentLanguage));
  setTimeout(() => {
    button.disabled = false;
  }, 500);
}

/* getters */

/**
 * @description Gets the current path of the website.
 *
 * @returns {string} - The current URL path.
 */
function getCurrentPath() {
  return window.location.pathname;
}

/**
 * @description Gets the current language of the website based on the cookie.
 *
 * @returns {string} - The current language code ('es' for Spanish, 'en' for English).
 */
function getCurrentSiteLanguage() {
  if (cookieExists("language")) {
    return getCookie("language");
  }
  return "en";
}

/**
 * @description Gets the default language of the user's browser.
 *
 * @returns {string} - The default language code using only the first 2 characters
 */
function getDefaultLanguage() {
  return navigator.language.substring(0, 2);
}

/**
 * @description Initialize language on page load.
 */
document.addEventListener("DOMContentLoaded", () => {
  let lang = getDefaultLanguage();
  if (lang !== "es") lang = "en";
  if (cookieExists("language")) {
    lang = getCookie("language");
  }
  applyLanguage(lang);
  updateLangButton(lang);

  // Also update menu button text on initial load
  const menuButton = document.getElementById("menuButton");
  if (menuButton) {
    const i18nSpan = menuButton.querySelector(".i18n");
    if (i18nSpan) {
      i18nSpan.innerHTML = i18nSpan.getAttribute(`data-i18n-${lang}`);
    }
  }
});

function updateMenuButtonLanguage(language) {
  const menuButton = document.getElementById("menuButton");
  if (menuButton) {
    const i18nSpan = menuButton.querySelector(".i18n");
    if (i18nSpan) {
      i18nSpan.innerHTML = i18nSpan.getAttribute(`data-i18n-${language}`);
    }
  }
}
