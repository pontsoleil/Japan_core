<!DOCTYPE html>
<html>
<head>
    <title>CSVデータを加工して表示する</title>
</head>
<body>
    <table id="myTable">
        <thead>
            <tr>
                <th>商品名</th>
                <th>価格</th>
                <th>数量</th>
                <th>合計</th>
            </tr>
        </thead>
        <tbody>
        </tbody>
    </table>
    <script>
        // XMLHttpRequestオブジェクトを使用して、CSVファイルを取得する
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'data.csv', true);
        xhr.onload = function() {
            // 取得したCSVデータをパースして、JavaScriptの配列に変換する
            var data = xhr.responseText.split('\n');
            var items = [];
            for (var i = 0; i < data.length; i++) {
                var item = data[i].split(',');
                items.push(item);
            }

            // 配列の内容を加工して、HTML要素に追加して表示する
            var tableBody = document.querySelector('#myTable tbody');
            for (var i = 0; i < items.length; i++) {
                var item = items[i];
                var price = parseInt(item[1], 10);
                var quantity = parseInt(item[2], 10);
                var total = price * quantity;
                var tr = document.createElement('tr');
                var td1 = document.createElement('td');
                var td2 = document.createElement('td');
                var td3 = document.createElement('td');
                var td4 = document.createElement('td');
                td1.textContent = item[0];
                td2.textContent = item[1];
                td3.textContent = item[2];
                td4.textContent = total;
                tr.appendChild(td1);
                tr.appendChild(td2);
                tr.appendChild(td3);
                tr.appendChild(td4);
                tableBody.appendChild(tr);
            }
        };
        xhr.send();
    </script>
</body>
</html>
