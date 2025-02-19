//import { setCookie, getCookie, cookieExists } from './cookies.js';

/**
 * @description Changes the language of the website and updates the URL path accordingly.
 *
 * @param {string} language - The language code to set ('es' for Spanish, 'en' for English).
 */
function changeLanguage(language) {
    let currentPath = getCurrentPath();
    let params = window.location.search;
    setCookie('language', language, 30);
    let newPath;
    if (currentPath.endsWith('/') === true) {
        if (language === 'es') {
            newPath = currentPath + 'es';
        } else {
            newPath = currentPath.replace('es/', '');
        }
    } else if (currentPath.endsWith('index.html') === true) { /* for index.html (local developing) */
        if (language === 'es') {
            newPath = currentPath.replace('/index.html', '/es/index.html');
        } else { /* en */
            newPath = currentPath.replace('/es/index.html', '/index.html');
        }
    }
    if (newPath !== undefined) {
        window.location.href = newPath + params; // Append the query parameters to the new path
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
 * @description Checks if language cookie exists.
 */
document.addEventListener('DOMContentLoaded', () => {
    let defaultLang = getDefaultLanguage();
    if (defaultLang !== 'es') {
        defaultLang = 'en'; // default language is English
    }
    if (cookieExists('language') === true) {
        const cookieLang = getCookie('language');
        if (getCurrentSiteLanguage() !== cookieLang) {
            changeLanguage(cookieLang);
        }
        /*else {
            // stay in the same page
        }
        */
    } else if (getCurrentSiteLanguage() !== defaultLang) { // && !cookieExists('language')
        changeLanguage(defaultLang);
    }
});