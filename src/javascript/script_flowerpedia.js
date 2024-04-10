document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("searchInput");
  const filters = document.querySelectorAll("#searchForm select");
  const container = document.querySelector(".pro_container");
  const searchButton = document.getElementById("searchButton");
  const possessedCheckbox = document.getElementById("possessed");
  possessedCheckbox.addEventListener("change", fetchFilteredData);

  function fetchFilteredData() {
    let queryString = "?search=" + encodeURIComponent(searchInput.value);

    filters.forEach((filter) => {
      if (filter.value) {
        queryString += `&${filter.name}=` + encodeURIComponent(filter.value);
      }
    });

    // Include the checkbox state in the query string
    if (possessedCheckbox.checked) {
      queryString += `&possessed=on`;
    }

    fetch(queryString, {
      headers: { "X-Requested-With": "XMLHttpRequest" },
    })
      .then((response) => response.json())
      .then((data) => {
        container.innerHTML = "";

        data.forEach((flower) => {
          const imageFilename = flower.common_name
            .replace(/[ '.,()&]/g, "_")
            .replace(/__+/g, "_")
            .toLowerCase();
          const imagePath = `../images/${imageFilename}.jpg`;

          const flowerHTML = `
                <div class="box_products" style="background-image: url('${imagePath}'); background-size: cover; background-position: center;">
                    <div class="visible_info">
                        <h5>${flower.common_name}</h5>
                    </div>
                    <div class="hidden_info des">
                        - Famille: <span>${flower.family}</span><br>
                        - Type: <span>${flower.plant_type}</span><br>
                        - Période de floraison: <span>${flower.blooming_period}</span><br>
                        - Couleurs: <span>${flower.colors}</span><br>
                        - Pollinisateurs: <span>${flower.pollinators}</span>
                    </div>
                </div>`;
          container.insertAdjacentHTML("beforeend", flowerHTML);
        });
      })
      .catch((error) => console.error("Error:", error));
  }

  searchInput.addEventListener("input", fetchFilteredData);
  filters.forEach((filter) =>
    filter.addEventListener("change", fetchFilteredData)
  );

  fetchFilteredData();
});
function Back_to_topFct() {
  const goToTopBtn = document.getElementById("back_top");
  // Lorsque l'utilisateur fait défiler vers le bas 20 pixels à partir du haut du document, affichez le bouton
  window.onscroll = function () {
    if (
      document.body.scrollTop > 20 ||
      document.documentElement.scrollTop > 20
    ) {
      goToTopBtn.style.display = "block";
    } else {
      goToTopBtn.style.display = "none";
    }
  };
  // When the user clicks on the button, scroll to the top of the document
  goToTopBtn.addEventListener("click", () => {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
  });
}
Back_to_topFct();
