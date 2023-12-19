let currentLanguage;

if (window.location.pathname.startsWith('./es') || navigator.language.startsWith('es') ) {
    currentLanguage = 'es';
} else {
    currentLanguage = 'en';
}
console.log('default lang ' + currentLanguage);

function changeLanguage(currentLanguage) {
    if (currentLanguage === 'es') {
        window.location.href = './es';
    } else {
        window.location.href = './';
    }
}

function langButton() {
    if (currentLanguage === 'es') {
        currentLanguage = 'en';
    } else {
        currentLanguage = 'es';
    }
    changeLanguage(currentLanguage);
    console.log('current lang ' + currentLanguage);
}
