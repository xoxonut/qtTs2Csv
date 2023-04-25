import csv
import xml.etree.ElementTree as ET
import sys

if(len(sys.argv) != 4):
    print("Usage: python3 ts2csv.py <csv file> <template ts file> <output ts file>\nTemplate ts  must be the template of csv file")
    exit(1)  

in_csv = sys.argv[1]
# 讀取CSV檔案
with open(in_csv, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    data = {}
    for i, row in enumerate(reader):
        if i == 0:
            continue
        content = row[0]
        if content not in data:
            data[content] = []
        data[content].append(row)

# 讀取XML檔案
template_ts=sys.argv[2]
tree = ET.parse(template_ts)
root = tree.getroot()

# 將資料寫回XML檔案
for context in root.iter('context'):
    content = context.find('name').text if context.find('name') is not None else ''
    if content in data:
        for i, message in enumerate(context.iter('message')):
            if i < len(data[content]):
                row = data[content][i]
                source = message.find('source')
                if source is not None:
                    source.text = row[1]
                translation = message.find('translation')
                if translation is not None:
                    translation.text = row[2]

# 寫回XML檔案，包含 XML 宣告及 DOCTYPE
out_ts=sys.argv[3]
with open(out_ts, 'wb') as f:
    f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
    f.write(b'<!DOCTYPE TS>\n')
    ET.ElementTree(root).write(f, encoding='utf-8')
