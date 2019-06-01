import json, os
from .Exporter import Exporter

class JSONExporter(Exporter):
	def __init__(self, config):
		super(JSONExporter, self).__init__(config)
		self.name = "json"
	
	def export_json(self, tabel):
		return tabel

	def dump_json(self, name, data):
		out_path = os.path.join(self.config['output'], self.name, name + '.json')
		if not os.path.isdir(os.path.dirname(out_path)):
				os.makedirs(os.path.dirname(out_path))
		indent = self.config['exporter']['json']['indent']
		json.dump(
			data,
			open(out_path, 'w', encoding="utf8"),
			sort_keys=True, ensure_ascii=False,
			indent=indent
		)
		
	def parse_tables(self, tables):
		for name in tables:
			self.tables[name] = self.export_json(tables[name])
			
	def dump(self):
		for name in self.tables:
			self.dump_json(name, self.tables[name])