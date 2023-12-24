const currentPath = window.location.pathname;
const defaultLanguage = navigator.language.substring(0, 2);
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
    if(currentLanguage === 'es'){
        currentLanguage = 'en';
    } else {
        currentLanguage = 'es';
    }
    changeLanguage(currentLanguage);
    console.log('current lang ' + currentLanguage);
}
