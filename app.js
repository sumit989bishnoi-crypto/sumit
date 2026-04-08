  document.addEventListener('DOMContentLoaded', () => {
    const codeInput = document.getElementById('codeInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const analyzeSpinner = document.getElementById('analyzeSpinner');
    const outputSection = document.getElementById('outputSection');
    const errorExplanation = document.getElementById('errorExplanation');
    const fixedCode = document.getElementById('fixedCode');
    const copyBtn = document.getElementById('copyBtn');
    const copyText = document.getElementById('copyText');

    analyzeBtn.addEventListener('click', async () => {
        const code = codeInput.value.trim();
        
        if (!code) {
            alert('Please paste some code first!');
            return;
        }

        // Show loading state
        analyzeBtn.disabled = true;
        analyzeBtn.classList.add('opacity-80', 'cursor-not-allowed');
        analyzeSpinner.classList.remove('hidden');
        outputSection.classList.add('hidden');

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    code: code,
                    language: 'python' // Hardcoded as per MVP specs
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Server responded with an error');
            }

            // Populate text
            errorExplanation.textContent = data.error || "No explanation provided.";
            fixedCode.textContent = data.fixed_code || "No code provided.";

            // Show output section
            outputSection.classList.remove('hidden');
            
            // Scroll to output
            outputSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        } catch (error) {
            // Error handling matching instructions
            errorExplanation.textContent = error.message || "The bug is too powerful, try again!";
            fixedCode.textContent = "";
            outputSection.classList.remove('hidden');
        } finally {
            // Revert loading state
            analyzeBtn.disabled = false;
            analyzeBtn.classList.remove('opacity-80', 'cursor-not-allowed');
            analyzeSpinner.classList.add('hidden');
        }
    });

    copyBtn.addEventListener('click', () => {
        const textToCopy = fixedCode.textContent;
        if (!textToCopy) return;

        navigator.clipboard.writeText(textToCopy).then(() => {
            const originalText = copyText.textContent;
            copyText.textContent = 'Copied!';
            copyBtn.classList.replace('bg-slate-700', 'bg-emerald-600');
            
            setTimeout(() => {
                copyText.textContent = originalText;
                copyBtn.classList.replace('bg-emerald-600', 'bg-slate-700');
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy: ', err);
            alert('Failed to copy code to clipboard.');
        });
    });
});
