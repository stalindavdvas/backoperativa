function resolver() {
    let oferta = document.getElementById("oferta").value.split(",").map(Number);
    let demanda = document.getElementById("demanda").value.split(",").map(Number);
    let costos = JSON.parse(document.getElementById("costos").value);

    fetch("http://127.0.0.1:5000/esquina_noroeste", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ oferta, demanda, costos })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("resultado").innerText = JSON.stringify(data.solucion, null, 2);
    })
    .catch(error => console.error("Error:", error));
}
