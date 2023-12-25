function changeLanguage(language) {
    let currentPath = getCurrentPath();
    console.log('current path = ' + currentPath);
    setCookie('language', language, 30);
    let newPath;
    if (currentPath.endsWith('/') === true) {
        if (language === 'es') {
            newPath = currentPath + 'es';
        } else {
            newPath = currentPath.replace('es/', '');
        }
    } else if (currentPath.endsWith('index.html') === true) { /* for index.html */
        if (language === 'es') {
            newPath = currentPath.replace('/index.html', '/es');
        } else { /* en */
            newPath = currentPath.replace('/es/index.html', '/index.html');
        }
    }
    console.log('input = ' + language  + ', new path = ' + newPath);
    if(newPath !== undefined){
        window.location.href = newPath;
    }
}

function oppositeLanguage(language) {
    if (language === 'es') {
        return 'en';
    }
    return 'es';
}

function langButton(button){
    button.disabled = true;
    let currentLanguage;
    if ( cookieExists('language') ) {
        currentLanguage = getCookie('language');
    } else { 
        currentLanguage = getCurrentSiteLanguage();
    }

    changeLanguage(oppositeLanguage(currentLanguage));    
    setTimeout(function() {
        button.disabled = false;
    }, 500);
}

/* getters */
function getCurrentPath(){
    return window.location.pathname;

}
function getCurrentSiteLanguage(){
    let currentPath = getCurrentPath();
    if(currentPath.endsWith('/es/') || currentPath.endsWith('/es/index.html')){
        return 'es';
    }
    return 'en';
}
function getDefaultLanguage(){
    return navigator.language.substring(0, 2);
}
