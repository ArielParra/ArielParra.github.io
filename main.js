/**
 * @description Initializes the website by setting up the default: language,
 *              navigation bar text, color theme, color theme button icon and  
 *              gif favicon. This function is called once every time the website loads.
 */
function main() {

    /* language */

    if ( cookieExists('language') === true ) {
      const cookieLang = getCookie('language');
      if(getCurrentSiteLanguage() !== cookieLang){
        changeLanguage(cookieLang);
      } else {
        /* stay in the same page */
      }
    } else if ( getCurrentSiteLanguage() !== getDefaultLanguage() ){ // && !cookieExists('language')
      changeLanguage(getDefaultLanguage());
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

    console.log('default lang = ' + getDefaultLanguage() );
    console.log('lang cookie  = ' + getCookie('language') );
    console.log('current site lang = ' + getCurrentSiteLanguage());
    console.log('current path = ' + getCurrentPath()); 
    console.log('browser prefers light = ' + browserPrefersLight());
    console.log('theme cookie = ' + getCookie('theme'));

}main();
