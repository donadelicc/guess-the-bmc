let correctCompany = '';
let usedCompanies = []; // Liste over selskaper som allerede er blitt brukt
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

// Funksjon for å hente en ny BMC som ikke allerede er brukt
async function getUniqueBMC() {
    let data;
    do {
        const response = await fetch('/get_bmc');
        data = await response.json();
    } while (usedCompanies.includes(data.company)); // Fortsett å hente til vi får et unikt selskap

    // Når vi har et unikt selskap, legg det til listen over brukte selskaper
    usedCompanies.push(data.company);
    return data;
}


document.getElementById('start-game').addEventListener('click', function() {
    if (!gameStarted) {
        gameStarted = true;
        document.getElementById('game-bar').style.display = 'flex';
        document.getElementById('start-knapp-container').style.display = 'none';
        document.getElementById('main-image').style.display = 'none';
        document.getElementById('game-score-value').textContent = '0';
        document.getElementById('round-number').textContent = '1';
        document.getElementById('game-time-value').textContent = '00:00';

        // Start timer og spill
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
        resultElement.style.display = '';
        
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
            document.getElementById('game-score-value').textContent = score; // Oppdater poeng            
            resultElement.textContent = 'Correct!';
            resultElement.style.backgroundColor = '#DD650E';
            resultElement.style.color = 'white';
            resultElement.classList.add('correct-guess');
        } else {
            resultElement.textContent = `Wrong! The correct company was ${data.correct_company}.`;
            resultElement.style.backgroundColor = '#DD650E';
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

    // Vise inputfeltet og submit-knappen på nytt
    document.getElementById('guess').style.display = '';
    document.getElementById('submit-guess').style.display = '';

    // Tømme resultatfeltet og skjule "Neste"-knappen
    document.getElementById('result').textContent = '';
    document.getElementById('result').style.display = 'none'; 
    document.getElementById('next-round').style.display = 'none';

    // Oppdater rundetall i game-bar
    document.getElementById('round-number').textContent = currentRound;

    // Start timer for ny runde
    roundStartTime = Date.now();
    tpbmTimerRunning = true; // Sett TPBM-timeren til å kjøre

    getUniqueBMC().then(data => {
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
        document.getElementById('game-time-value').textContent = formatTime(totalTime); // Oppdater tid i game-bar
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
