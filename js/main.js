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
					let target = _contents.substring(start);
					let syntax = "";
					if (0 == target.indexOf("Invoice")) {
						syntax = "JP-PINT";
					}
					else if (0 == target.indexOf("rsm:SME")) {
						syntax = "SME-COMMON";
					}
					document.querySelectorAll('#invoice2csv input[name="syntax"]').disabled = true;
					if (syntax == "JP-PINT") {
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

	function _convertCSVtoJSON(csv,column) {
		function _escape_comma(line) {
			escaped_line = '';
			var found = false;
			for (var i = 0; i < line.length; i++) {
				var ch = line.charAt(i);
				if ('"'==ch) {
					if (!found) { 
						found = true;
					} else {
						found = false;
					}
				}
				if (found && ','==ch) {
					escaped_line += '__comma__';
				} else {
					escaped_line += ch;
				}
			}
			return escaped_line;
		}

		function _unescape_comma(escaped_line) {
			if (escaped_line) {
				line = escaped_line.replace(/__comma__/g,',');
			} else {
				line = '';
			}
			return line;
		}
		var lines = csv.split("\n");
		var result = [];	
		// NOTE: If your columns contain commas in their values, you'll need
		// to deal with those before doing the next step 
		// (you might convert them to &&& or something, then covert them back later)
		// jsfiddle showing the issue https://jsfiddle.net/
	
		var headers = lines[0].split(",");
	
		for (var i = 1; i < lines.length; i++) {
			var obj = {};
			var line = _escape_comma(lines[i])
			var currentline = line.split(",");
	
			for (var j = 0; j < headers.length; j++) {
				var id;
				if (column=='C') {
					id = 'C'+(''+j);
				} else {
					id = headers[j];
				}
				obj[id] = _unescape_comma(currentline[j]);
			}
			result.push(obj);
		}
		return result; //JSON
	}

	function invoice2csv(evt) {
		const url = 'https://www.wuwei.space/core-japan/server/invoice2csv.cgi';
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
				let escaped = data.replace(/\\n/g, "\\n")
								.replace(/\\'/g, "\\'")
								.replace(/\\"/g, '\\"')
								.replace(/\\&/g, "\\&")
								.replace(/\\r/g, "\\r")
								.replace(/\\t/g, "\\t")
								.replace(/\\b/g, "\\b")
								.replace(/\\f/g, "\\f");
				let response = JSON.parse(escaped);
				let syntax = response.syntax;
				let uuid = response.uuid;
				let csvfile = response.csvfile;
				let xmlfile = response.xmlfile;
				let csv_contents = response.csv_contents;
				let transposed_contents = response.transposed_contents;
				// let xml_contents = response.xml_contents;
				document.querySelector('#invoice2csv #csv_title').innerHTML = csvfile;
				document.querySelector('#invoice2csv #xml_title').innerHTML = syntax + ': ' + xmlfile;
				document.querySelector('#invoice2csv #csv_area').textContent = csv_contents;
				// document.querySelector('#invoice2csv #xml_area').textContent = xml_contents;
				let csv_json = _convertCSVtoJSON(csv_contents);
				let transposed_table = document.getElementById('transposed_table');
				let transposed_json = _convertCSVtoJSON(transposed_contents,'C');
				transposed_table.innerHTML = "";
				for (let row of transposed_json) {
					let tr = transposed_table.insertRow();
					for (let col of row) {
						let td = tr.insertCell();
						td.innerHTML = col;
					}
				}
			}
		});
	}

	function csv2invoice(evt) {
		const url = 'https://www.wuwei.space/core-japan/server/csv2invoice.cgi';
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
				let escaped = data.replace(/\\n/g, "\\n")
								.replace(/\\'/g, "\\'")
								.replace(/\\"/g, '\\"')
								.replace(/\\&/g, "\\&")
								.replace(/\\r/g, "\\r")
								.replace(/\\t/g, "\\t")
								.replace(/\\b/g, "\\b")
								.replace(/\\f/g, "\\f");
				let response = JSON.parse(escaped);
				let syntax = response.syntax;
				let uuid = response.uuid;
				let csvfile = response.csvfile;
				let xmlfile = response.xmlfile;
				// let csv_contents = response.csv_contents;
				let xml_contents = response.xml_contents;
				document.querySelector('#csv2invoice #csv_title').innerHTML = csvfile;
				document.querySelector('#csv2invoice #xml_title').innerHTML = syntax + ': ' + xmlfile;
				// document.querySelector('#csv2invoice #csv_area').textContent = csv_contents;
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

		// https://www.w3schools.com/howto/howto_js_scroll_to_top.asp
		//Get the button:
		let gotoTopButton = document.getElementById("gotoTopButton");
		// When the user scrolls down 20px from the top of the document, show the button
		window.onscroll = function() {scrollFunction()};

		function scrollFunction() {
			if ($('#gotoTopButton')) {
			if (document.body.scrollTop > 120 || document.documentElement.scrollTop > 120) {
				gotoTopButton.style.display = 'block';
			} else {
				gotoTopButton.style.display = 'none';
			}
			}
		}

		$('#gotoTopButton').on('click', function() {
			gotoTop();
		})

		// When the user clicks on the button, scroll to the top of the document
		function gotoTop() {
			document.body.scrollTop = 0; // For Safari
			document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
		}
	}

	return {
		initModule: initModule,
		invoice2csv: invoice2csv,
		csv2invoice: csv2invoice
	};
})();
// main.js