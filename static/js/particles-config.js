particlesJS("particles-js", {
    particles: {
        number: { value: 80, density: { enable: true, value_area: 800 } },
        color: { value: ["#1e3a8a", "#3b82f6", "#94a3b8"] }, // Couleurs des particules : bleu foncé, bleu clair, gris bleuté
        shape: { type: "circle" },
        opacity: { value: 0.5, random: true },
        size: { value: 5, random: true },
        line_linked: { 
            enable: true, 
            distance: 150, // Distance de connexion des particules
            color: { value: ["#1e3a8a", "#3b82f6", "#94a3b8"] }, // Couleur des lignes de connexion, bleu très sombre
            opacity: 0.4, 
            width: 1 
        },
        move: { 
            enable: true, 
            speed: 1, // Vitesse modérée pour observer les connexions
            random: false, 
            out_mode: "out" 
        }
    },
    interactivity: {
        detect_on: "canvas",
        events: {
            onhover: { enable: true, mode: "grab" }
        },
        modes: {
            grab: { distance: 100, line_linked: { opacity: 1 } }
        }
    },
    retina_detect: true
});
