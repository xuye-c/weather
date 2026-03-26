from abc import ABC, abstractmethod
from db.reader import Reader

class BaseExporter(ABC):
    """导出器基类"""
    
    def __init__(self):
        self.format_name = "base"
    
    def get_data(self, city=None, start_date=None, end_date=None):
        """获取数据"""
        if city:
            rows = Reader.get_by_city_and_range_fixed(city, start_date, end_date)
        else:
            rows = Reader.get_all()
        
        data = [
            {
                "city": r[0],
                "date": r[1],
                "temperature": r[2]
            }
            for r in rows
        ]
        return data
    
    @abstractmethod
    def export(self, city=None, start_date=None, end_date=None):
        """导出数据 """
        pass
    
    @abstractmethod
    def get_mimetype(self):
        """返回MIME类型"""
        pass
    
    @abstractmethod
    def get_file_extension(self):
        """返回文件扩展名"""
        pass