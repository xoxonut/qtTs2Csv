import csv
import xml.etree.ElementTree as ET
import sys

if(len(sys.argv) != 2):
    print("Usage: python3 ts2csv.py <ts file>")
    exit(1)   
    

ts_name = sys.argv[1]

# 讀取XML檔案
tree = ET.parse(ts_name)
root = tree.getroot()

# 準備CSV檔案
with open(ts_name[:-2]+'csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['content','source', 'translation'])

    # 解析XML檔案並寫入CSV檔案
    for context in root.iter('context'):
        content = context.find('name').text if context.find('name') is not None else ''
        for message in context.iter('message'):
            source = message.find('source').text if message.find('source') is not None else ''
            translation = message.find('translation').text if message.find('translation') is not None else ''
            writer.writerow([content,source, translation])
