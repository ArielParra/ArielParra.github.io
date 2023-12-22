const currentPath = window.location.pathname;
const defaultLanguage = navigator.language.substring(0, 2);
console.log('default browser lang ' + defaultLanguage);
let currentLanguage;

function detectLanguage() {
    if (defaultLanguage==='es' || currentPath.endsWith('/es') || 
        currentPath.endsWith('/es/') || currentPath.endsWith('/es/index.html') ) {
        currentLanguage = 'es';
    } else {
        currentLanguage = 'en';
    }
    console.log('current lang ' + currentLanguage);
}

function changeLanguage(currentLanguage) {
    let newPath;
    if (currentLanguage === 'es') {
        newPath = currentPath.replace(/\/index\.html$/, '/es');
        newPath = newPath.replace(/\/es\/es$/, '/es');
    } else {
        newPath = currentPath.replace(/\/es(\/index\.html)?$/, '');
    }

    window.location.href = newPath;
}

function langButton() {
    if (currentLanguage === 'es') {
        currentLanguage = 'en';
    } else {
        currentLanguage = 'es';
    }
    changeLanguage(currentLanguage);
    console.log('change lang with button to lang ' + currentLanguage);
}

/*main driver code*/
detectLanguage();
