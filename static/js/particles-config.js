particlesJS("particles-js", {
    particles: {
        number: { value: 50, density: { enable: true, value_area: 800 } },
        color: { value: ["#03dac6", "#ff0266", "#000000"] },
        shape: { type: "circle" },
        opacity: { value: 0.5, random: true },
        size: { value: 5, random: true },
        line_linked: { enable: true, color: "#ffffff", opacity: 0.4, width: 1 },
        move: { enable: true, speed: 3, direction: "none", random: false, straight: false, out_mode: "out", bounce: false }
    },
    interactivity: {
        detect_on: "canvas",
        events: {
            onhover: { enable: true, mode: "grab" },
            onclick: { enable: true, mode: "push" },
            resize: true
        },
        modes: {
            grab: { distance: 200, line_linked: { opacity: 1 } },
            push: { particles_nb: 4 }
        }
    },
    retina_detect: true
});
