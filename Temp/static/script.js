// Example static dataset
const data = {
    labels: ["January", "February", "March", "April", "May", "June"],
    datasets: [{
        label: 'Dataset 1',
        data: [65, 59, 80, 81, 56, 55], // Replace this with your dataset
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1
    }]
};

// Function to render bar chart
function renderBarChart() {
    const ctx = document.getElementById('barChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Function to render line chart
function renderLineChart() {
    const ctx = document.getElementById('lineChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}