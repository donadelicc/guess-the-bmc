let correctCompany = '';
let score = 0;
let gameStarted = false;
let timer;
let totalTime = 0;
let currentRound = 0;
const maxRounds = 5;

// Variabler for TPBM (Time Per Business Model)
let roundStartTime;
let roundTimes = []; // Liste for å lagre tidene per runde
let tpbmTimerRunning = true; // For å spore om TPBM-klokken kjører


document.getElementById('start-game').addEventListener('click', function() {
    if (!gameStarted) {
        gameStarted = true;

        // Skjul hovedtittelen og startknappen
        document.getElementById('start-knapp-container').style.display = 'none';
        document.getElementById('main-image').style.display = 'none';


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
        let resultElement = document.getElementById('result');

        // Stopp TPBM-klokken når svaret er sendt inn
        if (tpbmTimerRunning) {
            let roundEndTime = Date.now();
            let roundTime = (roundEndTime - roundStartTime) / 1000; // I sekunder
            roundTimes.push(roundTime);
            tpbmTimerRunning = false; // Sørg for at klokken ikke fortsetter
        }

        document.getElementById('guess').style.display = 'none';
        document.getElementById('submit-guess').style.display = 'none';

        if (data.result === 'correct') {
            score++;
            document.getElementById('score').textContent = `Score: ${score}`; // Oppdater poeng            
            resultElement.textContent = 'Correct!';
            resultElement.style.backgroundColor = 'green';
            resultElement.style.color = 'white';
            resultElement.classList.add('correct-guess');
        } else {
            resultElement.textContent = `Wrong! The correct company was ${data.correct_company}.`;
            resultElement.style.backgroundColor = 'red';
            resultElement.style.color = 'white';
            resultElement.classList.add('wrong-guess');        
        }
        // Vis "Neste"-knappen etter at svaret er sendt inn
        document.getElementById('next-round').style.display = ''; 
    });
});


document.getElementById('next-round').addEventListener('click', function() {
    if (currentRound < maxRounds) {
        // Start neste runde
        startNewRound();
    } else {
        clearInterval(timer);
        
        // Beregn TPBM (gjennomsnittet av rundetidene)
        let totalRoundTime = roundTimes.reduce((acc, time) => acc + time, 0);
        let TPBM = (totalRoundTime / roundTimes.length).toFixed(2);

        window.location.href = `/stats?score=${score}&TPBM=${TPBM}&time=${formatTime(totalTime)}`;
    }
});



function startNewRound() {
    currentRound++;
    document.getElementById('guess').value = '';
    document.getElementById('bmc-container').style.display = 'block';
    document.getElementById('guess').style.display = '';
    document.getElementById('submit-guess').style.display = '';
    document.getElementById('result').textContent = ''; // Fjern tidligere resultat
    document.getElementById('next-round').style.display = 'none'; // Skjul "Neste"-knappen

    // Oppdater rundetall i rundeoverskriften
    document.getElementById('round-header').textContent = `Runde ${currentRound}`;

    // Start timer for ny runde
    roundStartTime = Date.now();
    tpbmTimerRunning = true; // Sett TPBM-timeren til å kjøre

    fetch('/get_bmc')
    .then(response => response.json())
    .then(data => {
        correctCompany = data.company;
        displayFormattedText('key_partners', data.bmc.key_partners);
        displayFormattedText('key_activities', data.bmc.key_activities);
        displayFormattedText('key_resources', data.bmc.key_resources);
        displayFormattedText('value_proposition', data.bmc.value_proposition);
        displayFormattedText('customer_relationships', data.bmc.customer_relationships);
        displayFormattedText('channels', data.bmc.channels);
        displayFormattedText('customer_segments', data.bmc.customer_segments);
        displayFormattedText('cost_structure', data.bmc.cost_structure);
        displayFormattedText('revenue_streams', data.bmc.revenue_streams);
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

function displayFormattedText(elementId, dataArray) {
    const element = document.getElementById(elementId);
    // Split the data by commas and join with line breaks
    element.innerHTML = dataArray.map(item => `<div>${item}</div>`).join('');
}