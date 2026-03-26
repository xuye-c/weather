import json
from .base_exporter import BaseExporter
from db.reader import Reader

class JSONExporter(BaseExporter):
    """JSON格式导出器"""
    
    def __init__(self):
        super().__init__()
        self.format_name = "json"
    
    def export(self, city=None, start_date=None, end_date=None):     
        data = self.get_data(city, start_date, end_date)
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def get_mimetype(self):
        return "application/json"
    
    def get_file_extension(self):
        return "json"