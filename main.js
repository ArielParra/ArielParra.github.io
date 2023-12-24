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

function main() {

  loadAllScripts().then(() => {  

    /*dynamic icon*/

    if (navigator.userAgent.toLowerCase().indexOf('firefox') === -1) {
      //for all the other chromium based browsers that doesnt support dynamic favicons
      setInterval(animateIcon, 800);
    }

    /*color theme*/

    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: light)').matches;
    if (prefersDarkScheme) {
      setTheme('theme-light');
      document.getElementById('themeButton').textContent = 'Dark';
    } else {
      setTheme('theme-dark');
      document.getElementById('themeButton').textContent = 'Light';
    }

    /*language*/

    detectLanguage();
    console.log('default lang = ' + defaultLanguage);
    console.log('lang cookie  = ' + getCookie('language') );
    console.log('current path = ' + currentPath);
  });

}main();