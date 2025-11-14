async function analyzeUrl() {
    const url = document.getElementById('urlInput').value;
    const resultDiv = document.getElementById('result');
    
    if (!url) {
        alert('Please enter a URL');
        return;
    }

    try {
        // Show loading state
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = '<p>Analyzing URL features...</p>';

        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();
        
        // Display results
        document.getElementById('scoreDisplay').textContent = `Score: ${data.score}`;
        document.getElementById('reasonsDisplay').innerHTML = 
            '<strong>Key Reasons:</strong><br>' + data.reasons.join('<br>');
        
    } catch (error) {
        console.error('Error:', error);
        resultDiv.innerHTML = '<p style="color: red;">Error analyzing URL</p>';
    }
}

function runDemo() {
    const demoType = document.getElementById('demoSelect').value;
    if (!demoType) return;

    const demoResults = {
        legitimate: { score: 12.5, reasons: ["Legitimate domain", "Trusted SSL certificate"] },
        suspicious: { score: 65.8, reasons: ["Suspicious domain age", "Unusual URL structure"] },
        phishing: { score: 92.3, reasons: ["Known phishing patterns", "Fake login page detected"] }
    };

    const result = demoResults[demoType];
    const resultDiv = document.getElementById('result');
    
    resultDiv.style.display = 'block';
    document.getElementById('scoreDisplay').textContent = `Score: ${result.score}`;
    document.getElementById('reasonsDisplay').innerHTML = 
        '<strong>Key Reasons:</strong><br>' + result.reasons.join('<br>');
}