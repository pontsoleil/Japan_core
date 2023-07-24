/*
function groupByMonth(items) {
    var result = items.reduce(function (r, a) {
        var key = a[0].split('/')[0] + '-' + a[0].split('/')[1]; // assume date is in format dd/mm/yyyy
        r[key] = r[key] || [];
        r[key].push(a);
        return r;
    }, {});

    return Object.values(result);
}
*/
function paginate(items, currentPage, perPage) {
    var start = (currentPage - 1) * perPage;
    return items.slice(start, start + perPage);
}

function groupItemsByMonth(items) {
    var itemsByMonth = {};
    var itemDate;
    var dateString;
    var year = 0, month = 0, day = 0;
    var source = document.querySelector('#source').value;
    for (var i = 0; i < items.length; i++) {
        if ('xbrl-gl' == source) {
            var dateColumn1 = items[i][1];
            var pattern1 = /\d+-(\d{8})-.+/;
            var match1 = dateColumn1.match(pattern1);
            var match2;
            if (match1 && match1[1]) {
                dateString = match1[1];
                year = dateString.slice(0, 4);
                month = dateString.slice(4, 6);
                day = dateString.slice(6, 8);
            } else {
                console.error("Date string is not valid. Year must be >= 1970, Month must be between 1 and 12, and Day must be between 1 and 31.");
            }
        } else if ('hokkaidou-sangyou' == source) {
            var dateColumn2 = items[i][4];
            var pattern2 = /(\d{4})-(\d{2})-(\d{2})/;
            match2 = dateColumn2.match(pattern2);        
            if (match2 && match2[1] && match2[2] && match2[2]) {
                year = match2[1];
                month = match2[2];
                day = match2[3];
            } else {
                console.error("Date string is not valid. Year must be >= 1970, Month must be between 1 and 12, and Day must be between 1 and 31.");
            }
        } else {
            console.error("Input source does not match the expected.");
        }
        if (match1 || match2) {
            if (year >= 1970 && month >= 1 && month <= 12 && day >= 1 && day <= 31) {
                itemDate = new Date(year, month - 1, day);
                console.log(itemDate);
                var yearMonthKey = itemDate.getFullYear() + '-' + (itemDate.getMonth() + 1).toString().padStart(2, '0'); // format as "yyyy-mm"
                if (!itemsByMonth[yearMonthKey]) {
                    itemsByMonth[yearMonthKey] = [];
                }
                itemsByMonth[yearMonthKey].push(items[i]);            
            } else {
                console.error("Date string is not valid. Year must be >= 1970, Month must be between 1 and 12, and Day must be between 1 and 31.");
            }
        } else {
            console.error("Input string does not match the expected pattern.");
        }
    }
    return itemsByMonth;
}

function createTableBodyForMonth(tableSelector, items) {
    // 配列の内容を加工して、HTML要素に追加して表示する
    var tableBody = document.createElement('tbody');
    for (var i = 0; i < items.length; i++) {
        var item = items[i];
        var tr = createTableRow(item);
        tableBody.appendChild(tr);
    }
    var table = document.querySelector(tableSelector);
    table.appendChild(tableBody);
}

function createTableRow(item) {
    // your logic to create a table row
    var tr = document.createElement('tr');
    var td1 = document.createElement('td');
    var td2 = document.createElement('td');
    var td3 = document.createElement('td');
    var td4 = document.createElement('td');
    var td5 = document.createElement('td');
    var td6 = document.createElement('td');
    var td7 = document.createElement('td');
    var td8 = document.createElement('td');
    var td9 = document.createElement('td');
    var td10 = document.createElement('td');
    var td11 = document.createElement('td');
    var td12 = document.createElement('td');
    var td13 = document.createElement('td');
    var td14 = document.createElement('td');
    var td15 = document.createElement('td');
    var td16 = document.createElement('td');
    var td17 = document.createElement('td');
    var td18 = document.createElement('td');
    var td19 = document.createElement('td');
    var td20 = document.createElement('td');
    var td21 = document.createElement('td');
    var td22 = document.createElement('td');
    var td23 = document.createElement('td');
    var td24 = document.createElement('td');
    var td25 = document.createElement('td');
    var td26 = document.createElement('td');
    var td27 = document.createElement('td');
    var td28 = document.createElement('td');
    var td29 = document.createElement('td');
    var td30 = document.createElement('td');
    var td31 = document.createElement('td');
    var td32 = document.createElement('td');
    var td33 = document.createElement('td');
    var td34 = document.createElement('td');
    var td35 = document.createElement('td');
    var td36 = document.createElement('td');
    var td37 = document.createElement('td');
    var td38 = document.createElement('td');
    var td39 = document.createElement('td');
    var td40 = document.createElement('td');
    var td41 = document.createElement('td');
    var td42 = document.createElement('td');

    var source = document.querySelector('#source').value;

    if ('xbrl-gl' == source) {
        td1.textContent = item[0]; td1.classList.add('text-center');
        td2.textContent = item[1]; td2.classList.add('text-center');
        td3.textContent = item[2]; td3.classList.add('text-center');
        td4.textContent = ''; td4.classList.add('text-center');
        td5.textContent = ''; td5.classList.add('text-center');
        td6.textContent = item[3]; td6.classList.add('text-center');
        td7.textContent = item[4]; td7.classList.add('text-center');
        td8.textContent = ''; td8.classList.add('text-center');
        td9.textContent = ''; td9.classList.add('text-center');
        td10.textContent = ''; td10.classList.add('text-center');
        td11.textContent = ''; td11.classList.add('text-left');
        td12.textContent = item[8]; td12.classList.add('text-left');
        td13.textContent = ''; td13.classList.add('text-left');
        td14.textContent = ''; td14.classList.add('text-center');
        td15.textContent = item[15]; td15.classList.add('text-center');
        td16.textContent = ''; td16.classList.add('text-center');
        td17.textContent = ''; td17.classList.add('text-center');
        td18.textContent = ''; td18.classList.add('text-center');
        td19.textContent = item[14]; td19.classList.add('text-left');
        td20.textContent = ''; td20.classList.add('text-center');
        td21.textContent = ''; td21.classList.add('text-center');
        td22.textContent = item[17]; td22.classList.add('text-center');
        td23.textContent = item[18]; td23.classList.add('text-left');
        td24.textContent = item[20]; td24.textContent = formatter.format(item[20]); td24.classList.add('text-right');
        td25.textContent = ''; td25.classList.add('text-center');
        td26.textContent = ''; td26.classList.add('text-center');
        td27.textContent = ''; td27.classList.add('text-left');
        td28.textContent = item[21]; td28.classList.add('text-left');
        td29.textContent = ''; td29.classList.add('text-center');
        td30.textContent = item[23]; td30.classList.add('text-left');
        td31.textContent = item[24]; td31.classList.add('text-center');
        td32.textContent = item[25]; td32.classList.add('text-left');
        td33.textContent = item[27]; td33.textContent = formatter.format(item[27]); td33.classList.add('text-right');
        td34.textContent = ''; td34.classList.add('text-center');
        td35.textContent = ''; td35.classList.add('text-center');
        td36.textContent = ''; td36.classList.add('text-left');
        td37.textContent = item[28]; td37.classList.add('text-left');
        td38.textContent = ''; td38.classList.add('text-center');
        td39.textContent = item[30]; td39.classList.add('text-left');
        td40.textContent = item[31]; td40.classList.add('text-left');
        td41.textContent = ''; td41.classList.add('text-center');
        td42.textContent = item[33]; td42.classList.add('text-left');
    } else if ('hokkaidou-sangyou' == source) {
        td1.textContent = item[0]; td1.classList.add('text-center');
        td2.textContent = item[1]; td2.classList.add('text-center');
        td3.textContent = item[2]; td3.classList.add('text-center');
        td4.textContent = item[3]; td4.classList.add('text-center');
        td5.textContent = item[4]; td5.classList.add('text-center');
        td6.textContent = item[5]; td6.classList.add('text-center');
        td7.textContent = item[6]; td7.classList.add('text-center');
        td8.textContent = item[7]; td8.classList.add('text-center');
        td9.textContent = item[8]; td9.classList.add('text-center');
        td10.textContent = item[9]; td10.classList.add('text-center');
        td11.textContent = item[10]; td11.classList.add('text-left');
        td12.textContent = item[12]; td12.classList.add('text-left');
        td13.textContent = item[13]; td13.classList.add('text-left');
        td14.textContent = item[15]; td14.classList.add('text-center');
        td15.textContent = item[16]; td15.classList.add('text-center');
        td16.textContent = item[17]; td16.classList.add('text-center');
        td17.textContent = item[18]; td17.classList.add('text-center');
        td18.textContent = item[19]; td18.classList.add('text-center');
        td19.textContent = item[20]; td19.classList.add('text-left');
        td20.textContent = item[21]; td20.classList.add('text-center');
        td21.textContent = item[22]; td21.classList.add('text-center');
        td22.textContent = item[23]; td22.classList.add('text-center');
        td23.textContent = item[24]; td23.classList.add('text-left');
        td24.textContent = item[26]; td24.textContent = formatter.format(item[26]); td24.classList.add('text-right');
        td25.textContent = item[28]; td25.classList.add('text-center');
        td26.textContent = item[29]; td26.classList.add('text-center');
        td27.textContent = item[30]; td27.classList.add('text-left');
        td28.textContent = item[31]; td28.classList.add('text-left');
        td29.textContent = item[32]; td29.classList.add('text-center');
        td30.textContent = item[33]; td30.classList.add('text-left');
        td31.textContent = item[34]; td31.classList.add('text-center');
        td32.textContent = item[35]; td32.classList.add('text-left');
        td33.textContent = item[37]; td33.textContent = formatter.format(item[37]); td33.classList.add('text-right');
        td34.textContent = item[39]; td34.classList.add('text-center');
        td35.textContent = item[40]; td35.classList.add('text-center');
        td36.textContent = item[41]; td36.classList.add('text-left');
        td37.textContent = item[42]; td37.classList.add('text-left');
        td38.textContent = item[43]; td38.classList.add('text-center');
        td39.textContent = item[44]; td39.classList.add('text-left');
        td40.textContent = item[45]; td40.classList.add('text-left');
        td41.textContent = item[46]; td41.classList.add('text-center');
        td42.textContent = item[47]; td42.classList.add('text-left');
    }

    tr.appendChild(td1);
    tr.appendChild(td2);
    tr.appendChild(td3);
    tr.appendChild(td4);
    tr.appendChild(td5);
    tr.appendChild(td6);
    tr.appendChild(td7);
    tr.appendChild(td8);
    tr.appendChild(td9);
    tr.appendChild(td10);
    tr.appendChild(td11);
    tr.appendChild(td12);
    tr.appendChild(td13);
    tr.appendChild(td14);
    tr.appendChild(td15);
    tr.appendChild(td16);
    tr.appendChild(td17);
    tr.appendChild(td18);
    tr.appendChild(td19);
    tr.appendChild(td20);
    tr.appendChild(td11);
    tr.appendChild(td12);
    tr.appendChild(td13);
    tr.appendChild(td14);
    tr.appendChild(td15);
    tr.appendChild(td16);
    tr.appendChild(td17);
    tr.appendChild(td18);
    tr.appendChild(td19);
    tr.appendChild(td20);
    tr.appendChild(td21);
    tr.appendChild(td22);
    tr.appendChild(td23);
    tr.appendChild(td24);
    tr.appendChild(td25);
    tr.appendChild(td26);
    tr.appendChild(td27);
    tr.appendChild(td28);
    tr.appendChild(td29);
    tr.appendChild(td30);
    tr.appendChild(td31);
    tr.appendChild(td32);
    tr.appendChild(td33);
    tr.appendChild(td34);
    tr.appendChild(td35);
    tr.appendChild(td36);
    tr.appendChild(td37);
    tr.appendChild(td38);
    tr.appendChild(td39);
    tr.appendChild(td40);
    tr.appendChild(td41);
    tr.appendChild(td42);

    return tr;
}

function getHorizontal() {
    snackbar.close();
    snackbar.open({ 'message': '<i class="fa fa-cog fa-spin"></i>仕訳日記帳 読み込み中', 'type': 'info' });
    document.querySelector('#horizontal tbody').innerHTML = '';
    // XMLHttpRequestオブジェクトを使用して、CSVファイルを取得する
    var xhr = new XMLHttpRequest();
    var url = getBase() + 'horizontal_ledger.csv';
    xhr.open('GET', url, true);
    xhr.onload = function () {
        // 取得したCSVデータをパースして、JavaScriptの配列に変換する
        var data = xhr.responseText.split('\n');
        var items = [];
        for (var i = 0; i < data.length; i++) {
            var item = parseCSV(data[i]);
            items.push(item);
        }
        var items_count = items.length;
        snackbar.close();
        snackbar.open({ 'message': '<i class="fa fa-cog fa-spin"></i>仕訳日記帳 ' + items_count + ' 件 読み込み中', 'type': 'info' });
        // // grouping items by month
        // var monthlyItems = groupByMonth(items);
        // // set the current page
        // var currentPage = 1;
        // // get the items for the current page
        // var currentItems = paginate(monthlyItems, currentPage, 1); // display one month per page

        // // ... continue your code by replacing 'items' with 'currentItems' where necessary ...




        // Group the items by month
        var itemsByMonth = groupItemsByMonth(items);

        // // Process each month separately
        // var monthKeys = Object.keys(itemsByMonth);

        var currentPage = 1;
        // get the items for the current page
        var currentItems = paginate(itemsByMonth, currentPage, 1); // display one month per page
        createTableBodyForMonth('#horizontal', monthItems);

        // for (var m = 0; m < monthKeys.length; m++) {
        //     var monthItems = itemsByMonth[monthKeys[m]];
        //     createTableBodyForMonth('#horizontal', monthItems);
        // }

        setTimeout(function () {
            snackbar.close();
        }, 3000);

        hideHolizontalLines();
    };
    xhr.send();
}