from datetime import datetime
from .base_exporter import BaseExporter

class MarkdownExporter(BaseExporter):
    """Markdown格式导出器"""
    
    def __init__(self):
        super().__init__()
        self.format_name = "markdown"
    
    def export(self, city=None, start_date=None, end_date=None):
        data = self.get_data(city, start_date, end_date)
        
        output = []
        
        # 标题
        output.append("# Weather Records Export")
        output.append(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        output.append(f"*Total Records: {len(data)}*")
        output.append("")
        
        if city:
            output.append(f"**Filtered by city:** {city}")
            output.append("")
        
        if start_date or end_date:
            date_range = []
            if start_date:
                date_range.append(f"from {start_date}")
            if end_date:
                date_range.append(f"to {end_date}")
            output.append(f"**Date range:** {' '.join(date_range)}")
            output.append("")
        
        # 表格
        output.append("| City | Date | Temperature (°C) |")
        output.append("|------|------|-----------------|")
        
        for record in data:
            output.append(f"| {record['city']} | {record['date']} | {record['temperature']} |")
        
        output.append("")
        output.append("---")
        output.append(f"*Exported from Weather API Service*")
        
        return "\n".join(output)
    
    def get_mimetype(self):
        return "text/markdown"
    
    def get_file_extension(self):
        return "md"