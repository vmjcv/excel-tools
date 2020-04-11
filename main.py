#!/usr/bin/env python
#coding=utf-8

import os, json, xlrd
from src.JSONExporter import JSONExporter
from src.TypeScriptExporter import TypeScriptExporter
from src.GDScriptExporter import GDScriptExporter
from src.CSharpExporter import CSharpExporter
from src.parser import load_tabels

CONFIG = json.load(open('config.json', 'r',  encoding='utf8'))
def main():
	exporters = []
	for name in CONFIG['exporter']:
		if name == 'json' and CONFIG['exporter'][name]['enabled']: exporters.append(JSONExporter(CONFIG))
		if name == 'typescript' and CONFIG['exporter'][name]['enabled']: exporters.append(TypeScriptExporter(CONFIG))
		if name == 'gdscript' and CONFIG['exporter'][name]['enabled']: exporters.append(GDScriptExporter(CONFIG))
		if name == 'csharp' and CONFIG['exporter'][name]['enabled']: exporters.append(CSharpExporter(CONFIG))
	if not os.path.isdir(CONFIG['output']): os.makedirs(CONFIG['output'])
	for input in CONFIG['input']:
		print("Parsing file", input['file'], "with encoding", input['encode'])
		tables = load_tabels(input['file'], input['encode'])
		for exporter in exporters:
			exporter.parse_tables(tables)
	for exporter in exporters:
		print("Exporting for", exporter.name)
		exporter.dump()
	print("All Done!")

if __name__ == '__main__':
	main()


