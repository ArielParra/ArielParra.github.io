/**
 * @description Portfolio filter: search bar with autocomplete technology suggestions.
 */

/** @type {string[]} Currently active tech filters */
let selectedTechs = [];

/**
 * @description Gets all available techs from the hidden data element.
 * @returns {Array<{value: string, en: string, es: string}>}
 */
function getAvailableTechs() {
  const el = document.getElementById('tech-data');
  if (!el) return [];
  try {
    return JSON.parse(el.getAttribute('data-techs') || '[]');
  } catch (e) {
    return [];
  }
}

/**
 * @description Returns the current site language.
 * @returns {string}
 */
function getPortfolioLang() {
  if (typeof getCurrentSiteLanguage === 'function') {
    return getCurrentSiteLanguage();
  }
  return document.documentElement.lang || 'en';
}

/**
 * @description Gets the display label for a tech in the current language.
 */
function getTechLabel(tech) {
  const lang = getPortfolioLang();
  return lang === 'es' ? tech.es : tech.en;
}

/**
 * @description Renders the suggestions dropdown based on current input.
 */
function showSuggestions(query) {
  const dropdown = document.getElementById('tech-suggestions');
  if (!dropdown) return;

  const allTechs = getAvailableTechs();
  const q = query.toLowerCase().trim();

  // Filter: match against value, en label, or es label; exclude already selected
  const matches = allTechs.filter(t =>
    !selectedTechs.includes(t.value) &&
    (q === '' ||
      t.value.includes(q) ||
      t.en.toLowerCase().includes(q) ||
      t.es.toLowerCase().includes(q))
  );

  if (matches.length === 0 || q === '') {
    dropdown.style.display = 'none';
    dropdown.innerHTML = '';
    return;
  }

  dropdown.innerHTML = matches.map(t =>
    `<div class="tech-suggestion" data-value="${t.value}">${getTechLabel(t)}</div>`
  ).join('');

  dropdown.style.display = 'block';

  // Attach click handlers
  dropdown.querySelectorAll('.tech-suggestion').forEach(el => {
    el.addEventListener('mousedown', (e) => {
      e.preventDefault(); // prevent input blur
      addTechFilter(el.getAttribute('data-value'));
    });
  });
}

/**
 * @description Adds a technology to the active filters.
 */
function addTechFilter(value) {
  if (selectedTechs.includes(value)) return;
  selectedTechs.push(value);

  const input = document.getElementById('tech-search');
  if (input) input.value = '';

  const dropdown = document.getElementById('tech-suggestions');
  if (dropdown) {
    dropdown.style.display = 'none';
    dropdown.innerHTML = '';
  }

  renderSelectedTechs();
  filterProjects();
}

/**
 * @description Removes a technology from the active filters.
 */
function removeTechFilter(value) {
  selectedTechs = selectedTechs.filter(t => t !== value);
  renderSelectedTechs();
  filterProjects();
}

/**
 * @description Renders the selected tech chips.
 */
function renderSelectedTechs() {
  const container = document.getElementById('selected-techs');
  if (!container) return;

  const allTechs = getAvailableTechs();

  container.innerHTML = selectedTechs.map(val => {
    const tech = allTechs.find(t => t.value === val);
    const label = tech ? getTechLabel(tech) : val;
    return `<span class="tech-chip" data-value="${val}">${label}<span class="tech-chip-remove" data-value="${val}">✕</span></span>`;
  }).join('');

  // Attach remove handlers
  container.querySelectorAll('.tech-chip-remove').forEach(el => {
    el.addEventListener('click', () => {
      removeTechFilter(el.getAttribute('data-value'));
    });
  });
}

/**
 * @description Updates the URL based on selected technologies.
 */
function updatePortfolioURL() {
  const url = new URL(window.location);

  if (selectedTechs.length > 0) {
    url.searchParams.set('techs', selectedTechs.join(','));
  } else {
    url.searchParams.delete('techs');
  }

  window.history.replaceState(null, '', url.toString());
}

/**
 * @description Restores filters from URL parameters on page load.
 */
function setPortfolioFiltersFromURL() {
  const url = new URL(window.location);
  const techs = url.searchParams.get('techs');

  if (techs) {
    selectedTechs = techs.split(',').filter(t => t.trim());
    renderSelectedTechs();
  }

  filterProjects();
}

/**
 * @description Filters project cards based on selected technologies.
 */
function filterProjects() {
  const cards = document.querySelectorAll('.card:not(#filter-techs)');

  let visibleCount = 0;

  cards.forEach(card => {
    const tagsAttr = card.getAttribute('data-tags');
    if (!tagsAttr) return;

    const tagsInCard = tagsAttr.split(' ').map(t => t.toLowerCase());

    if (selectedTechs.length === 0 || selectedTechs.some(tech => tagsInCard.includes(tech))) {
      card.style.display = '';
      visibleCount++;
    } else {
      card.style.display = 'none';
    }
  });

  const counterEl = document.getElementById('portfolio-count');
  if (counterEl) counterEl.textContent = visibleCount;

  updatePortfolioURL();
}

/**
 * @description Initialize portfolio search filter on page load.
 */
document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('tech-search');
  const dropdown = document.getElementById('tech-suggestions');

  if (input) {
    input.addEventListener('input', () => {
      showSuggestions(input.value);
    });

    input.addEventListener('focus', () => {
      if (input.value.trim()) {
        showSuggestions(input.value);
      }
    });

    input.addEventListener('blur', () => {
      // Small delay so click on suggestion fires first
      setTimeout(() => {
        if (dropdown) {
          dropdown.style.display = 'none';
        }
      }, 150);
    });

    // Keyboard navigation
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Backspace' && input.value === '' && selectedTechs.length > 0) {
        removeTechFilter(selectedTechs[selectedTechs.length - 1]);
      }
    });
  }

  setPortfolioFiltersFromURL();

  /**
   * @description Updates the search placeholder based on current language.
   */
  function updatePlaceholder() {
    if (!input) return;
    const lang = getPortfolioLang();
    const placeholder = lang === 'es'
      ? (input.getAttribute('data-placeholder-es') || 'Buscar tecnología...')
      : (input.getAttribute('data-placeholder-en') || 'Search technology...');
    input.placeholder = placeholder;
  }

  updatePlaceholder();

  // Re-render labels on language change
  window.addEventListener('languageChanged', () => {
    renderSelectedTechs();
    updatePlaceholder();
  });
});
