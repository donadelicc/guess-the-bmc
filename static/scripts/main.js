let correctCompany = '';
let score = 0;
let gameStarted = false;
let timer;
let totalTime = 0;
let currentRound = 0;
const maxRounds = 5; // Spilleren får 5 BMC-er på rad

document.getElementById('start-game').addEventListener('click', function() {
    if (!gameStarted) {
        gameStarted = true;

        // Skjul hovedtittelen og startknappen
        document.getElementById('main-title').style.display = 'none';
        document.getElementById('start-game').style.display = 'none';

        // Vis rundetittelen
        document.getElementById('round-header').style.display = 'block';
        document.getElementById('round-header').textContent = `Runde 1`;

        startTimer();
        startNewRound();
    }
});

document.getElementById('submit-guess').addEventListener('click', function() {
    let guess = document.getElementById('guess').value;
    fetch('/check_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            guess: guess,
            correct_company: correctCompany
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.result === 'correct') {
            score++;
            document.getElementById('result').textContent = 'Correct!';
            document.getElementById('score').textContent = `Score: ${score}`;
        } else {
            document.getElementById('result').textContent = `Wrong! The correct company was ${data.correct_company}.`;
        }

        if (currentRound < maxRounds) {
            startNewRound();
        } else {
            clearInterval(timer);
            // document.getElementById('result').textContent = `Game Over! Your score: ${score}. Time taken: ${formatTime(totalTime)}.`;
            window.location.href = `/stats?score=${score}&time=${formatTime(totalTime)}`;
        }
    });
});

function startNewRound() {
    currentRound++;
    document.getElementById('guess').value = '';
    document.getElementById('bmc-container').style.display = 'block';

    // Oppdater rundetall i rundeoverskriften
    document.getElementById('round-header').textContent = `Runde ${currentRound}`;

    fetch('/get_bmc')
    .then(response => response.json())
    .then(data => {
        correctCompany = data.company;

        document.getElementById('key_partners').textContent = data.bmc.key_partners.join(', ');
        document.getElementById('key_activities').textContent = data.bmc.key_activities.join(', ');
        document.getElementById('key_resources').textContent = data.bmc.key_resources ? data.bmc.key_resources.join(', ') : 'N/A';
        document.getElementById('value_proposition').textContent = data.bmc.value_proposition;
        document.getElementById('customer_relationships').textContent = data.bmc.customer_relationships.join(', ');
        document.getElementById('channels').textContent = data.bmc.channels.join(', ');
        document.getElementById('customer_segments').textContent = data.bmc.customer_segments.join(', ');
        document.getElementById('cost_structure').textContent = data.bmc.cost_structure || 'N/A';
        document.getElementById('revenue_streams').textContent = data.bmc.revenue_streams.join(', ');
    });
}

function startTimer() {
    timer = setInterval(function() {
        totalTime++;
        document.getElementById('clock').textContent = `Time: ${formatTime(totalTime)}`;
    }, 1000);
}

function formatTime(seconds) {
    let minutes = Math.floor(seconds / 60);
    let remainingSeconds = seconds % 60;
    return `${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`;
}