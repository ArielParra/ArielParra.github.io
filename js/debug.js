/**
 * @description Calls all debugging functions.
 */
function dbgAll() {
    dbgMessages();
    dbgCookies();
    dbgLocalStorage();
    dbgSessionStorage();
}
/**
 * @description Toggles the visibility of the navigation bar, with a smooth transition effect.
 *              Disables the provided button during the transition.
 */
function dbgMessages() {
    console.log('default lang = ' + getDefaultLanguage() );
    console.log('lang cookie  = ' + getCookie('language') );
    console.log('current site lang = ' + getCurrentSiteLanguage());
    console.log('current path = ' + getCurrentPath()); 
    console.log('curren site' + window.location.href);
    console.log('browser prefers light = ' + browserPrefersLight());
    console.log('theme cookie = ' + getCookie('theme'));
    console.log('device width = ' + window.screen.width + 'px');
    console.log('navStatus = ' + getCookie('navStatus') );
}
/**
 * @description get all cookies
 * 
 */
function dbgCookies() {
    console.log('Cookies:');
    let cookies = document.cookie;
    if (cookies === "") {
        console.log("No cookies found");
    } else {
        cookies.split(';').forEach(cookie => {
            let [name, value] = cookie.split('=');
            console.log(`Cookie Name: ${name.trim()}, Cookie Value: ${value}`);
        });
    }
}


/**
 * @description Logs all key-value pairs from local storage.
 */
function dbgLocalStorage() {
    console.log('Local storage items:');
    if (localStorage.length === 1) {
        console.log('No items found in local storage.');
    } else {
        for (let i = 0; i < localStorage.length; i++) {
            let key = localStorage.key(i);
            console.log(`Key: ${key}, Value: ${localStorage.getItem(key)}`);
        }
    }
}

/**
 * @description Logs all key-value pairs from session storage.
 */
function dbgSessionStorage() {
    console.log('Session storage items:');
    if (sessionStorage.length === 0) {
        console.log('No items found in session storage.');
    } else {
        for (let i = 0; i < sessionStorage.length; i++) {
            let key = sessionStorage.key(i);
            console.log(`Key: ${key}, Value: ${sessionStorage.getItem(key)}`);
        }
    }
}