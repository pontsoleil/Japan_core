import xml.etree.ElementTree as ET

# UBL請求書の読み込み
tree = ET.parse('invoice.xml')
root = tree.getroot()

# Invoice要素の情報を取得
invoice_id = root.findtext('.//cbc:ID', namespaces=root.nsmap)
invoice_date = root.findtext('.//cbc:IssueDate', namespaces=root.nsmap)
invoice_currency = root.findtext('.//cbc:DocumentCurrencyCode', namespaces=root.nsmap)

# InvoiceLine要素の情報を取得
invoice_lines = []
for line in root.findall('.//cac:InvoiceLine', namespaces=root.nsmap):
    line_id = line.findtext('.//cbc:ID', namespaces=root.nsmap)
    line_quantity = line.findtext('.//cbc:InvoicedQuantity', namespaces=root.nsmap)
    line_price = line.findtext('.//cbc:PriceAmount', namespaces=root.nsmap)
    invoice_lines.append({'id': line_id, 'quantity': line_quantity, 'price': line_price})

# 出力
print(f'Invoice ID: {invoice_id}')
print(f'Invoice Date: {invoice_date}')
print(f'Invoice Currency: {invoice_currency}')
for line in invoice_lines:
    print(f'Line ID: {line["id"]}, Quantity: {line["quantity"]}, Price: {line["price"]}')
