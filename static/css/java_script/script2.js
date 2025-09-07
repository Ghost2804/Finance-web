async function fetchStockData() {
    try {
        let response = await fetch('/stock-data');  
        let data = await response.json();
        let table = document.getElementById("stock-table");
        table.innerHTML = "";  // Clear old data before updating

        for (let stock in data) {
            let row = document.createElement("tr");
            row.innerHTML = `
                <td>${data[stock].name}</td>
                <td>$${data[stock].price.toFixed(2)}</td>
                <td class="${data[stock].change >= 0 ? 'green' : 'red'}">
                    ${data[stock].change.toFixed(2)}
                </td>
                <td class="${data[stock].change >= 0 ? 'green' : 'red'}">
                    ${data[stock].change_percent.toFixed(2)}%
                </td>
            `;
            table.appendChild(row);
        }
    } catch (error) {
        console.error("Error fetching stock data:", error);
    }
}

// Auto-refresh stock data every 5 seconds
setInterval(fetchStockData, 5000);
