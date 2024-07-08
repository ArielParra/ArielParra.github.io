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
        changeLanguage(cookieLang);
      } else {
        /* stay in the same page */
      }
    } else if ( getCurrentSiteLanguage() !== defaultLang ){ // && !cookieExists('language')
      changeLanguage(defaultLang);
    }
    
    /* navigation bar */

    const navButton = document.getElementById('navButton');

    // Check if the 'navStatus' cookie exists
    if (cookieExists('navStatus')) {
      const navStatus = getCookie('navStatus');
    
      // Check the status and update the button text accordingly
      if (navStatus === 'hidden') {
        hideMenu(navButton, false);
        console.log('trying');
        navButton.textContent = getCurrentSiteLanguage() === 'es' ? 'Mostrar Menú' : 'Show Menu';
      } else {
        navButton.textContent = getCurrentSiteLanguage() === 'es' ? 'Ocultar Menú' : 'Hide Menu';
      }
    } else {
      // Default: Navigation bar is visible
      navButton.textContent = getCurrentSiteLanguage() === 'es' ? 'Ocultar Menú' : 'Hide Menu';
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
      setInterval(animateFavicon, 800);
    }else {
      // For Firefox
      var link = document.createElement('link');
      link.rel = 'icon';
      link.href = './images/favicon.gif';
      link.type = 'image/gif';
      document.head.appendChild(link);
    } 
    
}main();