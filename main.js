/*main driver code*/
function main(){
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

}main();
