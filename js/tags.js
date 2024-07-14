/**
 * @description Updates the URL based on the selected checkboxes and radio buttons.
 */
function updateURLfilters() {
  const checkboxes = document.querySelectorAll('#filter-checks input[type="checkbox"]:checked');
  const radios = document.querySelectorAll('#filter-checks input[type="radio"]:checked');

  const selectedTags = Array.from(checkboxes).map(checkbox => checkbox.value.toLowerCase());
  const selectedType = radios.length ? radios[0].value.toLowerCase() : 'all';

  const url = new URL(window.location);

  if (selectedTags.length > 0) {
    url.searchParams.set('tags', selectedTags.join(','));
  } else {
    url.searchParams.delete('tags');
  }

  if (selectedType !== 'all') {
    url.searchParams.set('type', selectedType);
  } else {
    url.searchParams.delete('type');
  }

  window.history.replaceState(null, '', url.toString());
}

/**
 * @description Sets filters based on the URL parameters and applies them on page load.
 */
function setFiltersFromURL() {
  const url = new URL(window.location);
  const tags = url.searchParams.get('tags');
  const type = url.searchParams.get('type');

  if (tags) {
    const selectedTags = tags.split(',');
    selectedTags.forEach(tag => {
      const checkbox = document.querySelector(`#filter-checks input[type="checkbox"][value="${tag}"]`);
      if (checkbox) {
        checkbox.checked = true;
      }
    });
  }

  if (type) {
    const radio = document.querySelector(`#filter-checks input[type="radio"][value="${type}"]`);
    if (radio) {
      radio.checked = true;
    }
  }

  filterCards();
}

/**
 * @description Filters cards based on the selected checkboxes and radios within the card with id "filter-checks".
 */
function filterCards() {
  const cards = document.querySelectorAll('.card:not(#filter-checks)');
  const radios = document.querySelectorAll('#filter-checks input[type="radio"]:checked');
  const checkboxes = document.querySelectorAll('#filter-checks input[type="checkbox"]:checked');

  const selectedTags = Array.from(checkboxes).map(checkbox => checkbox.value.toLowerCase());
  const selectedType = radios.length ? radios[0].value.toLowerCase() : 'all';

  cards.forEach(card => {
    const tagsInCard = card.getAttribute('data-tags').toLowerCase().split(' ');

    const matchesType = selectedType === 'all' || tagsInCard.includes(selectedType);
    const matchesTags = selectedTags.every(tag => tagsInCard.includes(tag));

    if (matchesType && (selectedTags.length === 0 || matchesTags)) {
      card.style.display = '';
    } else {
      card.style.display = 'none';
    }
  });

  updateURLfilters();
}

/**
 * @description Sets up event listeners and initializes filters based on the URL on page load.
 */
document.addEventListener('DOMContentLoaded', () => {
  setFiltersFromURL();
  // Add event listeners to checkboxes and radios
  const inputs = document.querySelectorAll('#filter-checks input');
  inputs.forEach(input => {
    input.addEventListener('change', filterCards);
  });
  filterCards();
});
