from .json_exporter import JSONExporter
from .csv_exporter import CSVExporter
from .xml_exporter import XMLExporter
from .markdown_exporter import MarkdownExporter

class ExportManager:
    """导出管理器 - 统一调度所有导出器"""
    
    def __init__(self):
        self.exporters = {
            'json': JSONExporter(),
            'csv': CSVExporter(),
            'xml': XMLExporter(),
            'markdown': MarkdownExporter(),
        }
    
    def get_supported_formats(self):
        """返回支持的导出格式列表"""
        return list(self.exporters.keys())
    
    def export(self, format_name, city=None, start_date=None, end_date=None):
        """
        统一导出接口
        返回: (content, mimetype, file_extension, error_message)
        """
        if format_name not in self.exporters:
            return None, None, None, f"Unsupported format: {format_name}"
        
        exporter = self.exporters[format_name]
        
        # 检查PDF是否可用
        if format_name == 'pdf' and hasattr(exporter, 'is_available'):
            if not exporter.is_available():
                return None, None, None, "PDF export requires reportlab library. Please install: pip install reportlab"
        
        try:
            content = exporter.export(city, start_date, end_date)
            if content is None:
                return None, None, None, f"Failed to export {format_name} format"
            
            mimetype = exporter.get_mimetype()
            extension = exporter.get_file_extension()
            return content, mimetype, extension, None
            
        except Exception as e:
            return None, None, None, f"Export error: {str(e)}"
    
    def get_exporter_info(self, format_name):
        """获取导出器信息"""
        if format_name not in self.exporters:
            return None
        
        exporter = self.exporters[format_name]
        info = {
            'format': format_name,
            'mimetype': exporter.get_mimetype(),
            'extension': exporter.get_file_extension()
        }
        
        if format_name == 'pdf' and hasattr(exporter, 'is_available'):
            info['available'] = exporter.is_available()
        
        return info