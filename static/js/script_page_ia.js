let canvas = document.getElementById("canvas");
let ctx = canvas.getContext("2d");
let drawing = false;
let autoSendInterval = null;

ctx.fillStyle = "rgba(255, 255, 255, 1)";
ctx.fillRect(0, 0, canvas.width, canvas.height); // Fond blanc juvbju

// Pour pc
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

// Pour mobile
canvas.addEventListener("touchstart", () => {
    event.preventDefault();
    lastX =  event.touches[0].clientX - canvas.getBoundingClientRect().left;
    lastY = event.touches[0].clientY - canvas.getBoundingClientRect().top; 
    drawing = true;
    sendDrawing();
    });
canvas.addEventListener("touchend", () => { 
    sendDrawing();
    drawing = false;});
canvas.addEventListener("touchmove", draw);

let lastX = 0;
let lastY = 0;

function draw(event) {
    if (!drawing) return;

    ctx.fillStyle = "black";  // Couleur des points
    const pointSize = 4;  // Taille des points

    // Calculer les différences entre les positions pour tracer plusieurs points
    if (event.touches) {
        dx = event.touches[0].clientX - canvas.getBoundingClientRect().left - lastX;
        dy = event.touches[0].clientY - canvas.getBoundingClientRect().top - lastY;
    } else {
        dx = event.offsetX - lastX;
        dy = event.offsetY - lastY;
    }
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
    if (event.touches) {
        lastX = event.touches[0].clientX - canvas.getBoundingClientRect().left;
        lastY = event.touches[0].clientY - canvas.getBoundingClientRect().top;
    } else {
        lastX = event.offsetX;
        lastY = event.offsetY;
    }
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
        
        document.getElementById("image").src = "data:image/png;base64," + data.images.enlarged; 
        document.getElementById("after_reshape").src = "data:image/png;base64," + data.images.after_reshape;
        document.getElementById("conv_1").src = "data:image/png;base64," + data.images.first_conv_pool;
        document.getElementById("conv_2").src = "data:image/png;base64," + data.images.second_conv_pool;
        document.getElementById("conv_3").src = "data:image/png;base64," + data.images.third_conv_pool;
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
