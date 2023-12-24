const currentPath = window.location.pathname;
let currentLanguage;

function changeLanguage(language) {
    setCookie('language', language, 30);
    let newPath;
    if (language === 'es') {
        newPath = currentPath.replace(/\/index\.html$/, '/es');
    } else {
        newPath = currentPath.replace(/\/es(\/index\.html)?$/, '');
    }
    window.location.href = newPath;
    //console.log('website changed to = ' + newPath );
}

function langButton() {
    if(currentLanguage === 'es'){
        currentLanguage = 'en';
    } else {
        currentLanguage = 'es';
    }
    if( (currentLanguage !== currentLanguageSite) ){ // && !cookieExists('language')
        changeLanguage(currentLanguage);
    } 
}
