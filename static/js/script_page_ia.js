let canvas = document.getElementById("canvas");
let ctx = canvas.getContext("2d");
let drawing = false;
let autoSendInterval = null;

ctx.fillStyle = "rgba(255, 255, 255, 1)";
ctx.fillRect(0, 0, canvas.width, canvas.height); // Fond blanc

canvas.addEventListener("mousedown", () => {
            lastX = event.offsetX;
            lastY = event.offsetY; 
            drawing = true;
            sendDrawing();
            });
canvas.addEventListener("mouseup", () => { 
            sendDrawing();
            drawing = false;});
canvas.addEventListener("mousemove", draw);

let lastX = 0;
let lastY = 0;

function draw(event) {
    if (!drawing) return;

    ctx.fillStyle = "black";  // Couleur des points
    const pointSize = 4;  // Taille des points

    // Si c'est le premier mouvement, on initialise les coordonnées
    if (lastX === 0 && lastY === 0) {
        lastX = event.offsetX;
        lastY = event.offsetY;
    }

    // Calculer les différences entre les positions pour tracer plusieurs points
    const dx = event.offsetX - lastX;
    const dy = event.offsetY - lastY;
    const distance = Math.sqrt(dx * dx + dy * dy);
    
    // Nombre de points à dessiner entre lastX, lastY et la position actuelle
    const pointsCount = Math.floor(distance); // Ajuster la valeur pour avoir plus ou moins de points

    // Dessiner plusieurs points pour créer un effet de trait
    for (let i = 0; i < pointsCount; i++) {
        const x = lastX + (dx * i) / pointsCount;
        const y = lastY + (dy * i) / pointsCount;

        ctx.beginPath();
        ctx.arc(x, y, pointSize, 0, Math.PI * 2);  // Dessiner un point
        ctx.fill();
    }

    // Mettre à jour les coordonnées pour le prochain mouvement
    lastX = event.offsetX;
    lastY = event.offsetY;
}

function clearCanvas() {
    ctx.fillStyle = "rgba(255, 255, 255, 1)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    document.getElementById("rep").textContent = "Prêt à deviner !";
    document.getElementById("image").src = "";
    document.getElementById("after_reshape").src = "";
    document.getElementById("conv_1").src = "";
    document.getElementById("conv_2").src = "";
    document.getElementById("conv_3").src = "";
    for (let i = 0; i < 10; i++) {
        document.getElementById("li_" + i).innerText = "Chiffre " + i + " : 0%";
    }
}

function sendDrawing() {
    let dataURL = canvas.toDataURL("image/png");

    fetch("/save_drawing", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: dataURL })
    })
    .then(response => response.json())
    .then(data => {
        // Remplacer le contenu de la div avec l'ID 'message' par le message du serveur
        document.getElementById("rep").textContent = "C'est un " + data.predict;

        for (let i = 0; i < data.predict_probas.length; i++) {
            text = "Chiffre " + i + " : " + Math.round(data.predict_probas[i] * 100 * 100)/100 + "%"; 
            document.getElementById("li_" + i).innerText = text;
        }
        time = new Date().getTime();
        document.getElementById("image").src = "../static/img/enlarged_chiffre_norm.png?timestamp=" + time; // timestamp pour l'actualisation automatique de l'image
        document.getElementById("after_reshape").src = "../static/img/after_reshape.png?timestamp=" + time;
        document.getElementById("conv_1").src = "../static/img/first_conv_pool.png?timestamp=" + time;
        document.getElementById("conv_2").src = "../static/img/second_conv_pool.png?timestamp=" + time;
        document.getElementById("conv_3").src = "../static/img/third_conv_pool.png?timestamp=" + time;
        if (drawing) {
            sendDrawing();
        }
    })
    .catch(error => console.error("Erreur:", error));
}

function showDetails() {
    document.getElementById('details').classList.remove('hidden');
    document.getElementById('flecheButton').classList.remove('hidden');
    document.getElementById('detailsButton').classList.add('hidden');
}

function hideDetails() {
    document.getElementById('details').classList.add('hidden');
    document.getElementById('flecheButton').classList.add('hidden');
    document.getElementById('detailsButton').classList.remove('hidden');
}
