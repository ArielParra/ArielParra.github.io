/**
 * @description Gets the current path for a 404 page considering that 404 pages can have any path.
 *              This function serves as an override of the original getCurrentPath function in language.js
 *
 * @returns {string} The 'en' (english) path for the 404 page.
 */
function getCurrentPath() {
    return '/404/';
}