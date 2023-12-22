let currentPath = window.location.pathname;
console.log('current path = ' + currentPath);
const defaultLanguage = navigator.language.substring(0, 2);
console.log('default lang = ' + defaultLanguage);

console.log('lang cookie = ' + getCookie('language') );
let currentLanguage;

function detectLanguage() {
    const storedLanguage = getCookie('language');
    if (storedLanguage) {
        currentLanguage = storedLanguage;
    } else {
        if ( (currentPath.endsWith('/es') || currentPath.endsWith('/es/index.html')  || defaultLanguage === 'es') ) {
            currentLanguage = 'es';
        }else{
            currentLanguage = 'en';
        }
    }
    console.log('current lang  = ' + currentLanguage);
}
function changeLanguage(language) {
    setCookie('language', language, 365);
    let newPath;
    if (language === 'es') {
        newPath = currentPath.replace(/\/index\.html$/, '/es');
    } else {
        newPath = currentPath.replace(/\/es(\/index\.html)?$/, '');
    }
    console.log('lang cookie = ' + getCookie('language') );

 //   window.location.href = newPath;
}

function langButton() {
    currentLanguage = (currentLanguage === 'es') ? 'en' : 'es';
    changeLanguage(currentLanguage);
    console.log('current lang ' + currentLanguage);
}

function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    const sameSite = ';SameSite=None';
    const secure = ';Secure'; /*because of HTTPS*/
    document.cookie = name + '=' + value  + ';expires=' + expires.toUTCString() + ';path=/' + sameSite + secure;
}

function getCookie(name) {
    const nameEQ = name + '=';
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i];
        while (cookie.charAt(0) === ' ') cookie = cookie.substring(1, cookie.length);
        if (cookie.indexOf(nameEQ) === 0) return cookie.substring(nameEQ.length, cookie.length);
    }
    return null;
}

  function checkCookie() {
    if (getCookie('language') != null) {
      alert("cookie lang = " + getCookie('language').toString() );
    } else if ( (!currentPath.endsWith('/es') && !currentPath.endsWith('/es/index.html')  &&
    defaultLanguage === 'es') && getCookie()===null && !getCookie()===undefined  ) {
        changeLanguage(defaultLanguage);
    }
  }
/* main driver code */
function main(){
    detectLanguage();
}main();