const rutasSimuladas = {
    auto: {
        tiempo: "12 min",
        distancia: "4.5 km",
        instrucciones: "Tomar la autopista X en dirección norte, salir en bajada principal."
    },

    colectivo: {
        tiempo: "22 min",
        distancia: "Línea 10001 / 01010110",
        instrucciones: "Descender en la estación Y y caminar 6 cuadras en dirección norte."
    },

    tren: {
        tiempo: "25 min",
        distancia: "Línea Einstein",
        instrucciones: "Descender en la estación cabecera de la zona y caminar 5 cuadras en dirección norte."
    }
};

const botonesModo = document.querySelectorAll(".grupo-transporte button");

const spanTiempo = document.getElementById("info-tiempo");
const spanDistancia = document.getElementById("info-distancia");
const pInstruccion = document.getElementById("info-instruccion");

botonesModo.forEach(boton => {
    boton.addEventListener("click", function () {

        botonesModo.forEach(b => b.classList.remove("active"));

        this.classList.add("active");

        const modo = this.getAttribute("data-mode");

        const data = rutasSimuladas[modo];

        spanTiempo.innerText = data.tiempo;
        spanDistancia.innerText = data.distancia;
        pInstruccion.innerText = data.instrucciones;
    });
});