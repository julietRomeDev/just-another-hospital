btnHDD = document.getElementById("btnHDD")
btnSM = document.getElementById("btnSM")
btnMN = document.getElementById("btnMN")

btnSM.addEventListener("click", mostrarMensajeSaludMental)
btnHDD.addEventListener("click", mostrarMensajeHospitalDD)
btnMN.addEventListener("click", mostrarMensajeMNuclear)

function mostrarMensajeSaludMental() {
	alert("Salud Mental");
}

function mostrarMensajeHospitalDD() {
	alert("Hospital de Dia");
}

function mostrarMensajeMNuclear() {
	alert("Medicina Nuclear");
}
