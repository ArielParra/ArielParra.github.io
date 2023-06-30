
 
    var currentlanguage;
    if (navigator.language.startsWith('es')) {
        currentlanguage = 'es';
        console.log('default lang es');
    } else {
        currentlanguage = 'en';
        console.log('default lang en');

    }
    changeLanguage(currentlanguage);
    
    function langbutton(){
        if (currentlanguage=='es') {
            currentlanguage = 'en';
        }
        else {
            currentlanguage = 'es';
        }
    changeLanguage(currentlanguage);
    }

    function changeLanguage(currentlanguage) {
        Array.from(document.getElementsByClassName('lang')).forEach(function (elem) {
            if (elem.classList.contains(currentlanguage)) {
                 elem.style.display = 'initial';
            }
            else {
                 elem.style.display = 'none';
            }
        });
      }

