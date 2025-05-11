<script>
function askQuestion() {
    const question = document.getElementById('question').value;

    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response').innerText = data.answer;
    })
    .catch(error => {
        document.getElementById('response').innerText = 'Error: ' + error;
    });
}

function filterCategory() {
    const selectedCategory = document.getElementById('category').value;
    const rows = document.querySelectorAll('#highlights-table tbody tr');

    rows.forEach(row => {
        const category = row.getAttribute('data-category');
        if (selectedCategory === 'all' || category === selectedCategory) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

</script>