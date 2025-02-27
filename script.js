function submitData() {
    let attempts = document.getElementById("attempts").value;

    fetch("http://127.0.0.1:5000/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ attempts })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        updateStatus();
    })
    .catch(error => console.error("Помилка:", error));
}

function updateStatus() {
    fetch("http://127.0.0.1:5000/status")
    .then(response => response.json())
    .then(data => {
        document.getElementById("streak").textContent = data.streak;
        document.getElementById("freezes").textContent = data.freezes;
    })
    .catch(error => console.error("Помилка:", error));
}
updateStatus();


function createChart() {
    fetch("http://127.0.0.1:5000/get_chart_data")
    .then(response => response.json())
    .then(data => {
        let ctx = document.getElementById("chart").getContext("2d");
        new Chart(ctx, {
            type: "line",
            data: {
                labels: data.map((_, i) => i + 1),
                datasets: [{
                    label: "Дані",
                    data: data,
                    borderColor: "blue",
                    fill: false
                }]
            }
        });
    });
}
createChart()