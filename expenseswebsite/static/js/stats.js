const renderChart =(data, labels, chartName, title)=> {
    const ctx = document.getElementById(chartName).getContext('2d');
    console.log(data)
    console.log(labels)
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

const getExpensesData=(month, year)=> {
    fetch(`/expense_category_summary/${year}/${month}`).then(res=>res.json()).then(results=>{
        
        const categoryData = results.expense_category_data
        const [labels, data] = [Object.keys(categoryData), Object.values(categoryData)]
        const expensesDisplay = document.querySelector('#expenses-total')

        total = 0
        Object.values(categoryData).forEach(number => {
            total += number
        })
        expensesDisplay.textContent = `Expense Total: ${total}`

        if (total == 0) {
            const chart = document.getElementById('expenses-total')
            chart.innerHTML = 'No cashflow data for selected date'      
        } 
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

        if (total == 0) {
            const chart = document.getElementById('income-total')
            chart.innerHTML = 'No cashflow data for selected date'
        }
        renderChart(data, labels, 'myIncomeChart', 'Income')
    })
}


const months = document.querySelectorAll('.month')
const years = document.querySelectorAll('.year')

for (let i=0; i<years.length; i++) {
    years[i].addEventListener('click', ()=> {
        let selectedYear = parseInt(years[i].textContent)
        let selectedMonth = 0

        for (let x=0; x<years.length; x++) {
            if (years[x].classList.contains('btn-success')) {
                years[x].classList.remove('btn-success')
                years[x].classList.add('btn-secondary')
            }
        }
        years[i].classList.remove('btn-secondary')
        years[i].classList.add('btn-success')

        months.forEach(month => {
            if(month.classList.contains('btn-success')) {
                selectedMonth = new Date(Date. parse(month.textContent +" 1, 2012")). getMonth()+1
            }
        })
        getIncomeData(selectedMonth, selectedYear)
        getExpensesData(selectedMonth, selectedYear)
    })
}

for (let x=0; x<months.length; x++) {
    months[x].addEventListener('click', ()=> {
        const selectedMonth = months[x].textContent
        let selectedYear = 0

        for (let i=0; i<months.length; i++) {
            if (months[i].classList.contains('btn-success')) {
                months[i].classList.remove('btn-success')
                months[i].classList.add('btn-secondary')
            }
        }
        months[x].classList.remove('btn-secondary')
        months[x].classList.add('btn-success')
       
        let month = new Date(Date. parse(selectedMonth +" 1, 2012")). getMonth()+1

        years.forEach(year => {
            if(year.classList.contains('btn-success')) {
                selectedYear = parseInt(year.textContent)
            }
        })

        getIncomeData(month, selectedYear)
        getExpensesData(month, selectedYear)
    })
}


