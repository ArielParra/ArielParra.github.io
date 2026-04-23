//import { setCookie, getCookie, cookieExists } from './cookies.js';

/**
 * @description Changes the language of the website and updates the URL path accordingly.
 *
 * @param {string} language - The language code to set ('es' for Spanish, 'en' for English).
 */
function changeLanguage(language) {
    setCookie('language', language, 30);
    document.documentElement.lang = language;
    document.querySelectorAll('.i18n').forEach(el => {
        el.innerHTML = el.getAttribute(`data-i18n-${language}`);
    });
document.querySelectorAll('[data-i18n-en]').forEach(el => {
    const attrEn = el.getAttribute('data-i18n-en');
    const attrEs = el.getAttribute('data-i18n-es');
    if (attrEn && attrEs) {
      const attrName = el.tagName === 'IMG' ? 'alt' : 'title';
      el.setAttribute(attrName, el.getAttribute(`data-i18n-${language}`));
    }
  });
  // Handle data-i18n-alt-en and data-i18n-alt-es on any element (especially images)
  document.querySelectorAll('[data-i18n-alt-en]').forEach(el => {
    el.setAttribute('alt', el.getAttribute(`data-i18n-alt-${language}`));
  });
  // Handle data-i18n-title-en and data-i18n-title-es on any element
  document.querySelectorAll('[data-i18n-title-en]').forEach(el => {
    el.setAttribute('title', el.getAttribute(`data-i18n-title-${language}`));
  });
    updateLangButton(language);
}

function updateLangButton(language) {
    const langButton = document.getElementById('langButton');
    if (langButton) {
        langButton.textContent = language === 'en' ? 'Español' : 'English';
    }
}
/**
 * @description Returns the opposite language code.
 *
 * @param {string} language - The current language code.
 * @returns {string}        - The opposite language code ('es' if 'en' and vice versa).
 */
function oppositeLanguage(language) {
    if (language === 'en') {
        return 'es';
    }
    return 'en';
}

/**
 * @description Handles the click event for a language button, changing the language and disabling the button temporarily.
 *
 * @param {HTMLButtonElement} button - The language button that triggered the event.
 */
function langButton(button) {
    button.disabled = true;
    let currentLanguage;
    if (cookieExists('language')) {
        currentLanguage = getCookie('language');
    } else {
        currentLanguage = getCurrentSiteLanguage();
    }

    changeLanguage(oppositeLanguage(currentLanguage));
    setTimeout(function () {
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
 * @description Gets the current language of the website based on the URL path.
 *
 * @returns {string} - The current language code ('es' for Spanish, 'en' for English).
 */
function getCurrentSiteLanguage() {
    let currentPath = getCurrentPath();
    if (currentPath.endsWith('/es/') || currentPath.endsWith('/es/index.html')) {
        return 'es';
    }
    return 'en';
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
document.addEventListener('DOMContentLoaded', () => {
    let lang = getDefaultLanguage();
    if (lang !== 'es') lang = 'en';
    if (cookieExists('language')) {
        lang = getCookie('language');
    }
    document.documentElement.lang = lang;
    updateLangButton(lang);
});