// main.js
var csvUrl = 'https://example.com/data.csv';
var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var csvData = xhr.responseText;
        var rows = csvData.split('\n').map(function(row) {
            return row.split(',');
        });
        var table = document.getElementById('csv-table');
        var tbody = table.querySelector('tbody');
        rows.forEach(function(row) {
            var tr = document.createElement('tr');
            row.forEach(function(cell) {
                var td = document.createElement('td');
                td.textContent = cell;
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
    }
};
xhr.open('GET', csvUrl, true);
xhr.send();
