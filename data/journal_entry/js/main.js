/**
 * main.js
 * 
 * designed by SAMBUICHI, Nobuyuki (Sambuichi Professional Engineers Office)
 * written by SAMBUICHI, Nobuyuki (Sambuichi Professional Engineers Office)
 * 
 * MIT License
 * 
 * (c) 2023 SAMBUICHI Nobuyuki (Sambuichi Professional Engineers Office)
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */
main = (function () {

    const formatter = new Intl.NumberFormat('ja-JP');

    function getBase() {
        var source = document.querySelector('#source').value;
        var base;
        if ('xbrl-gl' == source) {
            base = '';
        } else if ('hokkaidou-sangyou' == source) {
            base = 'data/hokkaidou-sangyou/';
        }
        return base;
    }

    function parseCSV(data) {
        var items = [];
        var field = "";
        var isInQuotes = false;
        for (var i = 0; i < data.length; i++) {
            var char = data[i];
            if (char === ',') {
                if (isInQuotes) {
                    field += char;
                } else {
                    items.push(field);
                    field = "";
                }
            } else if (char === '"') {
                if (isInQuotes && data[i + 1] === '"') {
                    field += char;
                    i++; // Skip the next double quote
                } else {
                    isInQuotes = !isInQuotes;
                }
            } else {
                field += char;
            }
        }
        items.push(field); // Add the last field
        return items;
    }

    function getHorizontal() {
        snackbar.close();
        snackbar.open({ 'message': '<i class="fa fa-cog fa-spin"></i> 読み込み中', 'type': 'info' });
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
            snackbar.open({ 'message': '<i class="fa fa-cog fa-spin"></i> ' + items_count + ' 件読み込み中', 'type': 'info' });

            // 配列の内容を加工して、HTML要素に追加して表示する
            var tableBody = document.querySelector('#horizontal tbody');
            tableBody.innerHTML = '';
            for (var i = 1; i < items.length; i++) {
                if (0 == i % 500) {
                    snackbar.close();
                    snackbar.open({ 'message': '<i class="fa fa-cog fa-spin"></i> 1' + i + ' / ' + items_count + ' 件読み込み中', 'type': 'info' });
                }
                var item = items[i];
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

                tableBody.appendChild(tr);
            }

            setTimeout(function () {
                snackbar.close();
            }, 3000);

            hideHolizontalLines();
        };
        xhr.send();
    }

    function hideHolizontalLines() {
        var thead = document.querySelector('#horizontal thead');
        var row = thead.rows[0];
        console.log(row);
        row.cells[3].style.display = 'none';
        row.cells[4].style.display = 'none';
        row.cells[5].style.display = 'none';
        row.cells[6].style.display = 'none';
        row.cells[7].style.display = 'none';
        row.cells[8].style.display = 'none';
        row.cells[9].style.display = 'none';
        row.cells[10].style.display = 'none';
        row.cells[11].style.display = 'none';
        row.cells[12].style.display = 'none';
        row.cells[13].style.display = 'none';
        row.cells[14].style.display = 'none';
        row.cells[17].style.display = 'none';
        row.cells[19].style.display = 'none';
        row.cells[20].style.display = 'none';
        row.cells[27].style.display = 'none';
        row.cells[28].style.display = 'none';
        row.cells[29].style.display = 'none';
        row.cells[36].style.display = 'none';
        row.cells[37].style.display = 'none';
        row.cells[38].style.display = 'none';
        row.cells[39].style.display = 'none';
        row.cells[40].style.display = 'none';
        row.cells[41].style.display = 'none';

        // tbody要素を取得する
        var tbody = document.querySelector('#horizontal tbody');
        // tbody要素内のtr要素を順番に取得する
        for (var i = 0; i < tbody.rows.length; i++) {
            // 各tr要素内のn番目のtd要素を取得する（ここでは3番目から）
            var td2 = tbody.rows[i].cells[2];
            var td3 = tbody.rows[i].cells[3];
            // 取得したtd要素が空かどうかを判定し、空であればtr要素を非表示にする
            if ('' == td2.textContent.trim() || '' != td3.textContent.trim()) {
                tbody.rows[i].style.display = 'none';
            }
        }
        for (i = 0; i < tbody.rows.length; i++) {
            row = tbody.rows[i];
            row.cells[3].style.display = 'none';
            row.cells[4].style.display = 'none';
            row.cells[5].style.display = 'none';
            row.cells[6].style.display = 'none';
            row.cells[7].style.display = 'none';
            row.cells[8].style.display = 'none';
            row.cells[9].style.display = 'none';
            row.cells[10].style.display = 'none';
            row.cells[11].style.display = 'none';
            row.cells[12].style.display = 'none';
            row.cells[13].style.display = 'none';
            row.cells[14].style.display = 'none';
            row.cells[17].style.display = 'none';
            row.cells[19].style.display = 'none';
            row.cells[20].style.display = 'none';
            row.cells[27].style.display = 'none';
            row.cells[28].style.display = 'none';
            row.cells[29].style.display = 'none';
            row.cells[36].style.display = 'none';
            row.cells[37].style.display = 'none';
            row.cells[38].style.display = 'none';
            row.cells[39].style.display = 'none';
            row.cells[40].style.display = 'none';
            row.cells[41].style.display = 'none';
        }
    }

    function showHolizontalLines() {
        var thead = document.querySelector('#horizontal thead');
        var row = thead.rows[0];
        row.cells[3].style.display = '';
        row.cells[4].style.display = '';
        row.cells[5].style.display = '';
        row.cells[6].style.display = '';
        row.cells[7].style.display = '';
        row.cells[8].style.display = '';
        row.cells[9].style.display = '';
        row.cells[10].style.display = '';
        row.cells[11].style.display = '';
        row.cells[12].style.display = '';
        row.cells[13].style.display = '';
        row.cells[14].style.display = '';
        row.cells[17].style.display = '';
        row.cells[19].style.display = '';
        row.cells[20].style.display = '';
        row.cells[27].style.display = '';
        row.cells[28].style.display = '';
        row.cells[29].style.display = '';
        row.cells[36].style.display = '';
        row.cells[37].style.display = '';
        row.cells[38].style.display = '';
        row.cells[39].style.display = '';
        row.cells[40].style.display = '';
        row.cells[41].style.display = '';

        // tbody要素を取得する
        var tbody = document.querySelector('#horizontal tbody');
        // tbody要素内のtr要素を順番に取得する
        for (var i = 0; i < tbody.rows.length; i++) {
            // 取得したtd要素が空かどうかを判定し、空であればtr要素を非表示にする
            row = tbody.rows[i];
            row.style.display = '';
            row.cells[3].style.display = '';
            row.cells[4].style.display = '';
            row.cells[5].style.display = '';
            row.cells[6].style.display = '';
            row.cells[7].style.display = '';
            row.cells[8].style.display = '';
            row.cells[9].style.display = '';
            row.cells[10].style.display = '';
            row.cells[11].style.display = '';
            row.cells[12].style.display = '';
            row.cells[13].style.display = '';
            row.cells[14].style.display = '';
            row.cells[17].style.display = '';
            row.cells[19].style.display = '';
            row.cells[20].style.display = '';
            row.cells[27].style.display = '';
            row.cells[28].style.display = '';
            row.cells[29].style.display = '';
            row.cells[36].style.display = '';
            row.cells[37].style.display = '';
            row.cells[38].style.display = '';
            row.cells[39].style.display = '';
            row.cells[40].style.display = '';
            row.cells[41].style.display = '';
        }
    }

    function getGL(file) {
        // XMLHttpRequestオブジェクトを使用して、CSVファイルを取得する
        var xhr = new XMLHttpRequest();
        url = getBase() + 'GL/' + file;
        xhr.open('GET', url, true);
        xhr.onload = function () {
            // 取得したCSVデータをパースして、JavaScriptの配列に変換する
            var data = xhr.responseText.split('\n');
            var items = [];
            for (var i = 0; i < data.length; i++) {
                var item = parseCSV(data[i]);
                if (item.length < 10) {
                    continue
                }
                item = item.map((element) => element.trim());
                items.push(item);
            }
            var items_count = items.length;
            snackbar.close();
            snackbar.open({ 'message': '<i class="fa fa-cog fa-spin"></i> ' + items_count + ' 件読み込み中', 'type': 'info' });
            // 配列の内容を加工して、HTML要素に追加して表示する
            var tableBody = document.querySelector('#GL tbody');
            tableBody.innerHTML = '';
            for (var i = 1; i < items.length; i++) {
                var item = items[i];
                if (0 == i % 500) {
                    snackbar.close();
                    snackbar.open({ 'message': '<i class="fa fa-cog fa-spin"></i> 1' + i + ' / ' + items_count + ' 件読み込み中', 'type': 'info' });
                }
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
                /*
                1 num
                2 GL02
                3 GL02-GL55
                4 date
                5 contra_acct
                6 contra_acct_name
                7 note
                8 dbt_amount
                9 dbt_tax_code
                10 dbt_tax_rate
                11 dbt_tax_desc
                12 cdt_amount
                13 cdt_tax_code
                14 cdt_tax_rate
                15 cdt_tax_desc
                16 balance
                */
                /*
                1 num
                2 GL02
                3 GL02-GL55
                4 date
                5 contra_account
                6 contra_account_name
                7 note
                8 debit_amount
                9 credit_amount
                10 balance
                */
                var source = document.querySelector('#source').value;

                td1.textContent = item[0]; td1.classList.add('text-right');
                td2.textContent = item[1]; td2.classList.add('text-center');
                td3.textContent = item[2]; td3.classList.add('text-center');
                td4.textContent = item[3]; td4.classList.add('text-left');
                td5.textContent = item[4]; td5.classList.add('text-center');
                td6.textContent = item[5]; td6.classList.add('text-left');
                td7.textContent = item[6]; td7.classList.add('text-left');
                td8.textContent = item[1].length > 0
                    ? formatter.format(item[7])
                    : /^[0-9]+$/.test(item[7]) ? formatter.format(item[7]) : '';
                td8.classList.add('text-right');
                if ('xbrl-gl' == source) {
                    td9.textContent = '';
                    td10.textContent = '';
                    td11.textContent = '';
                    td12.textContent = item[1].length > 0
                        ? formatter.format(item[8])
                        : /^[0-9]+$/.test(item[8]) ? formatter.format(item[8]) : '';
                    td12.classList.add('text-right');
                    td13.textContent = '';
                    td14.textContent = '';
                    td15.textContent = '';
                    td16.textContent = item[1].length > 0
                        ? formatter.format(item[9])
                        : /^[0-9]+$/.test(item[9]) ? formatter.format(item[9]) : '';
                    td16.classList.add('text-right');
                } else if ('hokkaidou-sangyou' == source) {
                    td9.textContent = item[8]; td3.classList.add('text-center');
                    td10.textContent = item[9]; td3.classList.add('text-center');
                    td11.textContent = item[10]; td3.classList.add('text-center');
                    td12.textContent = item[1].length > 0
                        ? formatter.format(item[11])
                        : /^[0-9]+$/.test(item[11]) ? formatter.format(item[11]) : '';
                    td12.classList.add('text-right');
                    td13.textContent = item[12]; td3.classList.add('text-center');
                    td14.textContent = item[13]; td3.classList.add('text-center');
                    td15.textContent = item[14]; td3.classList.add('text-center');
                    td16.textContent = item[1].length > 0
                        ? formatter.format(item[15])
                        : /^[0-9]+$/.test(item[15]) ? formatter.format(item[15]) : '';
                    td16.classList.add('text-right');
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

                tableBody.appendChild(tr);
            }
            snackbar.close();
        };
        xhr.send();
    }

    function getTB(month) {
        // XMLHttpRequestオブジェクトを使用して、CSVファイルを取得する
        var xhr = new XMLHttpRequest();
        url = getBase() + 'TB/' + month + 'trial_balance.csv';
        xhr.open('GET', url, true);
        xhr.onload = function () {
            // 取得したCSVデータをパースして、JavaScriptの配列に変換する
            var data = xhr.responseText.split('\n');
            var items = [];
            for (var i = 0; i < data.length; i++) {
                var item = parseCSV(data[i]);
                if (item.length < 7) {
                    continue
                }
                item = item.map((element) => element.trim());
                items.push(item);
            }
            var items_count = items.length;
            snackbar.close();
            snackbar.open({ 'message': '<i class="fa fa-cog fa-spin"></i> ' + items_count + ' 件読み込み中', 'type': 'info' });
            // 配列の内容を加工して、HTML要素に追加して表示する
            var tableBody = document.querySelector('#TB tbody');
            tableBody.innerHTML = '';
            for (var i = 1; i < items.length; i++) {
                var item = items[i];
                if (0 == i % 500) {
                    snackbar.close();
                    snackbar.open({ 'message': '<i class="fa fa-cog fa-spin"></i> 1' + i + ' / ' + items_count + ' 件読み込み中', 'type': 'info' });
                }
                var tr = document.createElement('tr');
                var td1 = document.createElement('td');
                var td2 = document.createElement('td');
                var td3 = document.createElement('td');
                var td4 = document.createElement('td');
                var td5 = document.createElement('td');
                var td6 = document.createElement('td');
                var td7 = document.createElement('td');
                /*
                month
                account_code
                account_name
                beginning_balance
                debit_amount
                credit_amount
                ending_balance
                */
                td1.textContent = item[0]; td2.classList.add('text-center');
                td2.textContent = item[1].length > 0 ? item[1] : '＊＊合計＊＊';
                td2.classList.add('text-center');
                td3.textContent = item[2]; td3.classList.add('text-left');
                td4.textContent = item[1].length > 0
                    ? formatter.format(item[3])
                    : /^[0-9]+$/.test(item[3]) ? formatter.format(item[3]) : '';
                td4.classList.add('text-right');
                td5.textContent = item[1].length > 0
                    ? formatter.format(item[4])
                    : /^[0-9]+$/.test(item[4]) ? formatter.format(item[4]) : '';
                td5.classList.add('text-right');
                td6.textContent = item[1].length > 0
                    ? formatter.format(item[5])
                    : /^[0-9]+$/.test(item[5]) ? formatter.format(item[5]) : '';
                td6.classList.add('text-right');
                td7.textContent = item[1].length > 0
                    ? formatter.format(item[6])
                    : /^[0-9]+$/.test(item[6]) ? formatter.format(item[6]) : '';
                td7.classList.add('text-right');
                tr.appendChild(td1);
                tr.appendChild(td2);
                tr.appendChild(td3);
                tr.appendChild(td4);
                tr.appendChild(td5);
                tr.appendChild(td6);
                tr.appendChild(td7);
                tableBody.appendChild(tr);
            }
            snackbar.close();
        };
        xhr.send();
    }

    function getGLlist() {
        var source = document.querySelector('#source').value;
        var url;
        if ('xbrl-gl' == source) {
            url = './file_GL_list.php';
        } else if ('hokkaidou-sangyou' == source) {
            url = './file_GL_hokkaidou-sangyou_list.php';
        } else {
            return
        }
        fetch(url)
            .then(response => response.json())
            .then(data => {
                var select = $('#selectGL');
                select.empty();
                for (var i = 0; i < Object.keys(data).length; i++) {
                    var value = Object.values(data)[i];
                    var name = value.substring(0, value.length - 4)
                    var option = $('<option></option>').text(name).val(value);
                    select.append(option);
                }
                select.on('change', function () {
                    const selected = event.target.value;
                    getGL(selected);
                });
            })
            .catch(error => {
                console.error('エラー: 総勘定元帳一覧が取得できません', error);
                alert('エラー: 総勘定元帳一覧が取得できません');
            });
    }

    function getTBlist() {
        var source = document.querySelector('#source').value;
        var url;
        if ('xbrl-gl' == source) {
            url = './file_TB_list.php';
        } else if ('hokkaidou-sangyou' == source) {
            url = './file_TB_hokkaidou-sangyou_list.php';
        } else {
            return
        }
        fetch(url)
            .then(response => response.json())
            .then(data => {
                var select = $('#selectTB');
                select.empty();
                for (var i = 0; i < Object.keys(data).length; i++) {
                    var value = Object.values(data)[i];
                    var month = value.substring(0, 7);
                    var option = $('<option></option>').text(month).val(month);
                    select.append(option);
                }
                select.on('change', function () {
                    const selected = event.target.value;
                    getTB(selected);
                });
            })
            .catch(error => {
                console.error('エラー: 残高試算表一覧が取得できません', error);
                alert('エラー: 残高試算表一覧が取得できません');
            });
    }

    function getInstances() {
        snackbar.close()
        snackbar.open({ 'message': '<i class="fa fa-cog fa-spin"></i> Tidy Data (xBRL-CSV) 読み込み中', 'type': 'info' });
        // XMLHttpRequestオブジェクトを使用して、CSVファイルを取得する
        var xhr = new XMLHttpRequest();
        var url = getBase() + 'instances.csv'
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
            snackbar.close()
            snackbar.open({ 'message': '<i class="fa fa-cog fa-spin"></i> ' + items_count + ' 件読み込み中', 'type': 'info' });
            // 配列の内容を加工して、HTML要素に追加して表示する
            var tableBody = document.querySelector('#instances tbody');
            tableBody.innerHTML = '';
            for (var i = 1; i < items.length; i++) {
                if (0 == i % 500) {
                    snackbar.close();
                    snackbar.open({ 'message': '<i class="fa fa-cog fa-spin"></i> 1' + i + ' / ' + items_count + ' 件読み込み中', 'type': 'info' });
                }
                var item = items[i];
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
                // 1	c GL
                // 2	c GL詳細
                // 3	l ソース説明
                // 4	c 作成日
                // 5	c 明細行番号
                // 6	c 記帳日
                // 7	c 伝票日付
                // 8	l 摘要
                // 9	c 借方/貸方
                // 10	c 勘定科目番号
                // 11	l 勘定科目名
                // 12	r f 金額
                // 13	c セグメント
                // 14	l セグメント名
                // 15	c 税コード
                // 16	c 税率
                // 17	l 税コード説明
                // 18	c 事業セグメント
                // 19	l 名称
                var source = document.querySelector('#source').value;
                if ('hokkaidou-sangyou' == source) {
                    td1.textContent = item[0]; td1.classList.add('text-center');
                    td2.textContent = item[1]; td2.classList.add('text-center');
                    td3.textContent = item[7]; td3.classList.add('text-left');
                    td4.textContent = item[11]; td4.classList.add('text-center');
                    td5.textContent = item[12]; td5.classList.add('text-center');
                    td6.textContent = '';
                    td7.textContent = item[13]; td7.classList.add('text-center');
                    td8.textContent = item[15]; td8.classList.add('text-left');
                    td9.textContent = item[16]; td9.classList.add('text-center');
                    td10.textContent = item[19]; td10.classList.add('text-center');
                    td11.textContent = item[20]; td11.classList.add('text-left');
                    td12.textContent = formatter.format(item[21]); td12.classList.add('text-right');
                    td13.textContent = item[22]; td13.classList.add('text-center');
                    td14.textContent = item[23]; td14.classList.add('text-center');
                    td15.textContent = item[25]; td15.classList.add('text-center');
                    td16.textContent = item[26]; td16.classList.add('text-center');
                    td17.textContent = item[27]; td17.classList.add('text-left');
                    td18.textContent = '';
                    td19.textContent = '';
                } else if ('xbrl-gl' == source) {
                    td1.textContent = item[0]; td1.classList.add('text-center');
                    td2.textContent = item[1]; td2.classList.add('text-center');
                    td3.textContent = item[6]; td3.classList.add('text-left');
                    td4.textContent = '';
                    td5.textContent = '';
                    td6.textContent = item[19]; td6.classList.add('text-center');
                    td7.textContent = '';
                    td8.textContent = item[12]; td8.classList.add('text-left');
                    td9.textContent = item[13]; td9.classList.add('text-center');
                    td10.textContent = item[14]; td10.classList.add('text-center');
                    td11.textContent = item[15]; td11.classList.add('text-left');
                    td12.textContent = formatter.format(item[17]); td12.classList.add('text-right');
                    td13.textContent = item[20]; td13.classList.add('text-center');
                    td14.textContent = item[22]; td14.classList.add('text-left');
                    td15.textContent = '';
                    td16.textContent = '';
                    td17.textContent = '';
                    td18.textContent = item[23]; td18.classList.add('text-center');
                    td19.textContent = item[25]; td19.classList.add('text-left');
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

                tableBody.appendChild(tr);
            }
            snackbar.close();
        };
        xhr.send();
    }

    function getEPSON() {
        snackbar.close()
        snackbar.open({ 'message': '<i class="fa fa-cog fa-spin"></i> EPSON R4 読み込み中', 'type': 'info' });
        // XMLHttpRequestオブジェクトを使用して、CSVファイルを取得する
        var xhr = new XMLHttpRequest();
        var url = 'data/hokkaidou-sangyou/hokkaidou-sangyou.csv'
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
            snackbar.close()
            snackbar.open({ 'message': '<i class="fa fa-cog fa-spin"></i> ' + items_count + ' 件読み込み中', 'type': 'info' });
            // 配列の内容を加工して、HTML要素に追加して表示する
            var tableBody = document.querySelector('#EPSON-R4 tbody');
            tableBody.innerHTML = '';
            for (var i = 1; i < items.length; i++) {
                if (0 == i % 500) {
                    snackbar.close();
                    snackbar.open({ 'message': '<i class="fa fa-cog fa-spin"></i> 1' + i + ' / ' + items_count + ' 件読み込み中', 'type': 'info' });
                }
                var item = items[i];
                var tr = document.createElement('tr');
                for (var j = 0; j <= item.length; j++) {
                    var td = document.createElement('td');
                    td.textContent = item[j];
                    tr.appendChild(td);
                }
                tableBody.appendChild(tr);
            }
            snackbar.close();
        };
        xhr.send();
    }

    function getFileList() {
        fetch('./file_list.php')
            .then(response => response.json())
            .then(data => {
                var file_list = $('#file-list');
                var select = $('<select id="file-select"></select>');
                for (var i = 0; i < Object.keys(data).length; i++) {
                    var value = Object.values(data)[i];
                    var option = $('<option></option>').text(value).val(value);
                    select.append(option);
                }
                file_list.append(select);

                var fileName = document.getElementById("file-select").value;
                getXMLFile(fileName);

                select.on('change', function () {
                    var fileName = $(this).val();
                    getXMLFile(fileName);
                });
            })
            .catch(error => {
                console.error('エラー: ファイル一覧が取得できません', error);
                alert('エラー: ファイル一覧が取得できません');
            });
    }

    // xmlファイルの内容を表示
    function getXMLFile(fileName) {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "./XBRL_GLinstances/" + fileName, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                let xmlText = xhr.responseText;
                xmlText = xmlText.replace(/\n[ ]+\n[ ]+/g, '');
                const escapedXmlString = escapeHtml(xmlText);
                var contentDiv = document.getElementById("file-content");
                contentDiv.innerHTML = escapedXmlString;// `<pre>${formattedXml}</pre>`;
                // let xmlData = xhr.responseXML;
                // // XMLデータを文字列に変換する
                // let wellFormedXml = new XMLSerializer().serializeToString(xmlData);
                // // HTMLエスケープする
                // const escapedXmlString = escapeHtml(wellFormedXml);
                // var contentDiv = document.getElementById("file-content");
                // contentDiv.innerHTML = escapedXmlString;// `<pre>${formattedXml}</pre>`;
            }
        };
        xhr.send();
    }

    // HTMLエスケープする関数
    function escapeHtml(unsafe) {
        return unsafe.replace(/[&<"']/g, function (match) {
            switch (match) {
                case '&':
                    return '&amp;';
                case '<':
                    return '&lt;';
                case '"':
                    return '&quot;';
                default:
                    return '&#039;';
            }
        });
    }

    function initModule() {
        snackbar.open({ 'message': '<i class="fa fa-cog fa-spin"></i> 読み込み中', 'type': 'info' });

        $('#nav_horizontal').on('click', function () {
            getHorizontal();
        });

        $('#nav_GL').on('click', function () {
            let sourceSelect = document.querySelector('#source');
            var source = sourceSelect.value;
            getGLlist();
            if ('xbrl-gl' == source) {
                getGL('111現金.csv');
            } else if ('hokkaidou-sangyou' == source) {
                getGL('100現金.csv')
            }
        });

        $('#nav_TB').on('click', function () {
            let sourceSelect = document.querySelector('#source');
            var source = sourceSelect.value;
            getTBlist();
            if ('xbrl-gl' == source) {
                getTB('2009-04');
            } else if ('hokkaidou-sangyou' == source) {
                getTB('2022-07');
            }
        });

        $('#nav_tidy').on('click', function () {
            getInstances();
        });

        var linesButton = $('#linesButton');
        linesButton.value = '明細行のみ';
        var isEnabled = false; // 初期状態では処理を無効にする

        linesButton.on('click', function () {
            isEnabled = !isEnabled; // 現在の状態を反転する
            if (isEnabled) {
                // 処理を有効にするためのコードを記述する
                // linesButton.value = '全て表示';
                linesButton.removeClass('btn-secondary');
                linesButton.addClass('btn-primary');
                hideHolizontalLines();
            } else {
                // 処理を無効にするためのコードを記述する
                // linesButton.value = '明細行のみ';
                linesButton.removeClass('btn-primary');
                linesButton.addClass('btn-secondary');
                showHolizontalLines();
            }
        });

        const selectGL = document.getElementById("selectGL");
        selectGL.addEventListener("change", (event) => {
            const selected = event.target.value;
            getGL(selected);
        });

        const selectTB = document.getElementById("selectTB");
        selectTB.addEventListener("change", (event) => {
            const selectedMonth = event.target.value;
            getTB(selectedMonth)
        });

        // 初期設定
        getEPSON();
        getFileList();
        getHorizontal();
        getInstances();
        getGLlist();
        getTBlist();
        var selectGLvalue = document.querySelector('#selectGL').value;
        var selectTBvalue = document.querySelector('#selectTB').value;
        getGL(selectGLvalue)
        getTB(selectTBvalue)

        var elementEPSON = document.getElementById("nav_EPSON-R4");
        var elementXBRL = document.getElementById("nav_XBRL-GL");
        let sourceSelect = document.querySelector('#source');
        if ('hokkaidou-sangyou'==sourceSelect.value) {
            elementEPSON.style.display = 'block';
            elementXBRL.style.display = 'none';
        } else if ('xbrl-gl'==sourceSelect.value) {
            elementEPSON.style.display = 'none';
            elementXBRL.style.display = 'block';
        }

        sourceSelect.addEventListener("change", (event) => {
            event.stopPropagation();
            var href = document.querySelector('.nav-link.active').getAttribute('href');
            switch (href) {
                case '#tab_horizontal':
                    getHorizontal();
                    break;
                case '#tab_GL':
                    getGLlist();
                    var selectGLvalue = document.querySelector('#selectGL').value;
                    getGL(selectGLvalue);
                    break;
                case '#tab_TB':
                    getTBlist();
                    var selectTBvalue = document.querySelector('#selectTB').value;
                    getTB(selectTBvalue);
                    break;
                case '#tab_tidyData':
                    getInstances();
                    break;
                default:
                    // 上記のいずれのcaseにも一致しない場合の処理
                    break;
            }
            var elementEPSON = document.getElementById("nav_EPSON-R4");
            var elementXBRL = document.getElementById("nav_XBRL-GL");
            let sourceSelect = document.querySelector('#source');
            if ('hokkaidou-sangyou'==sourceSelect.value) {
                elementEPSON.style.display = 'block';
                elementXBRL.style.display = 'none';
            } else if ('xbrl-gl'==sourceSelect.value) {
                elementEPSON.style.display = 'none';
                elementXBRL.style.display = 'block';
            }
        });

        // https://www.w3schools.com/howto/howto_js_scroll_to_top.asp
        //Get the button:
        let gotoTopButton = document.getElementById("gotoTopButton");
        gotoTopButton.style.display = 'none';
        // When the user scrolls down 20px from the top of the document, show the button
        window.onscroll = function () { scrollFunction() };

        function scrollFunction() {
            if ($('#gotoTopButton')) {
                if (document.body.scrollTop > 80 || document.documentElement.scrollTop > 80) {
                    gotoTopButton.style.display = 'block';
                } else {
                    gotoTopButton.style.display = 'none';
                }
            }
        }

        $('#gotoTopButton').on('click', function () {
            gotoTop();
        });

        // When the user clicks on the button, scroll to the top of the document
        function gotoTop() {
            document.body.scrollTop = 0; // For Safari
            document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
        }

        window.onload = function () {
            // URLからタブ指定パラメータを取得
            var tabParam = new URLSearchParams(window.location.search).get('tab');
            if (tabParam) {
                var activeTabLink = document.querySelector('.nav-link.active');
                if (activeTabLink) {
                    activeTabLink.classList.remove('active');
                    activeTabLink.setAttribute('aria-selected', 'false');
                    var activeTabContentId = activeTabLink.getAttribute('href').substring(1);
                    var activeTabContent = document.getElementById(activeTabContentId);
                    if (activeTabContent) {
                        activeTabContent.classList.remove('active', 'show');
                    }
                }
                // タブ指定パラメータがある場合、対応するタブをアクティブにする
                var tabLink = document.querySelector('a[href="#' + tabParam + '"]');
                if (tabLink) {
                    tabLink.classList.add('active');
                    tabLink.setAttribute('aria-selected', 'true');
                    var tabContentId = tabLink.getAttribute('href').substring(1);
                    var tabContent = document.getElementById(tabContentId);
                    if (tabContent) {
                        tabContent.classList.add('active', 'show');
                    }
                }
            }
        }
    }
    return {
        initModule: initModule
    };
})();
// main.js