document.addEventListener('DOMContentLoaded', () => {
    const questionForm = document.getElementById('questionForm');
    const queryInput = document.getElementById('query');
    const submitBtn = document.getElementById('submitBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const answerContainer = document.getElementById('answerContainer');
    const answerContent = document.getElementById('answerContent');
    const errorContainer = document.getElementById('errorContainer');
    const errorContent = document.getElementById('errorContent');

    // API endpoint (backend runs on port 9090)
    const API_URL = 'http://localhost:9090/ask';

    // Function to show loading state
    function showLoading() {
        submitBtn.disabled = true;
        loadingIndicator.classList.remove('hidden');
        answerContainer.classList.add('hidden');
        errorContainer.classList.add('hidden');
    }

    // Function to show answer
    function showAnswer(answer) {
        loadingIndicator.classList.add('hidden');
        answerContainer.classList.remove('hidden');
        answerContent.textContent = answer;
        submitBtn.disabled = false;
    }

    // Function to show error
    function showError(error) {
        loadingIndicator.classList.add('hidden');
        errorContainer.classList.remove('hidden');
        errorContent.textContent = error;
        submitBtn.disabled = false;
    }

    // Function to ask a question
    async function askQuestion(query) {
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: query,
                    top_k: 5
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            return data.answer;
        } catch (error) {
            throw new Error(`Failed to get answer: ${error.message}`);
        }
    }

    // Form submission handler
    questionForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const query = queryInput.value.trim();
        if (!query) {
            showError('Please enter a question.');
            return;
        }

        showLoading();

        try {
            const answer = await askQuestion(query);
            showAnswer(answer);
        } catch (error) {
            showError(error.message);
        }
    });
});
