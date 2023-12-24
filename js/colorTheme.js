function setTheme(theme) {
  localStorage.setItem('theme', theme);
  document.documentElement.className = theme;
}

function toggleTheme(button) {
  if (localStorage.getItem('theme') === 'theme-dark') {
    setTheme('theme-light');
    button.textContent = 'Dark';
  } else {
    setTheme('theme-dark');
    button.textContent = 'Light';
  }
}