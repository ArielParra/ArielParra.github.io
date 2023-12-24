async function loadScript(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = src;
    script.defer = false;
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
}
async function loadAllScripts() {
  await loadScript('./js/cookies.js');
  await loadScript('./js/language.js');
  await loadScript('./js/colorTheme.js');
  await loadScript('./js/navButton.js');
  await loadScript('./js/dynFavicon.js');
}

/*function that sets the buttons, cookies, etc.
  called once everytime the website loads */
function main() {

  loadAllScripts().then(() => {  

    /* language */
    const defaultLanguage = navigator.language.substring(0, 2);
    let currentLanguageSite;

    if ( currentPath.endsWith('/es/') || currentPath.endsWith('/es/index.html') ) {
      currentLanguage = 'es';
      currentLanguageSite = 'es';
    }else{
      currentLanguage = 'en';
      currentLanguageSite = 'en';
    }

    if ( cookieExists('language') ) {
      currentLanguage = getCookie('language');
      changeLanguage(currentLanguage);
    } else {
      if( (currentLanguage !== defaultLanguage) ||
          (currentLanguage !== currentLanguageSite) ){ // && !cookieExists('language')
          changeLanguage(currentLanguage);
      } 
    }
    
    /* nav bar */
    const navButton = document.getElementById('navButton');
    if(currentLanguage === 'es'){
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
    console.log('default lang = ' + defaultLanguage);
    console.log('current lang = ' + currentLanguage);
    console.log('current lang site = ' + currentLanguageSite);
    console.log('current path = ' + currentPath); 
    console.log('lang cookie  = ' + getCookie('language') );
    console.log('theme cookie = ' + getCookie('theme'));

  });

}main();