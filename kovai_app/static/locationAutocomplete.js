// locationAutocomplete.js

export function initLocationAutocomplete(inputId = "locationInput", suggestionsListId = "locationSuggestions") {
    const apiKey = "pk.14cf1b1494a70c76266ea1b070448402";
  
    const input = document.getElementById(inputId);
    const suggestionsList = document.getElementById(suggestionsListId);
  
    if (!input || !suggestionsList) {
      console.error("Input or suggestions container not found.");
      return;
    }
  
    input.addEventListener("keyup", async () => {
      const query = input.value.trim();
  
      if (query.length < 3) {
        suggestionsList.innerHTML = "";
        suggestionsList.parentElement.style.display = "none";
        return;
      }
  
      const url = `https://api.locationiq.com/v1/autocomplete?key=${apiKey}&q=${encodeURIComponent(query)}&countrycodes=IN&format=json&normalizecity=1`;
  
      try {
        const res = await fetch(url);
        const data = await res.json();
  
        suggestionsList.innerHTML = "";
  
        data.forEach(place => {
          const { address } = place;
          const district = address.county || address.state_district || "";
          const state = address.state || "";
          const country = address.country || "";
  
          if (!district || !state) return;
  
          const display = `${district}, ${state}, ${country}`;
          const li = document.createElement("li");
          li.textContent = display;
          li.addEventListener("click", () => {
            input.value = display;
            suggestionsList.innerHTML = "";
            suggestionsList.parentElement.style.display = "none";
          });
          suggestionsList.appendChild(li);
        });
  
        suggestionsList.parentElement.style.display = suggestionsList.children.length > 0 ? "block" : "none";
      } catch (err) {
        console.error("Location API error:", err);
      }
    });
  
    document.addEventListener("click", function (event) {
      if (!event.target.closest(`#${inputId}`) && !event.target.closest(`#${suggestionsListId}`)) {
        suggestionsList.innerHTML = "";
        suggestionsList.parentElement.style.display = "none";
      }
    });
  }
  