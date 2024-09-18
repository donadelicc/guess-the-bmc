document.getElementById('bmc-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Hindre standard skjemaoppførsel

    // Hent data fra skjemaet, og bruk 'N/A' hvis feltet er tomt
    const companyName = document.getElementById('company-name').value || 'N/A';
    const keyPartners = document.getElementById('key-partners').value ? 
        document.getElementById('key-partners').value.split(',').map(item => item.trim()) : ['N/A'];
    const keyActivities = document.getElementById('key-activities').value ? 
        document.getElementById('key-activities').value.split(',').map(item => item.trim()) : ['N/A'];
    const keyResources = document.getElementById('key-resources').value ? 
        document.getElementById('key-resources').value.split(',').map(item => item.trim()) : ['N/A'];
    const valueProposition = document.getElementById('value-proposition').value || 'N/A';
    const customerRelationships = document.getElementById('customer-relationships').value ? 
        document.getElementById('customer-relationships').value.split(',').map(item => item.trim()) : ['N/A'];
    const channels = document.getElementById('channels').value ? 
        document.getElementById('channels').value.split(',').map(item => item.trim()) : ['N/A'];
    const customerSegments = document.getElementById('customer-segments').value ? 
        document.getElementById('customer-segments').value.split(',').map(item => item.trim()) : ['N/A'];
    const costStructure = document.getElementById('cost-structure').value ? 
        document.getElementById('cost-structure').value.split(',').map(item => item.trim()) : ['N/A'];
    const revenueStreams = document.getElementById('revenue-streams').value ? 
        document.getElementById('revenue-streams').value.split(',').map(item => item.trim()) : ['N/A'];

    // Liste over felter som kan fylles ut
    const fields = [
        keyPartners, keyActivities, keyResources, customerRelationships,
        channels, customerSegments, costStructure, revenueStreams
    ];

    // Tell antall felter som er fylt ut
    let filledFieldsCount = fields.filter(field => field[0] !== 'N/A').length;

    // Sjekk om selskapets navn og value proposition er fylt ut
    if (companyName === 'N/A') {
        alert("Selskapets navn må fylles ut.");
        return;
    }

    if (valueProposition === 'N/A') {
        alert("Value Proposition må fylles ut.");
        return;
    }

    // Legg til Value Proposition og Selskapets navn i antall utfylte felter
    filledFieldsCount += 2;

    // Sjekk om minst 4 felter er fylt ut
    if (filledFieldsCount < 4) {
        alert("Minst 4 felter må være fylt ut, inkludert 'Value Proposition' og 'Selskapets navn'.");
        return;
    }

    // Validering bestått, lag JSON-data
    const bmcData = {
        company_name: companyName || 'N/A',
        key_partners: keyPartners || 'N/A',
        key_activities: keyActivities || 'N/A',
        key_resources: keyResources || 'N/A',
        value_proposition: valueProposition || 'N/A',
        customer_relationships: customerRelationships || 'N/A',
        channels: channels || 'N/A',
        customer_segments: customerSegments || 'N/A',
        cost_structure: costStructure || 'N/A',
        revenue_streams: revenueStreams || 'N/A'
    };

    console.log(bmcData); // For debugging, her kan du sende data til serveren


    // Send data til serveren
    fetch('/add_bmc', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(bmcData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('BMC registrert!', 'green');
            document.getElementById('bmc-form').reset();
        } else {
            showNotification('Noe gikk galt. Prøv igjen.', 'red');
        }
    })
    .catch(error => {
        showNotification('Feil ved registrering av BMC. Prøv igjen eller oppdater siden.', 'red');
    });
});

function showNotification(message, color) {
    const notification = document.getElementById('notification');
    const notificationMessage = document.getElementById('notification-message');
    
    notificationMessage.textContent = message;
    notification.style.backgroundColor = color;
    notification.style.display = 'block'; // Viser notifikasjonen
    
    // Skjul notifikasjonen etter 5 sekunder
    setTimeout(() => {
        notification.style.display = 'none';
    }, 5000);
}
