let currentTaskIndex = -1;
let tasks = [];
let selectedBoxes = [];

async function generateInitialTasks() {
    try {
        const response = await fetch("http://127.0.0.1:5000/generate_initial_tasks", {
            method: "POST"
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        tasks = data.initial_tasks;
        console.log("Initial tasks generated:", tasks);
    } catch (error) {
        console.error("Failed to generate initial tasks:", error);
    }
}

async function displayBoxes() {
    if (currentTaskIndex >= tasks.length) {
        document.getElementById("content").innerHTML = "No more tasks available.";
        return;
    }

    const task = tasks[currentTaskIndex];
    const container = document.getElementById('box-container');
    container.innerHTML = '';

    task.forEach((address, index) => {
        const box = document.createElement('div');
        box.className = 'box';
        box.dataset.index = index;
        box.onclick = toggleSelection;

        // Code to display NFT images related to this address would go here

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        box.appendChild(checkbox);

        box.innerHTML += address;

        container.appendChild(box);
    });
    document.getElementById("current-index").innerText = currentTaskIndex;
}

function toggleSelection(event) {
    const index = event.target.parentNode.dataset.index;
    if (selectedBoxes.includes(index)) {
        selectedBoxes = selectedBoxes.filter(box => box !== index);
        event.target.parentNode.classList.remove('selected');
    } else {
        selectedBoxes.push(index);
        event.target.parentNode.classList.add('selected');
    }
}

document.getElementById("start-task").addEventListener("click", () => {
    currentTaskIndex = 0;
    displayBoxes();
    document.getElementById("start-task").style.display = "none";
    document.getElementById("next-task").style.display = "block";
});

document.getElementById("next-task").addEventListener("click", () => {
    currentTaskIndex++;
    displayBoxes();
});

document.getElementById('submit').addEventListener('click', function() {
    if (selectedBoxes.length === 3) {
        currentTaskIndex++;
        selectedBoxes = [];
        displayBoxes();
    } else {
        const errorMessage = document.getElementById('error-message');
        errorMessage.innerHTML = 'Please select exactly 3 boxes.';
    }
});

window.addEventListener("DOMContentLoaded", () => {
    generateInitialTasks();
});
