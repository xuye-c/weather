import csv
import io
from .base_exporter import BaseExporter

class CSVExporter(BaseExporter):
    """CSV格式导出器"""
    
    def __init__(self):
        super().__init__()
        self.format_name = "csv"
    
    def export(self, city=None, start_date=None, end_date=None):
        data = self.get_data(city, start_date, end_date)
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # 写入表头
        writer.writerow(['City', 'Date', 'Temperature (°C)'])
        
        # 写入数据
        for row in data:
            writer.writerow([row['city'], row['date'], row['temperature']])
        
        return output.getvalue()
    
    def get_mimetype(self):
        return "text/csv"
    
    def get_file_extension(self):
        return "csv"