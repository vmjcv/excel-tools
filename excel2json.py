#!/usr/bin/env python
#coding=utf-8

import os, json, xlrd

# 读取原始数据
def read_table_file(file):
    if os.path.isfile(file):
        tables = {}
        xlrd.Book.encoding = "GBK"
        data = xlrd.open_workbook(file)
        for sheet_name in data.sheet_names():
            table_data = []
            sheet = data.sheet_by_name(sheet_name)
            if sheet.nrows < 2:
                # 忽略空表
                continue
            for i in range(sheet.nrows):
                table_data.append(sheet.row_values(i))
            tables[sheet_name] = table_data
        return tables
    else:
        raise Exception("文件不存在: " + file)

# 原始数据组装成json字典
def json_exporter(data):
    title = {}
    json_data = []
    raw_title = data[0]
    for i in range(len(raw_title)):
        title[i] = raw_title[i]
    for i in range(1, len(data)):
        json_row = {}
        raw_row = data[i]
        for j in range(len(raw_title)):
            value = raw_row[j]
            if isinstance(value, str) and len(value.strip()) == 0:
                value = None
            elif isinstance(value, float) and value == int(value):
                value = int(value)
            key = title[j]
            if not key in json_row:
                json_row[key] = value
            else:
                if isinstance(json_row[key], list):
                    json_row[key].append(value)
                else:
                    json_row[key] = [json_row[key], value]
        json_data.append(json_row)
    return json_data


declare_file_content = ''

# TypeScript 表声明
def typescript_declare(name, table_data):
    global declare_file_content
    data = json_exporter(table_data)
    if len(data):
        body = json.dumps(data[0], ensure_ascii=False, indent=4, sort_keys=True)
        class_name = CONFIG['exporter']['typescript']['type_prefix'] + name + CONFIG['exporter']['typescript']['type_extention']
        text = 'interface {} {}'.format(class_name, body)
        declare_file_content += text + '\n\n'

# 输出声明文件
def flush_declare_files():
    global declare_file_content
    file = open(os.path.join(CONFIG['output'], 'data.d.ts'), 'w', encoding="utf8")
    declare_file_content = '// Tool generated file. DO NOT MODIFY\n' + declare_file_content
    file.write(declare_file_content)
    file.close()

# json 存储
def json_dump(data, file):
    json.dump(
        data,
        open(file, 'w', encoding="utf8"),
        sort_keys=True, ensure_ascii=False,
        indent=CONFIG['exporter']['json']['indent']
    )



CONFIG = json.load(open('config.json', 'r',  encoding='utf8'))

def main():
    if not os.path.isdir(CONFIG['output']):
        os.makedirs(CONFIG['output'])
    for file in CONFIG['input']:
        tables = read_table_file(file)
        for name in tables:
            src_prefix = os.path.splitext(os.path.basename(file))[0] + '_'
            src_prefix = ''
            out_path = os.path.join(CONFIG['output'],  src_prefix + name + '.json')
            json_dump(json_exporter(tables[name]), out_path)
            typescript_declare(name, tables[name])
    flush_declare_files()
    print("完成")

if __name__ == '__main__':
    main()


