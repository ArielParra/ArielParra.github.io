/**
 * @description Filters cards based on selected checkboxes and radios within the card with id "filter-checks".
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
}

filterCards();
