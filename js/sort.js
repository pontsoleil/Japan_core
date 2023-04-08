let table = document.querySelector('table');
let rows = table.rows;
let rowsArray = Array.from(rows);
rowsArray.sort(function (rowA, rowB) {
    let ageA = parseInt(rowA.cells[1].textContent);
    let ageB = parseInt(rowB.cells[1].textContent);
    return ageA - ageB;
});
table.tBodies[0].innerHTML = '';
rowsArray.forEach(function (row) {
    table.tBodies[0].appendChild(row);
});