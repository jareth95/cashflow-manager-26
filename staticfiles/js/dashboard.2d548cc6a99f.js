const renderChart =(data, labels, chartName, title)=> {
    const ctx = document.getElementById(chartName).getContext('2d');
    const myChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: labels,
        datasets: [{
            label: '',
            data: data,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        title: {
            display:true,
            text: title,
        }
    },
});
}

renderChart(data, labels, 'myExpensesChart', 'This Months Expenses')
renderChart(data, labels, 'myIncomesChart', 'This Months Incomes')