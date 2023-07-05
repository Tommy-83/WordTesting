document.addEventListener('DOMContentLoaded', () => {
    const guessForm = document.getElementById('guess-form');
    const guessInput = document.getElementById('guess-input');
    const messageDiv = document.getElementById('message');
    const timerDiv = document.getElementById('timer');
    const gridDiv = document.getElementById('grid');
    let timer;

    // Function to update the timer display
    function updateTimer(startTime) {
        const currentTime = new Date();
        const timeElapsed = Math.floor((currentTime - startTime) / 1000); // Time elapsed in seconds
        const minutes = Math.floor(timeElapsed / 60);
        const seconds = timeElapsed % 60;
        timerDiv.innerText = `Time Elapsed: ${minutes} minutes ${seconds} seconds`;
    }

    // Function to display the grid with the guessed letters
    function displayGrid(grid) {
        gridDiv.innerHTML = '';
        grid.forEach(row => {
            const rowDiv = document.createElement('div');
            rowDiv.classList.add('row');
            row.forEach(letter => {
                const cellDiv = document.createElement('div');
                cellDiv.classList.add('cell');
                if (letter.visible) {
                    cellDiv.classList.add('visible');
                }
                cellDiv.classList.add(letter.color);
                cellDiv.innerText = letter.letter;
                rowDiv.appendChild(cellDiv);
            });
            gridDiv.appendChild(rowDiv);
        });
    }

    // Function to handle the form submission
    function handleSubmit(event) {
        event.preventDefault();
        const guess = guessInput.value.trim();
        if (guess !== '') {
            guessInput.value = '';
            messageDiv.innerText = '';

            fetch('/play', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `guess=${guess}`,
            })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        messageDiv.innerText = data.error;
                    } else {
                        displayGrid(data.grid);
                        messageDiv.innerText = data.message;
                        if (data.message.startsWith('Congratulations')) {
                            clearInterval(timer);
                        }
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    }

    // Start the game
    guessForm.addEventListener('submit', handleSubmit);

    // Initialize the timer
    const startTime = new Date();
    updateTimer(startTime);
    timer = setInterval(() => {
        updateTimer(startTime);
    }, 1000);
});
