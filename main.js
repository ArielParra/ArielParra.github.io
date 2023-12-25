/*function that sets the buttons, cookies, etc.
  called once everytime the website loads */
function main() {
    /* language */

    if ( cookieExists('language') === true ) {
      const cookieLang = getCookie('language');
      if(getCurrentLanguageSite() !== cookieLang){
        changeLanguage(cookieLang);
        console.log('alanguage changed to ' + cookieLang);
      }
    } else if( getCurrentLanguageSite() !== getDefaultLanguage() ){ // && !cookieExists('language')
      changeLanguage(getDefaultLanguage());
      console.log('blanguage changed to ' + getDefaultLanguage());
    }
    
    /* nav bar */
    
    const navButton = document.getElementById('navButton');

    if(getCurrentLanguageSite() === 'es'){
      navButton.textContent = 'Ocultar Barra';
    }else {
      navButton.textContent = 'Hide Nav Bar';
    }


    /* color theme */

    const prefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
    const themeButton = document.getElementById('themeButton');
    let theme;

    if (!cookieExists('theme')) {
      theme = prefersLight ? 'theme-light' : 'theme-dark';
    } else {
      theme = getCookie('theme');
    }

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
    console.log('current lang site = ' + getCurrentLanguageSite());
    console.log('current path = ' + getCurrentPath()); 
    console.log('lang cookie  = ' + getCookie('language') );
    console.log('theme cookie = ' + getCookie('theme'));

}main();
