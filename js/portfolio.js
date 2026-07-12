/**
 * @description Portfolio filter: search bar with autocomplete technology suggestions.
 */

// ==========================================
// STATE MODULE (Deep Core)
// ==========================================
const filterState = {
  selectedTechs: [],
  listeners: [],

  subscribe(listener) {
    this.listeners.push(listener);
  },

  notify() {
    this.listeners.forEach((listener) => listener(this.selectedTechs));
  },

  addTech(value) {
    if (this.selectedTechs.includes(value)) return;
    this.selectedTechs.push(value);
    this.notify();
  },

  removeTech(value) {
    this.selectedTechs = this.selectedTechs.filter((t) => t !== value);
    this.notify();
  },

  setTechs(techs) {
    this.selectedTechs = techs;
    this.notify();
  },

  get() {
    return this.selectedTechs;
  },
};

// ==========================================
// RENDERER ADAPTER (DOM Boundary)
// ==========================================
class DOMRenderer {
  static getAvailableTechs() {
    const el = document.getElementById("tech-data");
    if (!el) return [];
    try {
      return JSON.parse(el.getAttribute("data-techs") || "[]");
    } catch (e) {
      return [];
    }
  }

  static getTechLabel(tech) {
    const lang = typeof getCurrentSiteLanguage === "function" ? getCurrentSiteLanguage() : (document.documentElement.lang || "en");
    if (lang === "es") return tech.es || tech.en;
    if (lang === "fr") return tech.fr || tech.en;
    if (lang === "pt") return tech.pt || tech.en;
    return tech.en;
  }

  static updateURL(selectedTechs) {
    const url = new URL(window.location);
    if (selectedTechs.length > 0) {
      url.searchParams.set("techs", selectedTechs.join(","));
    } else {
      url.searchParams.delete("techs");
    }
    window.history.replaceState(null, "", url.toString());
  }

  static renderSelectedTechs(selectedTechs) {
    const container = document.getElementById("selected-techs");
    if (!container) return;
    const allTechs = DOMRenderer.getAvailableTechs();

    container.innerHTML = selectedTechs.map((val) => {
      const tech = allTechs.find((t) => t.value === val);
      const label = tech ? DOMRenderer.getTechLabel(tech) : val;
      return `<span class="tech-chip" data-value="${val}">${label}<span class="tech-chip-remove" data-value="${val}">✕</span></span>`;
    }).join("");

    container.querySelectorAll(".tech-chip-remove").forEach((el) => {
      el.addEventListener("click", () => filterState.removeTech(el.getAttribute("data-value")));
    });
  }

  static filterProjects(selectedTechs) {
    const cards = document.querySelectorAll(".card:not(#filter-techs)");
    let visibleCount = 0;

    cards.forEach((card) => {
      const tagsAttr = card.getAttribute("data-tags");
      if (!tagsAttr) return;
      const tagsInCard = tagsAttr.split(" ").map((t) => t.toLowerCase());

      if (selectedTechs.length === 0 || selectedTechs.some((tech) => tagsInCard.includes(tech))) {
        card.style.display = "";
        visibleCount++;
      } else {
        card.style.display = "none";
      }
    });

    const counterEl = document.getElementById("portfolio-count");
    if (counterEl) counterEl.textContent = visibleCount;
  }

  static onStateChange(selectedTechs) {
    const input = document.getElementById("tech-search");
    if (input) input.value = "";

    const dropdown = document.getElementById("tech-suggestions");
    if (dropdown) {
      dropdown.style.display = "none";
      dropdown.innerHTML = "";
    }

    DOMRenderer.renderSelectedTechs(selectedTechs);
    DOMRenderer.filterProjects(selectedTechs);
    DOMRenderer.updateURL(selectedTechs);
  }
}

// Subscribe the DOM adapter to the state module
filterState.subscribe(DOMRenderer.onStateChange);

/**
 * @description Renders the suggestions dropdown based on current input.
 */
function showSuggestions(query) {
  const dropdown = document.getElementById("tech-suggestions");
  if (!dropdown) return;

  const allTechs = DOMRenderer.getAvailableTechs();
  const q = query.toLowerCase().trim();
  const selectedTechs = filterState.get();

  const matches = allTechs.filter((t) => !selectedTechs.includes(t.value)
    && (q === "" || t.value.includes(q) || t.en.toLowerCase().includes(q) || t.es.toLowerCase().includes(q)));

  if (matches.length === 0 || q === "") {
    dropdown.style.display = "none";
    dropdown.innerHTML = "";
    return;
  }

  dropdown.innerHTML = matches.map((t) => `<div class="tech-suggestion" data-value="${t.value}">${DOMRenderer.getTechLabel(t)}</div>`).join("");
  dropdown.style.display = "block";

  dropdown.querySelectorAll(".tech-suggestion").forEach((el) => {
    el.addEventListener("mousedown", (e) => {
      e.preventDefault();
      filterState.addTech(el.getAttribute("data-value"));
    });
  });
}

function setPortfolioFiltersFromURL() {
  const url = new URL(window.location);
  const techs = url.searchParams.get("techs");
  if (techs) {
    filterState.setTechs(techs.split(",").filter((t) => t.trim()));
  } else {
    // Initial render even if empty
    DOMRenderer.onStateChange([]);
  }
}

function getPortfolioLang() {
  if (typeof getCurrentSiteLanguage === "function") {
    return getCurrentSiteLanguage();
  }
  return document.documentElement.lang || "en";
}

document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("tech-search");
  const dropdown = document.getElementById("tech-suggestions");

  if (input) {
    input.addEventListener("input", () => showSuggestions(input.value));
    input.addEventListener("focus", () => {
      if (input.value.trim()) showSuggestions(input.value);
    });
    input.addEventListener("blur", () => {
      setTimeout(() => {
        if (dropdown) dropdown.style.display = "none";
      }, 150);
    });
    input.addEventListener("keydown", (e) => {
      const selectedTechs = filterState.get();
      if (e.key === "Backspace" && input.value === "" && selectedTechs.length > 0) {
        filterState.removeTech(selectedTechs[selectedTechs.length - 1]);
      }
    });
  }

  setPortfolioFiltersFromURL();

  function updatePlaceholder() {
    if (!input) return;
    const lang = getPortfolioLang();
    const placeholders = {
      en: input.getAttribute("data-placeholder-en") || "Search technology...",
      es: input.getAttribute("data-placeholder-es") || "Buscar tecnología...",
      fr: input.getAttribute("data-placeholder-fr") || "Rechercher une technologie...",
      pt: input.getAttribute("data-placeholder-pt") || "Pesquisar tecnologia...",
    };
    input.placeholder = placeholders[lang] || placeholders.en;
  }

  updatePlaceholder();
  truncateProjectDescriptions();
  truncateTechs();

  const seeMoreLinks = document.querySelectorAll(".project-description .see-more");
  seeMoreLinks.forEach((link) => link.addEventListener("click", () => toggleProjectDescription(link)));

  const moreIndicators = document.querySelectorAll(".techs-more");
  moreIndicators.forEach((indicator) => {
    indicator.addEventListener("click", () => expandTechs(indicator));
    indicator.style.cursor = "pointer";
  });

  window.addEventListener("languageChanged", () => {
    DOMRenderer.renderSelectedTechs(filterState.get());
    updatePlaceholder();
    resetProjectDescriptions();
    truncateTechs();
  });
});

function toggleProjectDescription(element) {
  const container = element.closest(".project-description");
  const isExpanded = container.classList.contains("expanded");
  const textSpan = container.querySelector("span.desc-text");
  const lang = getPortfolioLang();

  const TEXT_SEE_MORE = {
    en: "See more",
    es: "Ver más",
    fr: "Voir plus",
    pt: "Ver mais",
  };
  const TEXT_SEE_LESS = {
    en: "See less",
    es: "Ver menos",
    fr: "Voir moins",
    pt: "Ver menos",
  };

  if (isExpanded) {
    container.classList.remove("expanded");
    element.textContent = `... ${TEXT_SEE_MORE[lang] || TEXT_SEE_MORE.en}`;
    truncateProjectDescriptions();
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

function truncateProjectDescriptions() {
  const descriptions = document.querySelectorAll(".project-description.justify");
  const MAX_CHARS = 82;

  descriptions.forEach((container) => {
    if (container.classList.contains("expanded")) return;

    const textSpan = container.querySelector("span.desc-text");
    const seeMoreLink = container.querySelector(".see-more");
    if (!textSpan || !seeMoreLink) return;

    const lang = getPortfolioLang();
    let fullText = container.getAttribute("data-full-text");
    if (!fullText) {
      fullText = textSpan.textContent;
      container.setAttribute("data-full-text", fullText);
    }

    const TEXT_SEE_MORE = {
      en: "See more",
      es: "Ver más",
      fr: "Voir plus",
      pt: "Ver mais",
    };

    if (fullText.length > MAX_CHARS) {
      let truncated = fullText.substring(0, MAX_CHARS);
      while (truncated.length > 0 && !truncated.match(/\s$/)) {
        truncated = truncated.slice(0, -1);
      }
      textSpan.innerHTML = truncated.trim();
      seeMoreLink.textContent = `... ${TEXT_SEE_MORE[lang] || TEXT_SEE_MORE.en}`;
      seeMoreLink.style.display = "inline";
    } else {
      seeMoreLink.style.display = "none";
    }
  });
}

function resetProjectDescriptions() {
  const descriptions = document.querySelectorAll(".project-description.justify");
  descriptions.forEach((container) => {
    const textSpan = container.querySelector("span.desc-text");
    const seeMoreLink = container.querySelector(".see-more");
    const fullText = container.getAttribute("data-full-text");
    if (textSpan && fullText) textSpan.innerHTML = fullText;
    container.classList.remove("expanded");
    if (seeMoreLink) {
      seeMoreLink.textContent = "";
      seeMoreLink.style.display = "none";
    }
  });
  truncateProjectDescriptions();
}

function truncateTechs() {
  const techContainers = document.querySelectorAll(".project-techs");
  const MAX_CHARS_PER_LINE = 30;

  techContainers.forEach((container) => {
    const techs = container.querySelectorAll(".project-tech");
    const moreIndicator = container.querySelector(".techs-more");

    if (!moreIndicator || techs.length <= 1) {
      if (moreIndicator) moreIndicator.style.display = "none";
      return;
    }

    let currentLength = 0;
    let techsToShow = 0;

    techs.forEach((tech, index) => {
      const techLength = tech.textContent.length + 2;
      if (index === 0 || currentLength + techLength <= MAX_CHARS_PER_LINE) {
        techsToShow = index + 1;
        currentLength += techLength;
        tech.style.display = "";
      } else {
        tech.style.display = "none";
      }
    });

    const extraCount = techs.length - techsToShow;
    if (extraCount > 0 && moreIndicator) {
      const lang = getPortfolioLang();
      moreIndicator.textContent = lang === "es" ? `+${extraCount} más` : `+${extraCount} more`;
      moreIndicator.style.display = "";
    } else if (moreIndicator) {
      moreIndicator.style.display = "none";
    }
  });
}

function expandTechs(element) {
  const container = element.closest(".project-techs");
  container.querySelectorAll(".project-tech").forEach((tech) => { tech.style.display = ""; });
  element.style.display = "none";
}
