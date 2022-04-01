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

const getExpensesData=()=> {
    fetch('/expense_category_summary').then(res=>res.json()).then(results=>{
        
        const categoryData = results.expense_category_data
        const [labels, data] = [Object.keys(categoryData), Object.values(categoryData)]
        const expensesDisplay = document.querySelector('#expenses-total')

        total = 0
        Object.values(categoryData).forEach(number => {
            total += number
        })
        expensesDisplay.textContent = `Expense Total: ${total}`

        renderChart(data, labels, 'myExpensesChart', 'Expenses')
    })
}
const getIncomeData=(month, year)=> {
    fetch(`/income_category_summary/${year}/${month}`).then(res=>res.json()).then(results=>{

        const categoryData = results.income_category_data
        const [labels, data] = [Object.keys(categoryData), Object.values(categoryData)]
        const incomeDisplay = document.querySelector('#income-total')

        total = 0
        Object.values(categoryData).forEach(number => {
            total += number
        })
        incomeDisplay.textContent = `Income Total: ${total}`

        renderChart(data, labels, 'myIncomeChart', 'Income')
    })
}

document.onload=getExpensesData()
document.onload=getIncomeData(12, 2021)
