/**
 * Frontend JavaScript for Excel Formula Optimizer
 * Handles API communication and UI updates
 */

// API base URL - automatically detects dev vs production
const API_BASE_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? 'http://localhost:8001'  // Development
    : window.location.origin;   // Production (same origin as frontend)

console.log('API_BASE_URL:', API_BASE_URL);
console.log('window.location:', window.location);

/**
 * Display an error message to the user
 */
function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.classList.add('show');

    // Hide error after 5 seconds
    setTimeout(() => {
        errorDiv.classList.remove('show');
    }, 5000);
}

/**
 * Show loading spinner
 */
function showLoading() {
    document.getElementById('loading').classList.add('show');
    document.getElementById('beautify-btn').disabled = true;
    document.getElementById('simplify-btn').disabled = true;
}

/**
 * Hide loading spinner
 */
function hideLoading() {
    document.getElementById('loading').classList.remove('show');
    document.getElementById('beautify-btn').disabled = false;
    document.getElementById('simplify-btn').disabled = false;
}

/**
 * Display results in the UI
 */
function showResults(data, showSimplified = false) {
    const resultsDiv = document.getElementById('results');
    const prettyResult = document.getElementById('pretty-result');
    const simplifiedSection = document.getElementById('simplified-section');
    const simplifiedResult = document.getElementById('simplified-result');
    const commentSection = document.getElementById('comment-section');
    const commentText = document.getElementById('comment-text');

    // Show beautified result
    prettyResult.textContent = data.pretty;

    // Show or hide simplified result based on the endpoint called
    if (showSimplified && data.simplified) {
        simplifiedResult.textContent = data.simplified;
        simplifiedSection.style.display = 'block';
    } else {
        simplifiedSection.style.display = 'none';
    }

    // Show or hide comment based on the endpoint called
    if (showSimplified && data.comment) {
        commentText.textContent = data.comment;
        commentSection.style.display = 'block';
    } else {
        commentSection.style.display = 'none';
    }

    // Show results container
    resultsDiv.classList.add('show');
}

/**
 * Beautify the formula
 */
async function beautifyFormula() {
    const formulaInput = document.getElementById('formula-input');
    const formula = formulaInput.value.trim();

    if (!formula) {
        showError('Please enter a formula');
        return;
    }

    showLoading();

    try {
        const response = await fetch(`${API_BASE_URL}/format`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ formula }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to format formula');
        }

        const data = await response.json();
        showResults(data, false);
    } catch (error) {
        showError(error.message || 'Failed to connect to the server');
    } finally {
        hideLoading();
    }
}

/**
 * Simplify the formula with AI
 */
async function simplifyFormula() {
    const formulaInput = document.getElementById('formula-input');
    const formula = formulaInput.value.trim();

    if (!formula) {
        showError('Please enter a formula');
        return;
    }

    showLoading();

    try {
        const response = await fetch(`${API_BASE_URL}/simplify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ formula }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to optimize formula');
        }

        const data = await response.json();
        showResults(data, true);
    } catch (error) {
        showError(error.message || 'Failed to connect to the server');
    } finally {
        hideLoading();
    }
}

/**
 * Copy text to clipboard
 */
async function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const text = element.textContent;

    try {
        await navigator.clipboard.writeText(text);

        // Visual feedback - find the copy button next to this element
        const copyBtn = element.parentElement.querySelector('.copy-btn');
        const originalHTML = copyBtn.innerHTML;

        // Show checkmark icon
        copyBtn.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
        `;
        copyBtn.classList.add('copied');

        setTimeout(() => {
            copyBtn.innerHTML = originalHTML;
            copyBtn.classList.remove('copied');
        }, 2000);
    } catch (error) {
        showError('Failed to copy to clipboard');
    }
}

/**
 * Allow Enter key to trigger beautify (Shift+Enter for new line)
 */
document.getElementById('formula-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        beautifyFormula();
    }
});

/**
 * Example formulas for testing
 */
const exampleFormulas = [
    '=IF(A1>0,IF(B1<10,"OK","NO"),"FAIL")',
    '=VLOOKUP(A1,Sheet2!A:B,2,FALSE)',
    '=SUMIFS(D:D,A:A,">=2023",B:B,"Sales")',
    '=IF(AND(A1>0,B1<10,C1="Active"),"Valid","Invalid")',
];

// Optional: Add example formula button
// Uncomment if you want to add this feature
/*
function loadExample() {
    const randomFormula = exampleFormulas[Math.floor(Math.random() * exampleFormulas.length)];
    document.getElementById('formula-input').value = randomFormula;
}
*/
