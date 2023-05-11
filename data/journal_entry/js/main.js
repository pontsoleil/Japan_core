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

    function getInstances() {
        // XMLHttpRequestオブジェクトを使用して、CSVファイルを取得する
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'instances.csv', true);
        xhr.onload = function () {
            // 取得したCSVデータをパースして、JavaScriptの配列に変換する

            var data = xhr.responseText.split('\n');
            var items = [];
            for (var i = 0; i < data.length; i++) {
                var item = data[i].split(',');
                items.push(item);
            }
            // var items_count = items.length;
            // snackbar.open({ 'message': '<i class="fa fa-cog fa-spin"></i> ' + items_count + ' 件読み込み中', 'type': 'info' });
            // 配列の内容を加工して、HTML要素に追加して表示する
            var tableBody = document.querySelector('#instances tbody');
            for (var i = 1; i < items.length; i++) {
                // if (0 == i % 5000) {
                //     snackbar.close();
                //     snackbar.open({ 'message': '<i class="fa fa-cog fa-spin"></i> 1' + i + ' / ' + items_count + ' 件読み込み中', 'type': 'info' });
                // }
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
                td1.textContent = item[0]
                td1.classList.add('text-center')
                td2.textContent = item[1]
                td2.classList.add('text-center')
                td3.textContent = item[6]
                td4.textContent = item[19]
                td4.classList.add('text-center')
                td5.textContent = item[12]
                td6.textContent = item[13]
                td6.classList.add('text-center')
                td7.textContent = item[14]
                td7.classList.add('text-center')
                td8.textContent = item[15]
                td9.textContent = item[17]
                td9.classList.add('text-right')
                td10.textContent = item[20]
                td10.classList.add('text-center')
                td11.textContent = item[22]
                td12.textContent = item[23]
                td12.classList.add('text-center')
                td13.textContent = item[25]
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
                tableBody.appendChild(tr);
            }
            // snackbar.close();
        };
        xhr.send();
    }

    function getHorizontal() {
        // XMLHttpRequestオブジェクトを使用して、CSVファイルを取得する
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'horizontal_ledger.csv', true);
        xhr.onload = function () {
            // 取得したCSVデータをパースして、JavaScriptの配列に変換する
            var data = xhr.responseText.split('\n');
            var items = [];
            for (var i = 0; i < data.length; i++) {
                var item = data[i].split(',');
                items.push(item);
            }
            var items_count = items.length;
            snackbar.open({ 'message': '<i class="fa fa-cog fa-spin"></i> ' + items_count + ' 件読み込み中', 'type': 'info' });
            // 配列の内容を加工して、HTML要素に追加して表示する
            var tableBody = document.querySelector('#horizontal tbody');
            for (var i = 1; i < items.length; i++) {
                if (0 == i % 5000) {
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

                td1.textContent = item[0]
                td1.classList.add('text-center')
                td2.textContent = item[1]
                td2.classList.add('text-center')
                td3.textContent = item[2]
                td3.classList.add('text-center')
                td4.textContent = item[3]
                td4.classList.add('text-center')
                td5.textContent = item[5]
                td5.classList.add('text-center')
                td6.textContent = item[8]
                td6.classList.add('text-center')

                td7.textContent = item[15]
                td7.classList.add('text-center')
                td8.textContent = item[14]

                td9.textContent = item[17]
                td9.classList.add('text-center')
                td10.textContent = item[18]
                td11.textContent = item[20]
                td11.classList.add('text-right')

                td12.textContent = item[21]
                td12.classList.add('text-center')
                td13.textContent = item[23]

                td14.textContent = item[24]
                td14.classList.add('text-center')
                td15.textContent = item[25]
                td16.textContent = item[27]
                td16.classList.add('text-right')

                td17.textContent = item[28]
                td17.classList.add('text-center')
                td18.textContent = item[30]

                td19.textContent = item[31]
                td19.classList.add('text-center')
                td20.textContent = item[33]

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
                tableBody.appendChild(tr);
            }
            snackbar.close();

            hideHolizontalLines();
        };
        xhr.send();
    }

    function hideHolizontalLines() {
        var thead = document.querySelector('#horizontal thead');
        var row = thead.rows[0];
        row.cells[19].style.display = 'none';
        row.cells[18].style.display = 'none';
        row.cells[17].style.display = 'none';
        row.cells[16].style.display = 'none';
        row.cells[12].style.display = 'none';
        row.cells[11].style.display = 'none';
        row.cells[5].style.display = 'none';
        row.cells[4].style.display = 'none';
        row.cells[3].style.display = 'none';
        // tbody要素を取得する
        var tbody = document.querySelector('#horizontal tbody');
        // tbody要素内のtr要素を順番に取得する
        for (var i = 0; i < tbody.rows.length; i++) {
            // 各tr要素内のn番目のtd要素を取得する（ここでは3番目から）
            var td2 = tbody.rows[i].cells[2];
            var td3 = tbody.rows[i].cells[3];
            var td4 = tbody.rows[i].cells[4];
            var td6 = tbody.rows[i].cells[6];
            var td11 = tbody.rows[i].cells[11];
            var td16 = tbody.rows[i].cells[16];
            // 取得したtd要素が空かどうかを判定し、空であればtr要素を非表示にする
            if ('' == td2.textContent.trim() || '' != td3.textContent.trim() || '' != td4.textContent.trim() ||
                ('' == td6.textContent.trim() && ('' != td11.textContent.trim() || '' != td16.textContent.trim()))) {
                tbody.rows[i].style.display = 'none';
            }
        }
        for (i = 0; i < tbody.rows.length; i++) {
            row = tbody.rows[i];
            row.cells[19].style.display = 'none';
            row.cells[18].style.display = 'none';
            row.cells[17].style.display = 'none';
            row.cells[16].style.display = 'none';
            row.cells[12].style.display = 'none';
            row.cells[11].style.display = 'none';
            row.cells[5].style.display = 'none';
            row.cells[4].style.display = 'none';
            row.cells[3].style.display = 'none';
        }
    }

    function showHolizontalLines() {
        var thead = document.querySelector('#horizontal thead');
        var row = thead.rows[0];
        row.cells[3].style.display = '';
        row.cells[4].style.display = '';
        row.cells[5].style.display = '';
        row.cells[11].style.display = '';
        row.cells[12].style.display = '';
        row.cells[16].style.display = '';
        row.cells[17].style.display = '';
        row.cells[18].style.display = '';
        row.cells[19].style.display = '';
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
            row.cells[11].style.display = '';
            row.cells[12].style.display = '';
            row.cells[16].style.display = '';
            row.cells[17].style.display = '';
            row.cells[18].style.display = '';
            row.cells[19].style.display = '';
        }
    }

    function getGL(url) {
        // XMLHttpRequestオブジェクトを使用して、CSVファイルを取得する
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'GL/' + url, true);
        xhr.onload = function () {
            // 取得したCSVデータをパースして、JavaScriptの配列に変換する
            var data = xhr.responseText.split('\n');
            var items = [];
            for (var i = 0; i < data.length; i++) {
                var item = data[i].split(',');
                items.push(item);
            }
            // 配列の内容を加工して、HTML要素に追加して表示する
            var tableBody = document.querySelector('#GL tbody');
            tableBody.innerHTML = '';
            for (var i = 1; i < items.length; i++) {
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
                var td9 = document.createElement('td');;
                var td10 = document.createElement('td');;
                /*
                num
                GL02
                GL02-GL55
                date
                contra_account
                contra_account_name
                note
                debit_amount
                credit_amount
                balance
                */
                td1.textContent = item[0]
                td1.classList.add('text-right')
                td2.textContent = item[1]
                td2.classList.add('text-center')
                td3.textContent = item[2]
                td3.classList.add('text-center')
                td4.textContent = item[3]
                td5.textContent = item[4]
                td5.classList.add('text-center')
                td6.textContent = item[5]
                td7.textContent = item[6]
                td8.textContent = item[7]
                td8.classList.add('text-right')
                td9.textContent = item[8]
                td9.classList.add('text-right')
                td10.textContent = item[9]
                td10.classList.add('text-right')
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
                tableBody.appendChild(tr);
            }
        };
        xhr.send();
    }

    function getTB(month) {
        // XMLHttpRequestオブジェクトを使用して、CSVファイルを取得する
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'TB/' + month + '/trial_balance.csv', true);
        xhr.onload = function () {
            // 取得したCSVデータをパースして、JavaScriptの配列に変換する
            var data = xhr.responseText.split('\n');
            var items = [];
            for (var i = 0; i < data.length; i++) {
                var item = data[i].split(',');
                items.push(item);
            }
            // 配列の内容を加工して、HTML要素に追加して表示する
            var tableBody = document.querySelector('#TB tbody');
            tableBody.innerHTML = '';
            for (var i = 1; i < items.length; i++) {
                var item = items[i];
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
                td1.textContent = item[0]
                td2.classList.add('text-center')
                td2.textContent = item[1]
                td2.classList.add('text-center')
                td3.textContent = item[2]
                td4.textContent = item[3]
                td4.classList.add('text-right')
                td5.textContent = item[4]
                td5.classList.add('text-right')
                td6.textContent = item[5]
                td6.classList.add('text-right')
                td7.textContent = item[6]
                td7.classList.add('text-right')
                tr.appendChild(td1);
                tr.appendChild(td2);
                tr.appendChild(td3);
                tr.appendChild(td4);
                tr.appendChild(td5);
                tr.appendChild(td6);
                tr.appendChild(td7);
                tableBody.appendChild(tr);
            }
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

                select.on('change', function () {
                    var fileName = $(this).val();
                    // var fileName = fileSelect.options[fileSelect.selectedIndex].value;
                    var fileSelect = document.getElementById("file-list");
                    var xhr = new XMLHttpRequest();
                    xhr.open("GET", "./XBRL_GLinstances/" + fileName, true);
                    xhr.onreadystatechange = function () {
                        if (xhr.readyState === 4 && xhr.status === 200) {
                            let xmlData = xhr.responseXML;
                            // XMLデータを文字列に変換する
                            let wellFormedXml = new XMLSerializer().serializeToString(xmlData);
                            // HTMLエスケープする
                            const escapedXmlString = escapeHtml(wellFormedXml);
                            var contentDiv = document.getElementById("file-content");
                            contentDiv.innerHTML = escapedXmlString;// `<pre>${formattedXml}</pre>`;
                        }
                    };
                    xhr.send();
                });
            })
            .catch(error => {
                console.error('エラー: ファイル一覧が取得できません', error);
                alert('エラー: ファイル一覧が取得できません');
            });
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

        var linesButton = $('#linesButton');
        linesButton.value = '明細行のみ';
        var isEnabled = false; // 初期状態では処理を無効にする

        linesButton.on('click', function () {
            isEnabled = !isEnabled; // 現在の状態を反転する

            if (isEnabled) {
                // 処理を有効にするためのコードを記述する
                // linesButton.value = '全て表示';
                linesButton.removeClass('btn-secondary')
                linesButton.addClass('btn-primary')
                hideHolizontalLines();
            } else {
                // 処理を無効にするためのコードを記述する
                // linesButton.value = '明細行のみ';
                linesButton.removeClass('btn-primary')
                linesButton.addClass('btn-secondary')
                showHolizontalLines();
            }
        });

        const selectGL = document.getElementById("selectGL");
        selectGL.addEventListener("change", (event) => {
            const selectedGL = event.target.value;
            // 選択されたオプションに応じた処理を実行する
            getGL(selectedGL)
        });

        const selectTB = document.getElementById("selectTB");
        selectTB.addEventListener("change", (event) => {
            const selectedMonth = event.target.value;
            // 選択されたオプションに応じた処理を実行する
            getTB(selectedMonth)
        });

        getHorizontal();
        getGL('111現金.csv')
        getTB('2009-04')
        getInstances();
        getFileList();
        // fetch('./file_list.php')
        //     .then(response => response.json())
        //     .then(data => {
        //         var file_list = $('#file-list');
        //         var select = $('<select id="file-select"></select>');
        //         for (var i = 0; i < Object.keys(data).length; i++) {
        //             var value = Object.values(data)[i];
        //             var option = $('<option></option>').text(value).val(value);
        //             select.append(option);
        //         }
        //         file_list.append(select);

        //         select.on('change', function () {
        //             var fileName = $(this).val();
        //             // var fileName = fileSelect.options[fileSelect.selectedIndex].value;
        //             var fileSelect = document.getElementById("file-list");
        //             var xhr = new XMLHttpRequest();
        //             xhr.open("GET", "./XBRL_GLinstances/" + fileName, true);
        //             xhr.onreadystatechange = function () {
        //                 if (xhr.readyState === 4 && xhr.status === 200) {
        //                     let xmlData = xhr.responseXML;
        //                     // XMLデータを文字列に変換する
        //                     let wellFormedXml = new XMLSerializer().serializeToString(xmlData);
        //                     // HTMLエスケープする
        //                     const escapedXmlString = escapeHtml(wellFormedXml);
        //                     var contentDiv = document.getElementById("file-content");
        //                     contentDiv.innerHTML = escapedXmlString;// `<pre>${formattedXml}</pre>`;
        //                 }
        //             };
        //             xhr.send();
        //         });
        //     })
        //     .catch(error => {
        //         console.error('Error: Could not retrieve file list.', error);
        //         alert('Error: Could not retrieve file list.');
        //     });

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

    }
    return {
        initModule: initModule
    };
})();
// main.js