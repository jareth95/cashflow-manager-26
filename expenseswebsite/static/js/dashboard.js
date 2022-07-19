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
        },
        
    },
});
}

const getPortfolioData=()=> {
    fetch(`/dashboard/current_portfolio`).then(res=>res.json()).then(results=>{
        
        const portfolioData = results.positions
        const prices = portfolioData.prices
        const amount = portfolioData.amount
        const labels = portfolioData.symbols
        let data = []
        let totalValue = 0

        for(let i=0; i < prices.length; i++){
            let total = Math.round(prices[i]*amount[i])
            data.push(total)
            totalValue += total
        }

        const valueEntry = document.querySelector('#portfolio-total')
        valueEntry.textContent = `Portfolio Total: ${totalValue}`

        renderChart(data, labels, 'myPortfolioChart', 'Current Portfolio')
    })
}
getPortfolioData()


const getExpenseData=()=> {
    fetch(`/dashboard/current_expenses`).then(res=>res.json()).then(results=>{
      
        const expenseData = results.expenses
        const labels = expenseData.names
        const data = expenseData.amounts
       
        let totalValue = 0

        for(let i=0; i < data.length; i++){
            totalValue += data[i]
        }

        const valueEntry = document.querySelector('#expenses-total')
        valueEntry.textContent = ` Total Expenses: ${totalValue}`

        renderChart(data, labels, 'myExpensesChart', 'This months expenses')
    })
}
getExpenseData()

const getIncomeData=()=> {
    fetch(`/dashboard/curent_income`).then(res=>res.json()).then(results=>{
      
        const expenseData = results.incomes
        const labels = expenseData.names
        const data = expenseData.amounts
       
        let totalValue = 0

        for(let i=0; i < data.length; i++){
            totalValue += data[i]
        }

        const valueEntry = document.querySelector('#income-total')
        valueEntry.textContent = ` Total Incomes: ${totalValue}`

        renderChart(data, labels, 'myIncomeChart', 'This months incomes')
    })
}
getIncomeData()