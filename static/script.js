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
    });

    // Polling for logs
    function fetchLogs() {
        fetch('/integration/get_logs')
        .then(response => response.json())
        .then(data => {
            const logsOutput = document.getElementById('logs-output');
            logsOutput.innerHTML = data.logs.join('<br>'); // Display logs
        })
        .catch(error => {
            console.error('Error fetching logs:', error);
        });
    }

    // Fetch logs every 1 second (adjust as needed)
    setInterval(fetchLogs, 1000);
});