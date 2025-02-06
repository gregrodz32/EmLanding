document.getElementById("start-flight-btn").addEventListener("click", function() {
    fetch('/start-flight', { method: 'POST' }).then(response => response.json()).then(data => {
        console.log(data);
    });
});

document.getElementById("pause-flight-btn").addEventListener("click", function() {
    fetch('/pause-flight', { method: 'POST' }).then(response => response.json()).then(data => {
        console.log(data);
    });
});
