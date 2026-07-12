/**
 * @description Credential card functionality: expand/collapse descriptions and skills truncation.
 */

/**
 * @description Toggles the credential description between truncated and full view.
 */
function toggleCredentialDescription(element) {
  const container = element.closest(".credential-description");
  const isExpanded = container.classList.contains("expanded");
  const textSpan = container.querySelector("span.desc-text");
  const lang = getCurrentSiteLanguage();

  const TEXT_SEE_MORE = {
    en: "See more", es: "Ver más", fr: "Voir plus", pt: "Ver mais",
  };
  const TEXT_SEE_LESS = {
    en: "See less", es: "Ver menos", fr: "Voir moins", pt: "Ver menos",
  };

  if (isExpanded) {
    container.classList.remove("expanded");
    element.textContent = `... ${TEXT_SEE_MORE[lang] || TEXT_SEE_MORE.en}`;
    truncateDescriptions();
  } else {
    container.classList.add("expanded");
    element.textContent = TEXT_SEE_LESS[lang] || TEXT_SEE_LESS.en;
    if (textSpan) {
      let fullText = container.getAttribute("data-full-text");
      if (!fullText) {
        fullText = textSpan.textContent;
        container.setAttribute("data-full-text", fullText);
      }
      textSpan.innerHTML = fullText;
    }
  }
}

/**
 * @description Truncates skills based on character width (~45 chars per line).
 */
function truncateSkills() {
  const skillContainers = document.querySelectorAll(".credential-skills");
  const MAX_CHARS_PER_LINE = 30;

  // Helper to clean i18n tags from text
  const cleanText = (text) => text.replace(/\(\(en\)\)/g, "").replace(/\(\(\/en\)\)/g, "")
    .replace(/\(\(es\)\)/g, "").replace(/\(\(\/es\)\)/g, "");

  skillContainers.forEach((container) => {
    const skills = container.querySelectorAll(".credential-skill");
    const moreIndicator = container.querySelector(".skills-more");

    if (!moreIndicator || skills.length <= 1) {
      if (moreIndicator) moreIndicator.style.display = "none";
      return;
    }

    let currentLength = 0;
    let skillsToShow = 0;

    skills.forEach((skill, index) => {
      const skillText = cleanText(skill.textContent);
      const skillLength = skillText.length + 2;

      if (index === 0 || currentLength + skillLength <= MAX_CHARS_PER_LINE) {
        skillsToShow = index + 1;
        currentLength += skillLength;
        skill.style.display = "";
      } else {
        skill.style.display = "none";
      }
    });

    const extraCount = skills.length - skillsToShow;
    if (extraCount > 0 && moreIndicator) {
      const lang = getCurrentSiteLanguage();
      const label = lang === "es"
        ? (moreIndicator.getAttribute("data-i18n-more-es") || `+${extraCount} más`)
        : (moreIndicator.getAttribute("data-i18n-more-en") || `+${extraCount} more`);
      moreIndicator.textContent = label;
      moreIndicator.style.display = "";
    } else if (moreIndicator) {
      moreIndicator.style.display = "none";
    }
  });
}

/**
 * @description Truncates description to 2 lines (approx 85 chars) with ellipsis and makes see-more clickable.
 */
function truncateDescriptions() {
  const descriptions = document.querySelectorAll(".credential-description.justify");
  const MAX_CHARS = 84;

  descriptions.forEach((container) => {
    const textSpan = container.querySelector("span.desc-text");
    const seeMoreLink = container.querySelector(".see-more");
    if (!textSpan || !seeMoreLink) return;

    const lang = getCurrentSiteLanguage();
    let fullText = container.getAttribute("data-full-text");
    if (!fullText) {
      fullText = textSpan.textContent;
      container.setAttribute("data-full-text", fullText);
    }

    const TEXT_SEE_MORE = {
      en: "See more", es: "Ver más", fr: "Voir plus", pt: "Ver mais",
    };

    if (fullText.length > MAX_CHARS) {
      let truncated = fullText.substring(0, MAX_CHARS);
      while (truncated.length > 0 && !truncated.match(/\s$/)) {
        truncated = truncated.slice(0, -1);
      }
      truncated = truncated.trim();

      textSpan.innerHTML = truncated;
      seeMoreLink.textContent = `... ${TEXT_SEE_MORE[lang] || TEXT_SEE_MORE.en}`;
      seeMoreLink.style.display = "inline";
    } else {
      seeMoreLink.style.display = "none";
    }
  });
}

/**
 * @description Expands hidden skills.
 */
function expandSkills(element) {
  const container = element.closest(".credential-skills");
  const skills = container.querySelectorAll(".credential-skill");
  skills.forEach((skill) => { skill.style.display = ""; });
  element.style.display = "none";
}

/**
 * @description Reset truncate state on language change.
 */
function resetDescriptions() {
  const descriptions = document.querySelectorAll(".credential-description.justify");
  descriptions.forEach((container) => {
    const textSpan = container.querySelector("span.desc-text");
    const seeMoreLink = container.querySelector(".see-more");
    const fullText = container.getAttribute("data-full-text");
    if (textSpan && fullText) {
      textSpan.innerHTML = fullText;
    }
    container.classList.remove("expanded");
    if (seeMoreLink) {
      seeMoreLink.textContent = "";
      seeMoreLink.style.display = "none";
    }
  });
  truncateDescriptions();
  truncateSkills();
}

/**
 * @description Initialize credential cards on page load.
 */
function initCredentials() {
  truncateSkills();
  truncateDescriptions();

  const seeMoreLinks = document.querySelectorAll(".see-more");
  seeMoreLinks.forEach((link) => {
    link.addEventListener("click", () => toggleCredentialDescription(link));
  });

  const moreIndicators = document.querySelectorAll(".skills-more");
  moreIndicators.forEach((indicator) => {
    indicator.addEventListener("click", () => expandSkills(indicator));
    indicator.style.cursor = "pointer";
  });

  window.addEventListener("languageChanged", () => resetDescriptions());
}

document.addEventListener("DOMContentLoaded", initCredentials);
