/**
 * convert.js
 * convert module
 **/
convert = (function () {

    function readSelectedFile(evt) {
        //Retrieve the first (and only!) File from the FileList object
        var f = evt.target.files[0];
        if (f) {
          var r = new FileReader();
          r.onload = function(e) { 
            var contents = e.target.result;
            if (f.name.indexOf(".csv") > 0) {
                document.querySelector('#csv2invoice #csv_title').innerHTML = f.name;
                document.querySelector('#csv2invoice #csv_area').textContent = contents;
            } else {
                document.querySelector('#invoice2csv #xml_title').textContent = f.name;
                document.querySelector('#invoice2csv #xml_area').textContent = contents;
                contents = contents.substring(contents.indexOf(">")+1,100);
                let start = 1 + contents.indexOf("<");
                let end = contents.indexOf(" ")
                let target = contents.substring(start,2 + end - start);    
                let syntax = "";            
                if ("Invoice"==target) {
                    syntax = "JP-PINT";
                    document.querySelectorAll('#invoice2csv input[name="syntax"]')[0].checked=true
                    document.querySelectorAll('#csv2invoice input[name="syntax"]')[0].checked=true
                }
                else if (0==target.indexOf("rsm:SME")) {
                    syntax = "SME-COMMON";
                    document.querySelectorAll('#invoice2csv input[name="syntax"]')[1].checked=true
                    document.querySelectorAll('#csv2invoice input[name="syntax"]')[1].checked=true
                }
                let xmlfile = f.name;
                document.querySelector('#invoice2csv #xml_title').innerHTML = syntax + ': ' + xmlfile;
            }        
            // alert( "Got the file.n" 
            //       +"name: " + f.name + "n"
            //       +"type: " + f.type + "n"
            //       +"size: " + f.size + " bytesn"
            //       + "starts with: " + contents.substr(1, contents.indexOf("n"))
            // );  
          }
          r.readAsText(f);
        } else { 
          alert("Failed to load file");
        }
      }

    function invoice2csv() {
        const url = 'https://www.wuwei.space/core-japan/server/invoice2csv.php';
        const formData = new FormData();
        const file = document.querySelector('[type=file]').files[0];
        formData.append('file', file);
        var syntax = document.querySelector('input[name="syntax"]:checked').value;
        formData.append("syntax", syntax);
        fetch(url, {
            method: 'POST',
            body: formData
        }).then(response => {
            return response.text();
        }).then(data => {
            if (0==data.indexOf("ERROR") || '{'!=data.substring(0,1)) {
                alert(data);
            }
            else {
                let response = JSON.parse(data);
                let syntax = response.syntax;
                let uuid = response.uuid;
                let csvfile = response.csvfile;
                document.querySelector('#invoice2csv #csv_title').innerHTML = csvfile;
                let xmlfile = response.xmlfile;
                document.querySelector('#invoice2csv #xml_title').innerHTML = syntax + ': ' + xmlfile;
                let csv_contents = response.csv_contents;
                document.querySelector('#invoice2csv #csv_area').textContent = csv_contents;
                let xml_contents = response.xml_contents;
                document.querySelector('#invoice2csv #xml_area').textContent = xml_contents;
            }
        });
    }

    function csv2invoice() {
        const url = 'https://www.wuwei.space/core-japan/server/csv2invoice.php';
        const formData = new FormData();
        const file = document.querySelector('[type=file]').files[0];
        formData.append('file', file);
        var syntax = document.querySelector('input[name="syntax"]:checked').value;
        formData.append("syntax", syntax);
        fetch(url, {
            method: 'POST',
            body: formData
        }).then(response => {
            return response.text();
        }).then(data => {
            if (0==data.indexOf("ERROR") || '{'!=data.substring(0,1)) {
                alert(data);
            }
            else {
                let response = JSON.parse(data);
                let syntax = response.syntax;
                let uuid = response.uuid;
                let csvfile = response.csvfile;
                document.querySelector('#csv2invoice #csv_title').innerHTML = csvfile;
                let xmlfile = response.xmlfile;
                document.querySelector('#csv2invoice #xml_title').innerHTML = syntax + ': ' + xmlfile;
                let csv_contents = response.csv_contents;
                document.querySelector('#csv2invoice #csv_area').textContent = csv_contents;
                let xml_contents = response.xml_contents;
                document.querySelector('#csv2invoice #xml_area').textContent = xml_contents;
            }
        });
    }

    function initModule() {
        document.getElementById('invoice2csv-form').addEventListener('submit', e => {
            e.preventDefault();
            convert.invoice2csv();//e.target);
        });
        document.getElementById('csv2invoice-form').addEventListener('submit', e => {
            e.preventDefault();
            convert.csv2invoice();//e.target);
        });
        document.getElementById('file').addEventListener('change', readSelectedFile, false);
    }

    return {
        initModule: initModule,
        invoice2csv: invoice2csv,
        csv2invoice: csv2invoice
    };
})();
// convert.js