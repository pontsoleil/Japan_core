/**
 * convert.js
 * convert module
 **/
convert = (function () {

	function readSelectedFile(f) {
		if (f) {
			var r = new FileReader();
			r.onload = function (e) {
				var contents = e.target.result;
				if (f.name.indexOf(".csv") > 0) {
					document.querySelector('#csv2invoice #csv_title').innerHTML = f.name;
					fillTable(contents, '#csv2invoice #csv_table', '');
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

	function _convertCSVtoJSON(csv, column) {
		function _escape_comma(line) {
			escaped_line = '';
			var found = false;
			for (var i = 0; i < line.length; i++) {
				var ch = line.charAt(i);
				if ('"' == ch) {
					if (!found) {
						found = true;
					} else {
						found = false;
					}
				}
				if (found && ',' == ch) {
					escaped_line += '__comma__';
				} else {
					escaped_line += ch;
				}
			}
			return escaped_line;
		}

		function _unescape_comma(escaped_line) {
			if (escaped_line) {
				line = escaped_line.replace(/__comma__/g, ',');
			} else {
				line = '';
			}
			return line;
		}

		var lines = csv.split("\n");
		var result = [];
		var headers = lines[0].split(",");

		for (var i = 1; i < lines.length; i++) {
			var obj = {};
			var line = _escape_comma(lines[i])
			var currentline = line.split(",");

			for (var j = 0; j < headers.length; j++) {
				var id;
				if (column == 'C') {
					id = 'C' + ('' + j);
				} else {
					id = headers[j];
				}
				obj[id] = _unescape_comma(currentline[j]);
			}
			result.push(obj);
		}
		return result; //JSON
	}

	function escape(data) {
		let escaped = data.replace(/\\n/g, "\\n")
			.replace(/\\'/g, "\\'")
			.replace(/\\"/g, '\\"')
			.replace(/\\&/g, "\\&")
			.replace(/\\r/g, "\\r")
			.replace(/\\t/g, "\\t")
			.replace(/\\b/g, "\\b")
			.replace(/\\f/g, "\\f");
		return escaped;
	}

	function fillTable(contents, table_id, column) {
		let json = _convertCSVtoJSON(contents, column);
		let table = document.querySelector(table_id);
		let thead = table.querySelector('thead');
		let header = Object.keys(json[0])
		thead.innerHTML = '';
		let tr = thead.insertRow();
		// let th = document.createElement('th');
		// let td = tr.insertCell();
		// tr.append(td);
		// td.setAttribute('scope','col');
		// td.style = 'white-space: nowrap;';
		// td.innerHTML = header[0];
		for (var i = 0; i < header.length; i++) {
			let td = tr.insertCell();
			td.setAttribute('scope', 'col')
			td.style = 'white-space: nowrap;';
			td.innerHTML = header[i];
		}
		let tbody = table.querySelector('tbody');
		tbody.innerHTML = '';
		for (let row of json) {
			let tr = tbody.insertRow();
			// let th = document.createElement('th');
			// tr.append(th);
			// th.setAttribute('scope','row')
			// th.style = 'white-space: nowrap;';
			// th.innerHTML = row[header[0]];
			for (var i = 0; i < header.length; i++) {
				let td = tr.insertCell();
				td.style = 'white-space: nowrap;';
				td.innerHTML = row[header[i]];
			}
		}
	}

	function invoice2csv(evt) {
		const formData = new FormData();
		let file = document.querySelector('#invoice2csv-form input[type="file"]').files[0];
		if (!file) {
			file = evt.target.querySelector('#invoice2csv-form input[type="file"]').files[0];
		}
		formData.append('file', file);
		var syntax = document.querySelector('#invoice2csv-form input[name="syntax"]:checked').value;
		formData.append("syntax", syntax);
		fetch('https://www.wuwei.space/core-japan/server/invoice2csv.php', {
			method: 'POST',
			body: formData
		})
			.then(response => {
				return response.text();
			})
			.then(data => {
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
					let transposed_contents = response.transposed_contents;
					document.querySelector('#invoice2csv #transposed_title').innerHTML = csvfile + '（縦横転置）';
					fillTable(transposed_contents, '#invoice2csv #transposed_table', 'C')
					document.querySelector('#invoice2csv #csv_title').innerHTML = csvfile;
					fillTable(csv_contents, '#invoice2csv #csv_table', '');
					document.querySelector('#invoice2csv #xml_title').innerHTML = syntax + ': ' + xmlfile;
				}
			})
			.catch(error => {
				alert('通信に失敗しました', error);
			});
	}

	function csv2invoice(evt) {
		const formData = new FormData();
		let file = document.querySelector('#csv2invoice-form input[type="file"]').files[0];
		if (!file) {
			file = evt.target.querySelector('#csv2invoice-form input[type="file"]').files[0];
		}
		formData.append('file', file);
		var syntax = document.querySelector('#csv2invoice-form input[name="syntax"]:checked').value;
		formData.append("syntax", syntax);
		fetch('https://www.wuwei.space/core-japan/server/csv2invoice.php', {
			method: 'POST',
			body: formData
		})
			.then(response => {
				return response.text();
			})
			.then(data => {
				if (0 == data.indexOf("ERROR") || '{' != data.substring(0, 1)) {
					alert(data)
				}
				else {
					let response = JSON.parse(data);
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
			})
			.catch(error => {
				alert('通信に失敗しました', error);
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
		window.onscroll = function () { scrollFunction() };

		function scrollFunction() {
			if ($('#gotoTopButton')) {
				if (document.body.scrollTop > 120 || document.documentElement.scrollTop > 120) {
					gotoTopButton.style.display = 'block';
				} else {
					gotoTopButton.style.display = 'none';
				}
			}
		}

		$('#gotoTopButton').on('click', function () {
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
// convert.js