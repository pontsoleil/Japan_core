/**
 * convert.js
 * convert module
 *
 * convert between csv and e-invoice
 * also supports syntax binding among different e-invoice
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
 **/
convert = (function () {

	let core_japan = {};
	let jp_pint_binding = {};
	let sme_binding = {};
	let syntax;
	let uuid;
	let base_url;

	// FormData polyfill by ChatGPT
	if (!window.FormData) {
		window.FormData = function() {
		  this.fake = true;
		  this.boundary = '--------FormDataPolyfill' + Math.random();
		  this._fields = [];
		}
		
		window.FormData.prototype.append = function(key, value, filename) {
		  if (value instanceof File) {
			this._fields.push([key, value, filename || value.name]);
		  } else {
			this._fields.push([key, value]);
		  }
		}
		
		window.FormData.prototype.toString = function() {
		  var boundary = this.boundary;
		  var body = '';
		  
		  this._fields.forEach(function(field) {
			body += '--' + boundary + '\r\n';
			
			if (field[1] instanceof File) {
			  body += 'Content-Disposition: form-data; name="' + field[0] + '"; filename="' + field[2] + '"\r\n';
			  body += 'Content-Type: ' + field[1].type + '\r\n\r\n';
			  body += field[1] + '\r\n';
			} else {
			  body += 'Content-Disposition: form-data; name="' + field[0] + '"\r\n\r\n';
			  body += field[1] + '\r\n';
			}
		  });
		  
		  body += '--' + boundary + '--';
		  return body;
		}
	  }
	  
	// cf. https://stackoverflow.com/questions/376373/pretty-printing-xml-with-javascript
	function formatXml(xml, tab) { // tab = optional indent value, default is tab (\t)
		var formatted = '', indent= '';
		tab = tab || '\t';
		xml.split(/>\s*</).forEach(function(node) {
			if (node.match( /^\/\w/ )) indent = indent.substring(tab.length); // decrease indent by one 'tab'
			formatted += indent + '<' + node + '>\r\n';
			if (node.match( /^<?\w[^>]*[^\/]$/ )) indent += tab;              // increase indent
		});
		return formatted.substring(1, formatted.length-3);
	}

	function updateSyntax(syntax,f) {
		if (document.getElementById('source2target').classList.contains('active')) {
			document.querySelectorAll('#source2target input[name="syntax"]').disabled = true;
			if (syntax == "JP-PINT") {
				document.querySelectorAll('#source2target input[name="syntax"]')[0].checked = true;
				document.querySelectorAll('#source2target input[name="target"]')[1].checked = true;
			} else if (syntax == "SME-COMMON") {
				document.querySelectorAll('#source2target input[name="syntax"]')[1].checked = true;
				document.querySelectorAll('#source2target input[name="target"]')[0].checked = true;
			}
			if (f && f.name) {
				let xmlfile = f.name;
				document.querySelector('#source2target #xml_title .name').innerHTML = syntax + ': ' + xmlfile;
				document.querySelector('#source2target #xml_area').textContent = contents;
			}
		} else if (document.getElementById('invoice2csv').classList.contains('active')) {
			document.querySelectorAll('#invoice2csv input[name="syntax"]').disabled = true;
			if (syntax == "JP-PINT") {
				document.querySelectorAll('#invoice2csv input[name="syntax"]')[0].checked = true;
				document.querySelectorAll('#invoice2csv input[name="target"]')[1].checked = true;
			} else if (syntax == "SME-COMMON") {
				document.querySelectorAll('#invoice2csv input[name="syntax"]')[1].checked = true;
				document.querySelectorAll('#invoice2csv input[name="target"]')[0].checked = true;
			}
			if (f && f.name) {
				let xmlfile = f.name;
				document.querySelector('#invoice2csv #xml_title .name').innerHTML = syntax + ': ' + xmlfile;
				document.querySelector('#invoice2csv #xml_area').textContent = contents;
			}
		}
	}

	function readSelectedFile(f) {
		if (f) {
			var r = new FileReader();
			r.onload = function (e) {
				var contents = e.target.result;
				if (f.name.indexOf(".csv") > 0) {
					document.querySelector('#csv2invoice #csv_title .name').innerHTML = f.name;
					fillTable(contents, '#csv2invoice #csv_table', '');
				} else {
					var _contents = contents.substring(contents.indexOf(">") + 1, 100);
					let start = 1 + _contents.indexOf("<");
					let target = _contents.substring(start);
					syntax = "";
					if (0 == target.indexOf("Invoice")) {
						syntax = "JP-PINT";
					}
					else if (0 == target.indexOf("rsm:SME")) {
						syntax = "SME-COMMON";
					}
					updateSyntax(syntax,f);
				}
			}
			r.readAsText(f);
		} else {
			snackbar.close();
			alert("Failed to load file");
		}
	}

	function _convertCSVtoJSON(csv, column) {
		if (!csv || 0 == csv.length) {
			return null;
		}

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
					id = headers[j].trim();
				}
				obj[id] = _unescape_comma(currentline[j]).trim();
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
		let table = document.querySelector(table_id);
		let thead = table.querySelector('thead');
		thead.innerHTML = '';
		let tbody = table.querySelector('tbody');
		tbody.innerHTML = '';
		if (!contents) {
			return;
		}
		let json = _convertCSVtoJSON(contents, column);
		let header = Object.keys(json[0])
		let tr = thead.insertRow();
		let td_id = tr.insertCell();
		tr.append(td_id);
		td_id.setAttribute('scope', 'col');
		td_id.innerHTML = 'ID';
		if (column) {
			let td_term = tr.insertCell();
			tr.append(td_term);
			td_term.setAttribute('scope', 'col');
			td_term.innerHTML = '項目名';
		}
		for (var i = 1; i < header.length; i++) {
			let td = tr.insertCell();
			td.setAttribute('scope', 'col');
			td.style = 'text-align: center;';
			td.innerHTML = header[i];
		}
		for (let row of json) {
			let tr = tbody.insertRow();
			let td_id = tr.insertCell();
			tr.append(td_id);
			td_id.setAttribute('scope', 'row')
			let core_id = row[header[0]];
			td_id.innerHTML = core_id;
			if (column) {
				let td_term = tr.insertCell();
				tr.append(td_term);
				let core_term = jp_pint_binding[core_id]['businessTerm'];
				td_term.innerHTML = core_term;
			}
			for (var i = 1; i < header.length; i++) {
				let td = tr.insertCell();
				td.innerHTML = row[header[i]];
			}
		}
	}

	function updateNameURL(selector, file, option) {
		document.querySelector(selector+' .fa').classList.remove('d-none');
		let name = file.substring(1+file.lastIndexOf('/'));
		let url = location.origin + '/core-japan/server/' + file;
		let title = document.querySelector(selector+' .name');
		if (title) {
			if (option) {
				title.innerHTML = name + '(' + option + ')';
			} else {
				title.innerHTML = name;
			}
		}
		let anchor = document.querySelector(selector+' .url');
		if (anchor) {
			anchor.setAttribute('href', url);
			anchor.setAttribute('download', name);
		}
	}

	function source2target(evt) {
		updateNameURL('#source2target #target_title','','');
		let target_area = document.querySelector('#source2target #target_area');
		if (target_area) {
			target_area.textContent = ''
		}
		updateNameURL('#source2target #transposed_title','','縦横転置');
		fillTable('','#source2target #transposed_table','C')
		updateNameURL('#source2target #csv_title','','')
		fillTable('','#source2target #csv_table','');
		updateNameURL('#source2target #xml_title','','')
		let xml_area = document.querySelector('#source2target #xml_area');
		if (xml_area) {
			xml_area.textContent = '';
		}
		const formData = new FormData();
		let file = document.querySelector('#source2target-form input[type="file"]').files[0];
		if (!file) {
			file = evt.target.querySelector('#source2target-form input[type="file"]').files[0];
		}
		if (file) {
			formData.append('file', file);
		} else {
			let selected = document.querySelector('#source2target #selected_file').value;
			if (selected && 'initial'!=selected) {
				let file_name = selected.substring(1+selected.indexOf(':'));
				formData.append('selected', file_name);
			} else {
				snackbar.open({'message':'ファイルを指定してください','type':'danger'});
				return;
			}
		}
		source = document.querySelector('#source2target-form input[name="syntax"]:checked').value;
		target = document.querySelector('#source2target-form input[name="target"]:checked').value;
		formData.append("syntax", source + '_' + target);
		uuid = document.getElementById('uuid').value;
		if (uuid) {
			formData.append("uuid", uuid);
		}
		snackbar.open({'message':'<i class="fa fa-cog fa-spin"></i> 変換中','type':'info'});
		fetch(base_url+'/server/source2target.php', {
			method: 'POST',
			body: formData
		})
			.then(response => {
				return response.text();
			})
			.then(data => {
				snackbar.close();
				if (0 == data.indexOf("ERROR") || '{' != data.substring(0, 1)) {
					snackbar.close();
					alert(data)
				}
				else {
					try {
						let response = JSON.parse(data);
						syntax = response.syntax;
						uuid = response.uuid;
						document.getElementById('uuid').value = uuid;
						localStorage.setItem('uuid', uuid);
						let source = response.source;
						let target = response.target;
						let source_xml = response.source_xml;
						let csv_file = response.csv_file;
						let transposed_file = response.transposed_file;
						let target_xml = response.target_xml;
						let xml_contents = response.source_contents;
						let csv_contents = response.csv_contents;
						let transposed_contents = response.transposed_contents;
						let target_contents = response.target_contents;
						updateNameURL('#source2target #target_title',target_xml,target);
						if (target_area) {
							target_area.textContent = formatXml(target_contents);
						}
						updateNameURL('#source2target #transposed_title',transposed_file,'縦横転置');
						fillTable(transposed_contents,'#source2target #transposed_table','C')
						updateNameURL('#source2target #csv_title',csv_file,'')
						fillTable(csv_contents,'#source2target #csv_table','');
						updateNameURL('#source2target #xml_title',source_xml,source)
						if (xml_area) {
							xml_area.textContent = xml_contents;
						}
					} catch (error) {
						snackbar.close();
						alert('受信メッセージの処理に失敗しました', error);
					}
				}
			})
			.catch(error => {
				snackbar.close();
				alert('通信に失敗しました', error);
			});
	}

	function invoice2csv(evt) {
		updateNameURL('#invoice2csv #transposed_title','','縦横転置')
		fillTable('', '#invoice2csv #transposed_table', 'C')
		updateNameURL('#invoice2csv #csv_title','','')
		fillTable('', '#invoice2csv #csv_table', '');
		updateNameURL('#invoice2csv #xml_title','','');
		document.querySelector('#invoice2csv #xml_area').textContent = '';
		const formData = new FormData();
		let file = document.querySelector('#invoice2csv-form input[type="file"]').files[0];
		if (!file) {
			file = evt.target.querySelector('#invoice2csv-form input[type="file"]').files[0];
		}
		if (file) {
			formData.append('file', file);
		} else {
			let selected = document.querySelector('#invoice2csv #selected_file').value;
			if (selected && 'initial'!=selected) {
				formData.append('selected', selected);
			} else {
				snackbar.open({'message':'ファイルを指定してください','type':'danger'});
				return;
			}
		}
		syntax = document.querySelector('#invoice2csv-form input[name="syntax"]:checked').value;
		formData.append("syntax", syntax);
		uuid = document.getElementById('uuid').value;
		if (uuid) {
			formData.append("uuid", uuid);
		}
		snackbar.open({'message':'<i class="fa fa-cog fa-spin"></i> 変換中','type':'info'});
		fetch(base_url+'/server/invoice2csv.php', {
			method: 'POST',
			body: formData
		})
			.then(response => {
				return response.text();
			})
			.then(data => {
				snackbar.close();
				if (0 == data.indexOf("ERROR") || '{' != data.substring(0, 1)) {
					snackbar.close();
					alert(data)
				}
				else {
					try {
						let response = JSON.parse(data);
						syntax = response.syntax;
						uuid = response.uuid;
						uuid = response.uuid;
						document.getElementById('uuid').value = uuid;
						localStorage.setItem('uuid', uuid);
						let csv_file = response.csv_file;
						let transposed_file = response.transposed_file;
						let xml_file = response.xml_file;
						let xml_contents = response.xml_contents;
						let csv_contents = response.csv_contents;
						let transposed_contents = response.transposed_contents;
						updateNameURL('#invoice2csv #transposed_title',transposed_file,'縦横転置')
						fillTable(transposed_contents, '#invoice2csv #transposed_table', 'C')
						updateNameURL('#invoice2csv #csv_title',csv_file,'')
						fillTable(csv_contents, '#invoice2csv #csv_table', '');
						updateNameURL('#invoice2csv #xml_title',xml_file,syntax);
						document.querySelector('#invoice2csv #xml_area').textContent = xml_contents;
					}
					catch (error) {
						snackbar.close();
						alert('受信メッセージの処理に失敗しました', error);
					}
				}
			})
			.catch(error => {
				snackbar.close();
				alert('通信に失敗しました', error);
			});
	}

	function csv2invoice(evt) {
		updateNameURL('#csv2invoice #xml_title','','')
		let xml_area = document.querySelector('#csv2invoice #xml_area');
		if (xml_area) {
			xml_area.textContent = '';
		}
		const formData = new FormData();
		let file = document.querySelector('#csv2invoice-form input[type="file"]').files[0];
		if (!file) {
			file = evt.target.querySelector('#csv2invoice-form input[type="file"]').files[0];
		} 
		if (file) {
			formData.append('file', file);
		} else {
			snackbar.open({'message':'ファイルを指定してください','type':'danger'});
			return;
		}
		formData.append('file', file);
		syntax = document.querySelector('#csv2invoice-form input[name="syntax"]:checked').value;
		formData.append("syntax", syntax);
		uuid = document.getElementById('uuid').value;
		if (uuid) {
			formData.append("uuid", uuid);
		}
		snackbar.open({'message':'<i class="fa fa-cog fa-spin"></i> 変換中','type':'info'});
		fetch(base_url+'/server/csv2invoice.php', {
			method: 'POST',
			body: formData
		})
			.then(response => {
				return response.text();
			})
			.then(data => {
				snackbar.close();
				if (0 == data.indexOf("ERROR") || '{' != data.substring(0, 1)) {
					snackbar.close();
					alert(data)
				}
				else {
					try {
						let response = JSON.parse(data);
						syntax = response.syntax;
						uuid = response.uuid;
						uuid = response.uuid;
						document.getElementById('uuid').value = uuid;
						localStorage.setItem('uuid', uuid);
						let csv_file = response.csv_file;
						let xml_file = response.xml_file;
						let xml_contents = response.xml_contents;
						updateNameURL('#csv2invoice #xml_title',xml_file,syntax)
						if (xml_area) {
							xml_area.textContent = formatXml(xml_contents);
						}
					} catch (error) {
						snackbar.close();
						alert('受信メッセージの処理に失敗しました', error);
					}
				}
			})
			.catch(error => {
				snackbar.close();
				alert('通信に失敗しました', error);
			});
	}

	function initModule() {
		base_url = location.href;
		base_url = base_url.substring(0,base_url.lastIndexOf('/'));

		uuid = localStorage.getItem('uuid');
		if (uuid) {
			document.getElementById('uuid').value = uuid;
		}

		document.getElementById('source2target-form').addEventListener('submit', e => {
			e.preventDefault();
			source2target(e);
		});

		document.getElementById('invoice2csv-form').addEventListener('submit', e => {
			e.preventDefault();
			invoice2csv(e);
		});

		document.getElementById('csv2invoice-form').addEventListener('submit', e => {
			e.preventDefault();
			csv2invoice(e);
		});

		document.querySelector('#source2target-form input[type="file"]').addEventListener('change', e => {
			e.preventDefault();
			const file = document.querySelector('#source2target-form input[type="file"]').files[0];
			if (!file) {
				file = etarget.querySelector('#source2target-form input[type="file"]').files[0];
			}
			readSelectedFile(file);
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

		document.querySelector('#source2target #selected_file').addEventListener('change', e => {
			e.preventDefault();
			let upload = document.querySelector('#source2target #upload_file');
			let option = document.querySelector('#source2target #selected_file').value;
			if ('initial' == option) {
				upload.classList.remove('d-none');
			} else {
				upload.classList.add('d-none');
			}
			let syntax = option.substring(0,option.indexOf(':'));
			updateSyntax(syntax);
		});

		document.querySelector('#source2target #csv_button').addEventListener('click', e => {
			e.preventDefault();
			document.querySelector('#source2target #transposed').classList.add('d-none');
			document.querySelector('#source2target .tidy_csv').classList.add('d-none');
			document.querySelector('#source2target #csv').classList.remove('d-none');
			document.querySelector('#source2target #csv_button').classList.add('active');
			document.querySelector('#source2target #csv_button').classList.add('bg-secondary');
			document.querySelector('#source2target #csv_button').classList.remove('bg-light');
			document.querySelector('#source2target #transposed_button').classList.remove('active');
			document.querySelector('#source2target #transposed_button').classList.add('bg-light');
			document.querySelector('#source2target #transposed_button').classList.remove('bg-secondary');
		});

		document.querySelector('#source2target #transposed_button').addEventListener('click', e => {
			e.preventDefault();
			document.querySelector('#source2target #transposed').classList.remove('d-none');
			document.querySelector('#source2target .tidy_csv').classList.remove('d-none');
			document.querySelector('#source2target #csv').classList.add('d-none');
			document.querySelector('#source2target #csv_button').classList.remove('active');
			document.querySelector('#source2target #csv_button').classList.add('bg-lighht');
			document.querySelector('#source2target #csv_button').classList.remove('bg-secondary');
			document.querySelector('#source2target #transposed_button').classList.add('active');
			document.querySelector('#source2target #transposed_button').classList.add('bg-secondary');
			document.querySelector('#source2target #transposed_button').classList.remove('bg-light');
			document.querySelector('#source2target .tidy_csv a#core-japan').addEventListener('click', function (e) {
				e.preventDefault();
				$(this).tab('show');
				updateTransposedLabel('core-japan');
			});
			document.querySelector('#source2target .tidy_csv a#jp-pint').addEventListener('click', function (e) {
				e.preventDefault();
				$(this).tab('show');
				updateTransposedLabel('jp-pint');
			});
			document.querySelector('#source2target .tidy_csv a#jp-pint_ja').addEventListener('click', function (e) {
				e.preventDefault();
				$(this).tab('show');
				updateTransposedLabel('jp-pint_ja');
			});
			document.querySelector('#source2target .tidy_csv a#sme-common').addEventListener('click', function (e) {
				e.preventDefault();
				$(this).tab('show');
				updateTransposedLabel('sme-common');
			});
		});

		function updateTransposedLabel(mode) {
			let trs = document.querySelectorAll('#transposed_table tbody tr');
			for (tr of trs) {
				if (''==tr.firstChild.innerText) {
					continue;
				}
				let id = tr.childNodes[0].innerText;
				// let label = '';
				if (undefined==core_japan[id]) {
					core_japan[id] = {};
				}
				if (mode=='core-japan') {
					tr.childNodes[1].innerText = core_japan[id]['name'] || '(未定義)';
				} else if (mode=='jp-pint') {
					tr.childNodes[1].innerText = (core_japan[id]['pint_Id'] || '') + (core_japan[id]['pint_name'] || '(undefined)');
				} else if (mode=='jp-pint_ja') {
					tr.childNodes[1].innerText = (core_japan[id]['pint_Id'] || '') + (core_japan[id]['pint_name_ja'] || '(未定義)');
				} else if (mode=='sme-common') {
					tr.childNodes[1].innerText = (core_japan[id]['UN_CCL_ID'] || '') + (core_japan[id]['sme_name'] || '(未定義)');
				}					
			}
		}
		document.querySelector('#invoice2csv #selected_file').addEventListener('change', e => {
			e.preventDefault();
			let upload = document.querySelector('#invoice2csv #upload_file');
			let option = document.querySelector('#invoice2csv #selected_file').value;
			if ('initial' == option) {
				upload.classList.remove('d-none');
			} else {
				upload.classList.add('d-none');
			}
		});

		document.querySelector('#invoice2csv #csv_button').addEventListener('click', e => {
			e.preventDefault();
			document.querySelector('#invoice2csv #transposed').classList.add('d-none');
			document.querySelector('#invoice2csv #csv').classList.remove('d-none');
			document.querySelector('#invoice2csv #csv_button').classList.add('active');
			document.querySelector('#invoice2csv #csv_button').classList.add('bg-secondary');
			document.querySelector('#invoice2csv #csv_button').classList.remove('bg-light');
			document.querySelector('#invoice2csv #transposed_button').classList.remove('active');
			document.querySelector('#invoice2csv #transposed_button').classList.add('bg-light');
			document.querySelector('#invoice2csv #transposed_button').classList.remove('bg-secondary');
		});

		document.querySelector('#invoice2csv #transposed_button').addEventListener('click', e => {
			e.preventDefault();
			document.querySelector('#invoice2csv #transposed').classList.remove('d-none');
			document.querySelector('#invoice2csv #csv').classList.add('d-none');
			document.querySelector('#invoice2csv #csv_button').classList.remove('active');
			document.querySelector('#invoice2csv #csv_button').classList.add('bg-lighht');
			document.querySelector('#invoice2csv #csv_button').classList.remove('bg-secondary');
			document.querySelector('#invoice2csv #transposed_button').classList.add('active');
			document.querySelector('#invoice2csv #transposed_button').classList.add('bg-secondary');
			document.querySelector('#invoice2csv #transposed_button').classList.remove('bg-light');
		});

		document.querySelector('#source2target #selected_file').addEventListener('change', e => {
			e.preventDefault();
			let upload = document.querySelector('#source2target #upload_file');
			let option = document.querySelector('#source2target #selected_file').value;
			if ('initial' == option) {
				upload.classList.remove('d-none');
			} else {
				upload.classList.add('d-none');
			}
		});

		document.querySelector('#invoice2csv #selected_file').addEventListener('change', e => {
			e.preventDefault();
			let upload = document.querySelector('#invoice2csv #upload_file');
			let option = document.querySelector('#invoice2csv #selected_file').value;
			if ('initial' == option) {
				upload.classList.remove('d-none');
			} else {
				upload.classList.add('d-none');
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

		fetch(base_url+'/server/data/base/core_japan.csv')
		.then(res => res.text())
		.then(csv => {
			fillTable(csv,'#coreinvoice #core_japan_table','')
			let json = _convertCSVtoJSON(csv);
			for (let i = 0; i < json.length; i++) {
				let data = json[i];
				let id = data['id']
				core_japan[id] = {};
				core_japan[id]['name'] = data['name'];
				core_japan[id]['pint_name'] = data['pint_name'];
				core_japan[id]['pint_name_ja'] = data['pint_name_ja'];
				core_japan[id]['sme_name'] = data['sme_name'];
			}
		});

		fetch(base_url+'/server/data/base/jp_pint_binding.csv')
			.then(res => res.text())
			.then(csv => {
				fillTable(csv,'#coreinvoice #jp-pint_binding_table','')
				let json = _convertCSVtoJSON(csv);
				for (let i = 0; i < json.length; i++) {
					let data = json[i];
					let id = data['id'];
					jp_pint_binding[id] = {};
					jp_pint_binding[id]['businessTerm'] = data['businessTerm'];
					jp_pint_binding[id]['businessTerm_ja'] = data['businessTerm_ja'];
				}
			});

		fetch(base_url+'/server/data/base/sme_binding.csv')
			.then(res => res.text())
			.then(csv => {
				fillTable(csv,'#coreinvoice #sme_binding_table','')
				let json = _convertCSVtoJSON(csv);
				for (let i = 0; i < json.length; i++) {
					let data = json[i];
					let id = data['id'];
					sme_binding[id] = {};
					sme_binding[id]['businessTerm'] = data['businessTerm'];
					sme_binding[id]['businessTerm_ja'] = data['businessTerm_ja'];
				}
			});
	}

	return {
		initModule: initModule,
		invoice2csv: invoice2csv,
		csv2invoice: csv2invoice
	};
})();
// convert.js