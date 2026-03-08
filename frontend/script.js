// Cache DOM elements
const elements = {
    codeInput: document.getElementById('codeInput'),
    explainBtn: document.getElementById('explainBtn'),
    loadingState: document.getElementById('loading'),
    outputSection: document.getElementById('outputSection'),
    resultContainer: document.getElementById('resultContainer'),
    copyBtn: document.getElementById('copyBtn')
};

// Configure Marked.js to use Highlight.js for code blocks
marked.setOptions({
    highlight: function(code, lang) {
        const language = hljs.getLanguage(lang) ? lang : 'plaintext';
        return hljs.highlight(code, { language }).value;
    }
});

// Handle the API Request
elements.explainBtn.addEventListener('click', async () => {
    const code = elements.codeInput.value.trim();

    if (!code) {
        alert("Please paste some Python code first!");
        return;
    }

    // Update UI for loading state
    elements.loadingState.classList.remove('hidden');
    elements.outputSection.classList.add('hidden');
    elements.explainBtn.disabled = true;
    elements.explainBtn.innerHTML = 'Analyzing...';

    try {
        const response = await fetch('http://127.0.0.1:8000/explain', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Failed to connect to the backend.');
        }

        // Parse Markdown and inject into the DOM
        elements.resultContainer.innerHTML = marked.parse(data.result);
        
        // Reveal the output section
        elements.outputSection.classList.remove('hidden');

    } catch (error) {
        elements.resultContainer.innerHTML = `<p style="color: var(--accent-red);">Error: ${error.message}</p>`;
        elements.outputSection.classList.remove('hidden');
    } finally {
        // Reset loading state
        elements.loadingState.classList.add('hidden');
        elements.explainBtn.disabled = false;
        elements.explainBtn.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg> Analyze Code`;
    }
});

// Handle the Copy to Clipboard feature
elements.copyBtn.addEventListener('click', async () => {
    try {
        // Grab the raw text content of the result container (strips out HTML tags)
        const textToCopy = elements.resultContainer.innerText;
        await navigator.clipboard.writeText(textToCopy);
        
        // Temporarily change button text to show success
        const originalHtml = elements.copyBtn.innerHTML;
        elements.copyBtn.innerHTML = 'Copied!';
        setTimeout(() => {
            elements.copyBtn.innerHTML = originalHtml;
        }, 2000);
    } catch (err) {
        console.error('Failed to copy text: ', err);
        alert('Failed to copy to clipboard.');
    }
});