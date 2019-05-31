#!/usr/bin/env python
#coding=utf-8

import os, json, xlrd
from src.JSONExporter import JSONExporter
from src.TypeScriptExporter import TypeScriptExporter
from src.parser import load_tabels

CONFIG = json.load(open('config.json', 'r',  encoding='utf8'))
def main():
	exporters = []
	for name in CONFIG['exporter']:
		if name == 'json': exporters.append(JSONExporter(CONFIG))
		if name == 'typescript': exporters.append(TypeScriptExporter(CONFIG))
	if not os.path.isdir(CONFIG['output']):
		os.makedirs(CONFIG['output'])
	for input in CONFIG['input']:
		tables = load_tabels(input['file'], input['encode'])
		for exporter in exporters:
			exporter.parse_tables(tables)
	for exporter in exporters:
		exporter.dump()
	print("完成")

if __name__ == '__main__':
	main()


