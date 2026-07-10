/**
 * @description Credential filter module: type/topic filtering, text search, URL sync, counters, and reset.
 */

const CREDENTIAL_TYPES = ["education", "certification", "certificate", "badge", "award"];

// ---------------------------------------------------------------------------
// Pure helpers
// ---------------------------------------------------------------------------

/**
 * @description Returns the active filter state from the DOM.
 * @returns {{ selectedType: string, selectedTopics: string[], searchTerm: string }}
 */
function getActiveFilters() {
  const checkedRadio = document.querySelector("#filter-checks input[type=\"radio\"]:checked");
  const checkedBoxes = document.querySelectorAll("#filter-checks input[type=\"checkbox\"]:checked");
  const searchEl = document.getElementById("f-search");

  return {
    selectedType: checkedRadio ? checkedRadio.value.toLowerCase() : "all",
    selectedTopics: Array.from(checkedBoxes).map((cb) => cb.value.toLowerCase()),
    searchTerm: searchEl ? searchEl.value.trim().toLowerCase() : "",
  };
}

/**
 * @description Returns true if the card is a section header (no credential content).
 * @param {Element} card
 * @returns {boolean}
 */
function isHeaderCard(card) {
  return !card.querySelector(".credential-header") && Boolean(card.querySelector(".section-count"));
}

/**
 * @description Returns true if a card's data-tags match the given type and topics filters.
 * @param {string[]} cardTags  Lowercase tag tokens from data-tags attribute.
 * @param {string}   selectedType
 * @param {string[]} selectedTopics
 * @returns {boolean}
 */
function cardMatchesTypeAndTopics(cardTags, selectedType, selectedTopics) {
  const matchesType = selectedType === "all" || cardTags.includes(selectedType);
  const matchesTopics = selectedTopics.length === 0 || selectedTopics.some((t) => cardTags.includes(t));
  return matchesType && matchesTopics;
}

/**
 * @description Returns true if a credential card's visible text matches the search term.
 * @param {Element} card
 * @param {string}  searchTerm  Already lowercased and trimmed.
 * @returns {boolean}
 */
function cardMatchesSearch(card, searchTerm) {
  if (!searchTerm) return true;
  const title = card.querySelector(".title-main")?.textContent?.toLowerCase() ?? "";
  const issuer = card.querySelector(".credential-issuer")?.textContent?.toLowerCase() ?? "";
  const description = card.querySelector(".credential-description")?.textContent?.toLowerCase() ?? "";
  return title.includes(searchTerm) || issuer.includes(searchTerm) || description.includes(searchTerm);
}

// ---------------------------------------------------------------------------
// Counter helpers
// ---------------------------------------------------------------------------

/**
 * @description Accumulates per-type counts from an array of visible credential cards.
 * @param {Element[]} visibleCredentialCards  Cards that passed all filters (headers excluded).
 * @returns {Object.<string, number>}
 */
function buildTypeCounts(visibleCredentialCards) {
  const counts = Object.fromEntries(CREDENTIAL_TYPES.map((t) => [t, 0]));
  visibleCredentialCards.forEach((card) => {
    const cardTags = (card.getAttribute("data-tags") ?? "").toLowerCase().split(" ");
    const primaryType = cardTags.find((t) => Object.prototype.hasOwnProperty.call(counts, t));
    if (primaryType) counts[primaryType]++;
  });
  return counts;
}

/**
 * @description Pushes count values to all counter elements in the DOM.
 * @param {Object.<string, number>} counts
 * @param {number} total
 */
function updateCounterElements(counts, total) {
  document.querySelectorAll(".section-count").forEach((el) => {
    const type = el.getAttribute("data-type");
    el.textContent = `(${counts[type] ?? 0})`;
  });

  document.querySelectorAll(".stat-count[data-type]").forEach((el) => {
    const type = el.getAttribute("data-type");
    el.textContent = counts[type] ?? 0;
  });

  const totalEl = document.getElementById("global-total-credentials");
  if (totalEl) totalEl.textContent = total;
}

// ---------------------------------------------------------------------------
// URL sync
// ---------------------------------------------------------------------------

/**
 * @description Writes the current filter state to the URL query string (no page reload).
 */
function updateURLfilters() {
  const { selectedType, selectedTopics, searchTerm } = getActiveFilters();
  const url = new URL(window.location);

  if (selectedTopics.length > 0) {
    url.searchParams.set("tags", selectedTopics.join(","));
  } else {
    url.searchParams.delete("tags");
  }

  if (selectedType !== "all") {
    url.searchParams.set("type", selectedType);
  } else {
    url.searchParams.delete("type");
  }

  if (searchTerm) {
    url.searchParams.set("search", searchTerm);
  } else {
    url.searchParams.delete("search");
  }

  window.history.replaceState(null, "", url.toString());
}

/**
 * @description Reads URL params and ticks the matching checkboxes, radios, and search input.
 */
function setFiltersFromURL() {
  const url = new URL(window.location);
  const tags = url.searchParams.get("tags");
  const type = url.searchParams.get("type");
  const search = url.searchParams.get("search");

  if (tags) {
    tags.split(",").forEach((tag) => {
      const checkbox = document.querySelector(
        `#filter-checks input[type="checkbox"][value="${tag.toLowerCase()}"]`,
      );
      if (checkbox) checkbox.checked = true;
    });
  }

  if (type) {
    const radio = document.querySelector(`#filter-checks input[type="radio"][value="${type}"]`);
    if (radio) radio.checked = true;
  }

  const searchEl = document.getElementById("f-search");
  if (searchEl && search) searchEl.value = search;

  filterCards();
}

// ---------------------------------------------------------------------------
// Core filter
// ---------------------------------------------------------------------------

/**
 * @description Applies all active filters to credential cards and updates counters.
 */
function filterCards() {
  const { selectedType, selectedTopics, searchTerm } = getActiveFilters();
  const cards = document.querySelectorAll(".card:not(#filter-checks)");

  const visibleCredentialCards = [];

  cards.forEach((card) => {
    const tagsAttr = card.getAttribute("data-tags");
    if (!tagsAttr) return;

    const cardTags = tagsAttr.toLowerCase().split(" ");
    const header = isHeaderCard(card);

    const visible = cardMatchesTypeAndTopics(cardTags, selectedType, selectedTopics)
      && (header || cardMatchesSearch(card, searchTerm));

    card.style.display = visible ? "" : "none";

    if (visible && !header) {
      visibleCredentialCards.push(card);
    }
  });

  const counts = buildTypeCounts(visibleCredentialCards);
  updateCounterElements(counts, visibleCredentialCards.length);
  updateURLfilters();
}

// ---------------------------------------------------------------------------
// Reset
// ---------------------------------------------------------------------------

/**
 * @description Resets all filters to their default state and re-applies filtering.
 */
function resetFilters() {
  document.querySelectorAll("#filter-checks input[type=\"checkbox\"]").forEach((cb) => {
    cb.checked = false;
  });

  const allRadio = document.querySelector("#filter-checks input[type=\"radio\"][value=\"all\"]");
  if (allRadio) allRadio.checked = true;

  const searchEl = document.getElementById("f-search");
  if (searchEl) searchEl.value = "";

  filterCards();
}

// ---------------------------------------------------------------------------
// Init
// ---------------------------------------------------------------------------

/**
 * @description Wires up all event listeners and restores filter state from the URL.
 */
document.addEventListener("DOMContentLoaded", () => {
  // Attach listeners to all filter inputs (replaces inline onchange attributes)
  document.querySelectorAll("#filter-checks input").forEach((input) => {
    input.addEventListener("change", filterCards);
  });

  // Search input uses "input" event for live filtering
  const searchEl = document.getElementById("f-search");
  if (searchEl) searchEl.addEventListener("input", filterCards);

  // Reset button
  const resetBtn = document.getElementById("reset-btn");
  if (resetBtn) resetBtn.addEventListener("click", resetFilters);

  setFiltersFromURL();
});
