// UI Interactivity
document.addEventListener('DOMContentLoaded', () => {
    // Sidebar Toggle
    const menuBtn = document.querySelector('#menu-btn');
    const closeBtn = document.querySelector('#close-btn');
    const sideBar = document.querySelector('.side-bar');
    const body = document.body;

    if (menuBtn) {
        menuBtn.onclick = () => {
            sideBar.classList.toggle('active');
            body.classList.toggle('active');
        };
    }

    if (closeBtn) {
        closeBtn.onclick = () => {
            sideBar.classList.remove('active');
            body.classList.remove('active');
        };
    }

    // Profile Toggle 
    const userBtn = document.querySelector('#user-btn');
    const profile = document.querySelector('.profile');
    
    // Note: The original CSS/HTML structure for profile toggle might need adjustment 
    // based on the new CSS, but keeping basic logic here.
    if(userBtn && profile){
         userBtn.onclick = () =>{
             profile.classList.toggle('active');
         }
    }
    
    // Timer Logic (Conditional)
    const timerDisplay = document.getElementById('timer');
    if (timerDisplay) {
        // Set default or get from element attribute
        let duration = timerDisplay.getAttribute('data-duration') || 900; 
        startTimer(duration, timerDisplay);
    }
});

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
    // Logic: Only use session storage if we are in the Same quiz session. 
    // For simplicity, we'll assume yes for now, but a quiz ID check would be better.
    
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
        submitQuizForm();
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
            submitQuizForm();
        }
    }, 1000);
}

function submitQuizForm(){
    const form = document.getElementById("quiz-form");
    if(form) form.submit();
}

