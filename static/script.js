/* Italian Fiscal Code Calculator - JavaScript */

const form = document.getElementById('fiscalForm');
const resultDiv = document.getElementById('result');
const errorDiv = document.getElementById('error');

// Event listener for form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Hide previous results/errors
    resultDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
    
    // Get form data
    const formData = new FormData(form);
    const data = {
        surname: formData.get('surname'),
        name: formData.get('name'),
        birthDate: formData.get('birthDate'),
        gender: formData.get('gender'),
        municipality: formData.get('municipality')
    };
    
    try {
        // Send request to API
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'An error occurred');
        }
        
        const result = await response.json();
        displayResult(result);
        
    } catch (err) {
        displayError(err.message);
    }
});

/**
 * Display the generated fiscal code and breakdown
 */
function displayResult(result) {
    // Set fiscal code
    document.getElementById('fiscalCode').textContent = result.fiscalCode;
    
    // Set breakdown
    const breakdown = result.breakdown;
    document.getElementById('bd-surname').textContent = breakdown.surname;
    document.getElementById('bd-name').textContent = breakdown.name;
    document.getElementById('bd-year').textContent = breakdown.year;
    document.getElementById('bd-month').textContent = breakdown.month;
    document.getElementById('bd-day').textContent = breakdown.day;
    document.getElementById('bd-municipality').textContent = breakdown.municipality;
    document.getElementById('bd-checkDigit').textContent = breakdown.checkDigit;
    
    // Show result
    resultDiv.classList.remove('hidden');
    
    // Scroll to result
    resultDiv.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Display error message
 */
function displayError(message) {
    errorDiv.textContent = '❌ ' + message;
    errorDiv.classList.remove('hidden');
    
    // Scroll to error
    errorDiv.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Copy fiscal code to clipboard
 */
function copyToClipboard() {
    const code = document.getElementById('fiscalCode').textContent;
    
    navigator.clipboard.writeText(code).then(() => {
        const btn = event.target;
        const originalText = btn.textContent;
        
        btn.textContent = '✓ Copied!';
        btn.style.color = '#27ae60';
        
        setTimeout(() => {
            btn.textContent = originalText;
            btn.style.color = '';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

/**
 * Reset form and results
 */
function resetForm() {
    form.reset();
    resultDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
    
    // Scroll to top
    form.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Load demo data
 */
async function loadDemo() {
    try {
        const response = await fetch('/api/demo');
        const data = await response.json();
        
        document.getElementById('surname').value = data.surname;
        document.getElementById('name').value = data.name;
        document.getElementById('birthDate').value = data.birthDate;
        document.getElementById('municipality').value = data.municipality;
        
    } catch (err) {
        console.error('Failed to load demo data:', err);
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl+Enter to submit
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        if (!resultDiv.classList.contains('hidden')) {
            return; // Don't submit if result is showing
        }
        form.dispatchEvent(new Event('submit'));
    }
    
    // Escape to reset
    if (e.key === 'Escape' && !resultDiv.classList.contains('hidden')) {
        resetForm();
    }
});

// Date format validation
const dateInput = document.getElementById('birthDate');
dateInput.addEventListener('blur', (e) => {
    let value = e.target.value.trim();
    
    // Auto-format date if user enters it without slashes
    if (value.length === 8 && !value.includes('/')) {
        value = value.slice(0, 2) + '/' + value.slice(2, 4) + '/' + value.slice(4);
        e.target.value = value;
    }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Add some nice animations
    const inputs = document.querySelectorAll('input[type="text"], input[type="date"]');
    inputs.forEach(input => {
        input.addEventListener('focus', (e) => {
            e.target.parentElement.classList.add('focused');
        });
        input.addEventListener('blur', (e) => {
            e.target.parentElement.classList.remove('focused');
        });
    });
});
