/**
 * convert.js
 * convert module
 **/
convert = (function () {

  function readSelectedFile(f) {
    //Retrieve the first (and only!) File from the FileList object
    // var f = evt.target.files[0];
    if (f) {
      var r = new FileReader();
      r.onload = function (e) {
        var contents = e.target.result;
        if (f.name.indexOf(".csv") > 0) {
          document.querySelector('#csv2invoice #csv_title').innerHTML = f.name;
          document.querySelector('#csv2invoice #csv_area').textContent = contents;
        } else {
          var _contents = contents.substring(contents.indexOf(">") + 1, 100);
          let start = 1 + _contents.indexOf("<");
          let end = _contents.indexOf(" ")
          let target = _contents.substring(start, 2 + end - start);
          let syntax = "";
          if ("Invoice" == target) {
            syntax = "JP-PINT";          
          }
          else if (0 == target.indexOf("rsm:SME")) {
            syntax = "SME-COMMON";          
          }
          document.querySelectorAll('#invoice2csv input[name="syntax"]').disabled = true;
          if (syntax=="JP-PINT") {
            document.querySelectorAll('#invoice2csv input[name="syntax"]')[0].checked = true;
          } else {
            document.querySelectorAll('#invoice2csv input[name="syntax"]')[1].checked = true;
          }
          let xmlfile = f.name;
          document.querySelector('#invoice2csv #xml_title').innerHTML = syntax + ': ' + xmlfile;  
          document.querySelector('#invoice2csv #xml_area').textContent = contents;
        }
      }
      r.readAsText(f);
    } else {
      alert("Failed to load file");
    }
  }

  function invoice2csv(evt) {
    const url = 'https://www.wuwei.space/core-japan/server/invoice2csv.php';
    const formData = new FormData();
    let file = document.querySelector('#invoice2csv-form input[type="file"]').files[0];
    if (!file) {
      file = evt.target.querySelector('#invoice2csv-form input[type="file"]').files[0];
    }
    formData.append('file', file);
    var syntax = document.querySelector('#invoice2csv-form input[name="syntax"]:checked').value;
    formData.append("syntax", syntax);
    fetch(url, {
      method: 'POST',
      body: formData
    }).then(response => {
      return response.text();
    }).then(data => {
      if (0 == data.indexOf("ERROR") || '{' != data.substring(0, 1)) {
        alert(data)
      }
      else {
        let response = JSON.parse(data);
        let syntax = response.syntax;
        let uuid = response.uuid;
        let csvfile = response.csvfile;
        let xmlfile = response.xmlfile;
        let csv_contents = response.csv_contents;
        let xml_contents = response.xml_contents;
        document.querySelector('#invoice2csv #csv_title').innerHTML = csvfile;
        document.querySelector('#invoice2csv #xml_title').innerHTML = syntax + ': ' + xmlfile;
        document.querySelector('#invoice2csv #csv_area').textContent = csv_contents;
        document.querySelector('#invoice2csv #xml_area').textContent = xml_contents;
      }
    });
  }

  function csv2invoice(evt) {
    const url = 'https://www.wuwei.space/core-japan/server/csv2invoice.php';
    const formData = new FormData();
    let file = document.querySelector('#csv2invoice-form input[type="file"]').files[0];
    if (!file) {
      file = evt.target.querySelector('#csv2invoice-form input[type="file"]').files[0];
    }
    formData.append('file', file);
    var syntax = document.querySelector('#csv2invoice-form input[name="syntax"]:checked').value;
    formData.append("syntax", syntax);
    fetch(url, {
      method: 'POST',
      body: formData
    }).then(response => {
      return response.text();
    }).then(data => {
      if (0 == data.indexOf("ERROR") || '{' != data.substring(0, 1)) {
        alert(data)
      }
      else {
        let response = JSON.parse(data);
        let syntax = response.syntax;
        let uuid = response.uuid;
        let csvfile = response.csvfile;
        let xmlfile = response.xmlfile;
        let csv_contents = response.csv_contents;
        let xml_contents = response.xml_contents;
        document.querySelector('#csv2invoice #csv_title').innerHTML = csvfile;
        document.querySelector('#csv2invoice #xml_title').innerHTML = syntax + ': ' + xmlfile;
        document.querySelector('#csv2invoice #csv_area').textContent = csv_contents;
        document.querySelector('#csv2invoice #xml_area').textContent = xml_contents;
      }
    });
  }

  function initModule() {
    document.getElementById('invoice2csv-form').addEventListener('submit', e => {
      e.preventDefault();
      invoice2csv(e);
    });
    document.getElementById('csv2invoice-form').addEventListener('submit', e => {
      e.preventDefault();
      csv2invoice(e);
    });
    document.querySelector('#invoice2csv-form input[type="file"]').addEventListener('change', e => {
      e.preventDefault();
      const file = document.querySelector('#invoice2csv-form input[type="file"]').files[0];
      if (!file) {
        file = etarget.querySelector('#invoice2csv-form input[type="file"]').files[0];
      }
      readSelectedFile(file);
    });
    document.querySelector('#csv2invoice-form input[type="file"]').addEventListener('change', e => {
      e.preventDefault();
      const file = document.querySelector('#csv2invoice-form input[type="file"]').files[0];
      if (!file) {
        file = e.target.querySelector('#csv2invoice-form input[type="file"]').files[0];
      }
      readSelectedFile(file);
    });
  }

  return {
    initModule: initModule,
    invoice2csv: invoice2csv,
    csv2invoice: csv2invoice
  };
})();
// convert.js