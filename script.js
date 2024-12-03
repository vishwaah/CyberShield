document.getElementById('urlForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const url = document.getElementById('urlInput').value;
    const resultsDiv = document.getElementById('results');
    const scoreDiv = document.getElementById('score');
    const detailsPre = document.getElementById('details');

    resultsDiv.classList.add('hidden');
    scoreDiv.textContent = 'Loading...';

    try {
        const response = await fetch('/http://127.0.0.1:5000/api/check-url', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url }),
        });

        if (response.ok) {
            const result = await response.json();
            const finalScore = result.final_score.toFixed(2);
            const details = JSON.stringify(result.details, null, 2);

            scoreDiv.textContent = `Final Score: ${finalScore}`;
            detailsPre.textContent = details;
            resultsDiv.classList.remove('hidden');
        } else {
            scoreDiv.textContent = 'Error occurred while fetching results.';
        }
    } catch (error) {
        scoreDiv.textContent = 'Error connecting to the server.';
    }
});
