updateStatus()

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
        document.getElementById("warning").textContent = `Ваш стрік зіб'ється ${data.lost_day}. Останній день коли можна відновити свій відрізок ${data.reset_day}!`
    })
    .catch(error => console.error("Помилка:", error));
}

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

function cancel() {
    let text = "Cancel"
    fetch("http://127.0.0.1:5000/cancel", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        updateStatus();
    })
    .catch(error => console.error("Помилка:", error));
}