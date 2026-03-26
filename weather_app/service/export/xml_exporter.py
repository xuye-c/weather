import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
from .base_exporter import BaseExporter

class XMLExporter(BaseExporter):
    """XML格式导出器"""
    
    def __init__(self):
        super().__init__()
        self.format_name = "xml"
    
    def export(self, city=None, start_date=None, end_date=None):
        data = self.get_data(city, start_date, end_date)
        
        # 创建根元素
        root = ET.Element('weather_records')
        root.set('export_date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        root.set('record_count', str(len(data)))
        
        for record in data:
            record_elem = ET.SubElement(root, 'record')
            
            city_elem = ET.SubElement(record_elem, 'city')
            city_elem.text = record['city']
            
            date_elem = ET.SubElement(record_elem, 'date')
            date_elem.text = record['date']
            
            temp_elem = ET.SubElement(record_elem, 'temperature')
            temp_elem.text = str(record['temperature'])
            temp_elem.set('unit', 'celsius')
        
        # 格式化输出
        rough_string = ET.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
    def get_mimetype(self):
        return "application/xml"
    
    def get_file_extension(self):
        return "xml"