/* eslint-disable no-unused-vars */

/**
 * Multi-language support is now handled statically by the Python generator.
 * This file provides a backward-compatible utility for other scripts.
 */

function getCurrentSiteLanguage() {
  return document.documentElement.lang || "en";
}
