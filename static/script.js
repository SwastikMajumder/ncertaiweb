document.addEventListener('DOMContentLoaded', function() {
    // Function to get URL parameters
    function getUrlParameter(name) {
        name = name.replace(/[\[\]]/g, '\\$&');
        const regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
            results = regex.exec(window.location.href);
        if (!results) return null;
        if (!results[2]) return '';
        return decodeURIComponent(results[2].replace(/\+/g, ' '));
    }

    // Check for equation parameter in URL and trigger integration if present
    const equation = getUrlParameter('equation');
    if (equation) {
        const logsOutput = document.getElementById('logs-output');
        logsOutput.innerHTML = ''; // Clear logs here

        // Populate input box with equation from URL
        document.getElementById('mathInput').value = equation;

        let outputElement = document.getElementById('math-output');
        outputElement.innerHTML = ''; // Clear output area here, before fetch

        fetch(`/integration/integrate_url/${encodeURIComponent(equation)}`)
            .then(response => response.json())
            .then(data => {
                try {
                    renderMathTree(data.tree, outputElement);
                } catch (error) {
                    console.error("Error during rendering:", error);
                }
            })
            .catch(error => {
                console.error('Error fetching integration result:', error);
            });
    }

    document.getElementById('integrateButton').addEventListener('click', function() {
        let mathInput = document.getElementById('mathInput').value;
        const logsOutput = document.getElementById('logs-output');
        logsOutput.innerHTML = ''; // Clear logs here

        let outputElement = document.getElementById('math-output');
        outputElement.innerHTML = ''; // Clear output area here, before fetch

        fetch('/integration/integrate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ expression: mathInput })
        })
        .then(response => response.json())
        .then(data => {
            try {
                renderMathTree(data.tree, outputElement);
            } catch (error) {
                console.error("Error during rendering:", error);
            }
        })
        .catch(error => {
            console.error('Error fetching integration result:', error);
        });

        // Start log fetching and display inside the button click
        storedLogs = []; //reset the stored logs.
        logCollectionActive = true;
        clearTimeout(timeoutID); // Clear any existing timeout
        timeoutID = setTimeout(function logFetcher(){ // create a self contained function.
            if (!logCollectionActive) return;

            fetch('/integration/get_logs')
                .then(response => response.json())
                .then(data => {
                    storedLogs = storedLogs.concat(data.logs); // Add new logs
                    logsOutput.innerHTML = storedLogs.filter(log => !["PAUSE", "END_LOG_COLLECTION"].includes(log)).join('<br>'); // Filter out PAUSE and END_LOG_COLLECTION

                    if (data.logs.some(log => log.includes("END_LOG_COLLECTION"))) {
                        logCollectionActive = false;
                        console.log("Logs stopped.");
                        clearTimeout(timeoutID); // Stop further timeouts
                    } else {
                        storedLogs.push("PAUSE"); // Add pause marker
                        timeoutID = setTimeout(logFetcher, 1000); // Schedule next fetch
                    }
                })
                .catch(error => console.error('Error:', error));

        },1000); // start the log fetching.
    });

    // Log polling
    let storedLogs = [];
    let logCollectionActive = true;
    let timeoutID = null; // Store the timeout ID
    let logFetchRunning = false; // Add a flag to prevent multiple fetch loops

    //log fetching function.
    function fetchLogs() {
        if (!logCollectionActive || logFetchRunning) return; // Prevent multiple fetch loops
        logFetchRunning = true; // Set flag to true

        fetch('/integration/get_logs')
            .then(response => response.json())
            .then(data => {
                const logsOutput = document.getElementById('logs-output');
                storedLogs = storedLogs.concat(data.logs); // Add new logs
                logsOutput.innerHTML = storedLogs.filter(log => !["PAUSE", "END_LOG_COLLECTION"].includes(log)).join('<br>'); // Filter out PAUSE and END_LOG_COLLECTION

                if (data.logs.some(log => log.includes("END_LOG_COLLECTION"))) {
                    logCollectionActive = false;
                    console.log("Logs stopped.");
                    clearTimeout(timeoutID); // Stop further timeouts
                } else {
                    storedLogs.push("PAUSE"); // Add pause marker
                    timeoutID = setTimeout(fetchLogs, 1000); // Schedule next fetch
                }
            })
            .catch(error => console.error('Error:', error))
            .finally(() => {
                logFetchRunning = false; // Reset flag after fetch completes
            });
    }

    // Start log polling
    timeoutID = setTimeout(fetchLogs, 1000); // Start the first fetch
});