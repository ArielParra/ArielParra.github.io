/**
 * @description Credential card functionality: expand/collapse descriptions and skills truncation.
 */

/**
 * @description Toggles the credential description between truncated and full view.
 */
function toggleCredentialDescription(element) {
  const container = element.closest('.credential-description');
  const isExpanded = container.classList.contains('expanded');
  const textSpan = container.querySelector('span.i18n');
  const lang = getCurrentSiteLanguage();

  if (isExpanded) {
    container.classList.remove('expanded');
    element.textContent = '... ' + (lang === 'es' ? 'Ver más' : 'See more');
    truncateDescriptions();
  } else {
    container.classList.add('expanded');
    element.textContent = lang === 'es' ? 'Ver menos' : 'See less';
    if (textSpan) {
      const fullText = container.getAttribute('data-full-text');
      if (fullText) textSpan.textContent = fullText;
    }
  }
}

/**
 * @description Truncates skills tags to show only first 3.
 */
function truncateSkills() {
  const skillContainers = document.querySelectorAll('.credential-skills');

  skillContainers.forEach(container => {
    const skills = container.querySelectorAll('.credential-skill');
    const extraCount = skills.length - 3;
    const moreIndicator = container.querySelector('.skills-more');

    if (moreIndicator) {
      if (extraCount > 0) {
        const lang = getCurrentSiteLanguage();
        const label = lang === 'es'
          ? (moreIndicator.getAttribute('data-i18n-more-es') || `+${extraCount} más`)
          : (moreIndicator.getAttribute('data-i18n-more-en') || `+${extraCount} more`);
        moreIndicator.textContent = label;
        moreIndicator.style.display = '';

        skills.forEach((skill, index) => {
          if (index >= 3) skill.style.display = 'none';
        });
      } else {
        moreIndicator.style.display = 'none';
      }
    }
  });
}

/**
 * @description Truncates description to 2 lines (approx 85 chars) with ellipsis and makes see-more clickable.
 */
function truncateDescriptions() {
  const descriptions = document.querySelectorAll('.credential-description.justify');
  const MAX_CHARS = 84;

  descriptions.forEach(container => {
    const textSpan = container.querySelector('span.i18n');
    const seeMoreLink = container.querySelector('.see-more');
    if (!textSpan || !seeMoreLink) return;

    const lang = getCurrentSiteLanguage();
    const fullText = textSpan.getAttribute('data-i18n-' + lang) || textSpan.textContent;
    const seeMoreText = lang === 'es' ? 'Ver más' : 'See more';

    container.setAttribute('data-full-text', fullText);

    if (fullText.length > MAX_CHARS) {
      let truncated = fullText.substring(0, MAX_CHARS);
      while (truncated.length > 0 && !truncated.match(/\s$/)) {
        truncated = truncated.slice(0, -1);
      }
      truncated = truncated.trim();

      textSpan.textContent = truncated;
      seeMoreLink.textContent = '... ' + seeMoreText;
      seeMoreLink.style.display = 'inline';
    } else {
      seeMoreLink.style.display = 'none';
    }
  });
}

/**
 * @description Expands hidden skills.
 */
function expandSkills(element) {
  const container = element.closest('.credential-skills');
  const skills = container.querySelectorAll('.credential-skill');
  skills.forEach(skill => skill.style.display = '');
  element.style.display = 'none';
}

/**
 * @description Reset truncate state on language change.
 */
function resetDescriptions() {
  const descriptions = document.querySelectorAll('.credential-description.justify');
  descriptions.forEach(container => {
    const textSpan = container.querySelector('span.i18n');
    const seeMoreLink = container.querySelector('.see-more');
    const fullText = container.getAttribute('data-full-text');
    if (textSpan && fullText) {
      textSpan.textContent = fullText;
    }
    container.classList.remove('expanded');
    if (seeMoreLink) {
      seeMoreLink.textContent = '';
      seeMoreLink.style.display = 'none';
    }
  });
  truncateDescriptions();
}

/**
 * @description Initialize credential cards on page load.
 */
function initCredentials() {
  truncateSkills();
  truncateDescriptions();

  const seeMoreLinks = document.querySelectorAll('.see-more');
  seeMoreLinks.forEach(link => {
    link.addEventListener('click', () => toggleCredentialDescription(link));
  });

  const moreIndicators = document.querySelectorAll('.skills-more');
  moreIndicators.forEach(indicator => {
    indicator.addEventListener('click', () => expandSkills(indicator));
    indicator.style.cursor = 'pointer';
  });

  window.addEventListener('languageChanged', () => resetDescriptions());
}

document.addEventListener('DOMContentLoaded', initCredentials);