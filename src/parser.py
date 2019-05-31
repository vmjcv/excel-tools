#!/usr/bin/env python
#coding=utf-8

import os, json, xlrd

	
# 读取原始数据
def load_tabels(file, encode):
	if os.path.isfile(file):
		tables = {}
		xlrd.Book.encoding = encode
		data = xlrd.open_workbook(file)
		for sheet_name in data.sheet_names():
			table_data = []
			sheet = data.sheet_by_name(sheet_name)
			title_row = sheet.row_values(0)
			if sheet.nrows < 2 or not title_row:
				continue # 忽略空表
			for i in range(1, sheet.nrows):
				table_data.append(process_row(title_row, sheet.row_values(i)))
			tables[sheet_name] = table_data
		return tables
	else:
		raise Exception("文件不存在: " + file)
		
def process_row(title_row, row):
	data = {}
	for i in range(len(title_row)):
		key = title_row[i]
		if len(key.strip()) == 0:
			continue
		value = row[i]
		if isinstance(value, str) and len(value.strip()) == 0:
			value = None
		elif isinstance(value, float) and value == int(value):
			value = int(value)
		if key in data:
			if isinstance(data[key], list):
				data[key].append(value)
			else:
				data[key] = [data[key], value]
		else:
			data[key] = value
	return data