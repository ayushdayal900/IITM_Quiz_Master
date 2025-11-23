function confirmDelete() {
    return confirm("Confirm to DELETE?");
}

function confirmUpdate() {
    return confirm("Confirm to UPDATE?");
}

// Timer function
function startTimer(durationInSeconds, display) {
    let startTime = sessionStorage.getItem("quizStartTime");
    let now = Math.floor(Date.now() / 1000); // Current timestamp in seconds

    // If the timer was already started before, calculate remaining time
    if (startTime) {
        let elapsed = now - parseInt(startTime, 10);
        durationInSeconds -= elapsed;
    } else {
        // First time starting the timer
        sessionStorage.setItem("quizStartTime", now);
    }

    if (durationInSeconds <= 0) {
        display.textContent = "Time Over!";
        alert("Time is up! Submitting the answer.");
        document.getElementById("quiz-form").submit();
        return;
    }

    let timer = durationInSeconds, minutes, seconds;
    let countdown = setInterval(function () {
        minutes = Math.floor(timer / 60);
        seconds = timer % 60;

        seconds = seconds < 10 ? "0" + seconds : seconds;
        minutes = minutes < 10 ? "0" + minutes : minutes;
        display.textContent = `Time Left: ${minutes}:${seconds}`;

        if (--timer < 0) {
            clearInterval(countdown);
            alert("Time is up! Submitting the answer.");
            document.getElementById("quiz-form").submit();
        }
    }, 1000);
}

// Start the timer only if it's the first question or resume if ongoing
window.onload = function () {
    const timerDisplay = document.getElementById('timer');
    startTimer(900, timerDisplay);
};
