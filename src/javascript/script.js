function prendrePhoto(idPlante) {
  console.log(`Prendre une photo de la plante ${idPlante}`);
  // Ici, vous intégrerez la logique pour prendre une photo via votre caméra.
}
document.querySelectorAll(".toggle-graph").forEach((button) => {
  button.addEventListener("click", function () {
    const chartContainer = this.nextElementSibling; // Select the next sibling element, which is the chart container
    chartContainer.style.display =
      chartContainer.style.display === "none" ? "flex" : "none"; // Toggle display
  });
});
