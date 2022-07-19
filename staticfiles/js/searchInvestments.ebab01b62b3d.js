const searchField = document.querySelector('#searchField')
const outputTable = document.querySelector('.table-output')
const appTable = document.querySelector('.app-table')
const paginationContainer = document.querySelector('.pagination-container')
const tableBody = document.querySelector('.table-body')

outputTable.style.display = 'none'

searchField.addEventListener('keyup', (e) => {
    const searchValue = e.target.value

    if (searchValue.trim().length > 0) {
        console.log(searchValue)
        tableBody.innerHTML = ''
        fetch('/search-expenses', {
            body: JSON.stringify({'searchText': searchValue}),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            paginationContainer.style.display = 'none'
            appTable.style.display = 'none'
            outputTable.style.display = 'block'

            if (data.length == 0) {
                outputTable.innerHTML = 'No results found'
            } else {
                data.forEach(item => {
                    console.log(item)
                    tableBody.innerHTML += 
                `<tr>
                <td>${item.name}</td>
                <td>${item.amount}</td>
                <td>${item.exchange}</td>
                <td>${item.buy_price}</td>
                <td>${item.buy_date}</td>
                <td>${item.sell_price}</td>
                <td>${item.sell_date}</td>
                <td>${item.pnl}</td>
                <td><a href="expense-edit/${item.id}" class="btn btn-secondary btn-sm">Edit</a></td>
                <td><a href="expense-delete/${item.id}" class="btn btn-danger btn-sm">Delete</a></td>
                <tr>`
                })
            }
        })
    } else {
        paginationContainer.style.display = 'block'
        appTable.style.display = 'block'
        outputTable.style.display = 'none'
    }
})