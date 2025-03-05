let timeLeft = 15 * 60; // 15 minutes in seconds
const timerElement = document.getElementById("timer");

function updateTimer() {
    let minutes = Math.floor(timeLeft / 60);
    let seconds = timeLeft % 60;
    timerElement.textContent = `00:${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    
    if (timeLeft > 0) {
        timeLeft--;
        setTimeout(updateTimer, 1000);
    } else {
        alert("Time's up! Submitting quiz...");
        window.location.href = "/quiz/summary";
    }
}

updateTimer();
