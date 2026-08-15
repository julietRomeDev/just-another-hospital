//BTN SERVICIOS
btnMSD = document.getElementById("btnMSD")
btnPO = document.getElementById("btnPO")
btnSMBurn = document.getElementById("btnSMBurn")
btnTRPBF = document.getElementById("btnTRPBF")
btnSMBurn = document.getElementById("btnSMBurn")


btnMSD.addEventListener("click", mostrarMensajeMedicinaSueno)
btnPO.addEventListener("click", mostrarMensajePostOperatorio)
btnSMBurn.addEventListener("click", mostrarMensajeBurnout)
btnTRPBF.addEventListener("click", mostrarMensajeTRPBF)

function mostrarMensajeTRPBF() {
	alert("TRPBF")
}

function mostrarMensajeBurnout() {
	alert("Burnout")
}

function mostrarMensajeMedicinaSueno() {
	alert("MedicinaSueno")
}

function mostrarMensajePostOperatorio() {
	alert("Post-Operatorio")
}
