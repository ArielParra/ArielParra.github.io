/**
 * @description Changes the language of the website and updates the URL path accordingly.
 *
 * @param {string} language - The language code to set ('es' for Spanish, 'en' for English).
 */
function changeLanguage404(language) {
  let currentPath = '/404/';
  setCookie('language', language, 30);
  let newPath;
  if (currentPath.endsWith('/') === true) {
      if (language === 'es') {
          newPath = currentPath + 'es';
      } else {
          newPath = currentPath;
      }
  } else if (currentPath.endsWith('index.html') === true) { /* for index.html */
      if (language === 'es') {
          newPath = currentPath.replace('/index.html', '/es');
      } else { /* en */
          newPath = currentPath;
      }
  }
  if(newPath !== undefined){
      window.location.href = newPath;
  }
}

function langButton404(button){
  button.disabled = true;
  let currentLanguage;
  if ( cookieExists('language') ) {
      currentLanguage = getCookie('language');
  } else { 
      currentLanguage = getCurrentSiteLanguage();
  }

  changeLanguage404(oppositeLanguage(currentLanguage));    
  setTimeout(function() {
      button.disabled = false;
  }, 500);
}
/**
 * @description Initializes the website by setting up the default: language,
 *              navigation bar text, color theme, color theme button icon and  
 *              gif favicon. This function is called once every time the website loads.
 */
function main() {
  
  /* language */
  
  /* to consider other defaultLanguages as 'en' */
  let defaultLang = getDefaultLanguage();
  if (defaultLang !== 'es'){
    defaultLang = 'en';
  }
  if ( cookieExists('language') === true ) {
    const cookieLang = getCookie('language');
    if(getCurrentSiteLanguage() !== cookieLang){
      changeLanguage404(cookieLang);
    } else {
      /* stay in the same page */
    }
  } else if ( getCurrentSiteLanguage() !== defaultLang ){ // && !cookieExists('language')
    changeLanguage404(defaultLang);
  }
  
  /* navigation bar */

  /* will always be on by default */
  const navButton = document.getElementById('navButton');
  /* default button text */
  if(getCurrentSiteLanguage() === 'es'){
    navButton.textContent = 'Ocultar Barra';
  }else {
    navButton.textContent = 'Hide Nav Bar';
  }


  /* color theme */

  const themeButton = document.getElementById('themeButton');
  let theme;
  if (cookieExists('theme')) {
    theme = getCookie('theme');
  } else { /* no cookie */
    if (browserPrefersLight() === true) {
      theme = 'theme-light';
    } else {
      theme = 'theme-dark';
    }  
  }
  /* default button icon */
  if (theme === 'theme-light') {
    themeButton.textContent = ' 🌙 ';
  } else {
    themeButton.textContent = ' ☀️ ';
  }

  setTheme(theme);

  /* dynamic icon */

  if (navigator.userAgent.toLowerCase().indexOf('firefox') === -1) {
    //for all the other chromium based browsers that doesnt support dynamic favicons
    setInterval(animateIcon, 800);
  }

  /* debug messages */

  console.log('404 default lang = ' + getDefaultLanguage() );
  console.log('404 lang cookie  = ' + getCookie('language') );
  console.log('404 current site lang = ' + getCurrentSiteLanguage());
  console.log('404 current path = ' + getCurrentPath()); 
  console.log('404 browser prefers light = ' + browserPrefersLight());
  console.log('404 theme cookie = ' + getCookie('theme'));

}main();
