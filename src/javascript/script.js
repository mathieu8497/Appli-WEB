document.addEventListener("DOMContentLoaded", function () {
  // Simulons l'obtention des données des plantes
  const plantes = [
    {
      id: 1,
      nom: "Rose",
      temperature: "20°C",
      brightness: "450 lux",
      humidity: "60%",
    },
    {
      id: 2,
      nom: "Tulip",
      temperature: "18°C",
      brightness: "400 lux",
      humidity: "70%",
    },
  ];

  // Affichage des plantes
  const containerPlantes = document.getElementById("plantes");
  plantes.forEach((plante) => {
    const div = document.createElement("div");
    div.className = "plante";
    div.innerHTML = `
            <h2>${plante.nom}</h2>
            <p>Temperature: ${plante.temperature}</p>
            <p>Brightness: ${plante.brightness}</p>
            <p>Humidity: ${plante.humidity}</p>
            <button class="bouton" onclick="prendrePhoto(${plante.id})">Take Pictures</button>
        `;
    containerPlantes.appendChild(div);
  });
});

function prendrePhoto(idPlante) {
  console.log(`Prendre une photo de la plante ${idPlante}`);
  // Ici, vous intégrerez la logique pour prendre une photo via votre caméra.
}
