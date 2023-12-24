function setTheme(selectedTheme) {
  localStorage.setItem('theme', selectedTheme);
  document.documentElement.className = selectedTheme;
}

function toggleTheme(button) {
  let newTheme;
  if (localStorage.getItem('theme') === 'theme-dark') {
    newTheme = 'theme-light';
    button.textContent = ' 🌙 ';
  } else {
    newTheme = 'theme-dark';
    button.textContent = ' ☀️ ';
  }
  setTheme(newTheme);
  setCookie('theme', newTheme, 30);
}