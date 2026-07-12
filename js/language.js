/* eslint-disable no-unused-vars */

/**
 * Multi-language support is now handled statically by the Python generator.
 * This file provides a backward-compatible utility and handles explicit language selection cookies.
 */

function getCurrentSiteLanguage() {
  return document.documentElement.lang || "en";
}

function changeLanguage(langCode, href) {
  setCookie("language", langCode, 365);
  window.location.href = href;
}
