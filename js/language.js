function changeLanguage(language) {
    let currentPath = getCurrentPath();
    setCookie('language', language, 30);
    let newPath;
    if (language === 'es') {
        newPath = currentPath.replace(/\/index\.html$/, '/es');
    } else {
        newPath = currentPath.replace(/\/es(\/index\.html)?$/, '');
    }
    window.location.href = newPath;
    console.log('language path changed to ' + newPath);
}

function oppositeLanguage(language) {
    if (language === 'es') {
        return 'en';
    }
    return 'es';
}

function langButton(){
    let currentLanguage;

    if ( cookieExists('language') ) {
        currentLanguage = getCookie('language');
        changeLanguage(oppositeLanguage(currentLanguage)); 
        console.log('1language changed to ' + oppositeLanguage(currentLanguage));
    } else { 
        currentLanguage = getCurrentLanguageSite();
        console.log('2language changed to ' + oppositeLanguage(currentLanguage));

        changeLanguage(oppositeLanguage(currentLanguage));    
    }
}

/* getters */
function getCurrentPath(){
    return window.location.pathname;

}
function getCurrentLanguageSite(){
    let currentPath = getCurrentPath();
    if(currentPath.endsWith('/es/') || currentPath.endsWith('/es/index.html')){
        return 'es';
    }
    return 'en';
}
function getDefaultLanguage(){
    return defaultLanguage = navigator.language.substring(0, 2);
}
