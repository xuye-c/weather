import unittest
import os
import sys

# 添加 weather_app 目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'weather_app')))

from configs.messageManager import MessageManager


class TestMessageManager(unittest.TestCase):
    
    def setUp(self):
        """每个测试前重置单例状态"""
        MessageManager._instance = None
        MessageManager._messages = {}
        MessageManager._available_languages = []
        MessageManager._current_lang = None
        MessageManager._config_dir = os.path.join(os.path.dirname(__file__), '../..', 'weather_app', 'configs')
    
    # ==================== Initialization Tests ====================
    
    def test_init_with_multiple_languages(self):
        """测试有多个语言文件时的初始化"""
        mm = MessageManager()
        
        languages = mm.get_available_languages()
        self.assertIn('en', languages)
        self.assertIn('zh', languages)
    
    def test_init_with_env_language(self):
        """测试环境变量设置语言"""
        os.environ['APP_LANG'] = 'zh'
        
        mm = MessageManager()
        
        self.assertEqual(mm.get_language(), 'zh')
        self.assertEqual(mm.get("success.insert"), "天气记录添加成功")
        
        del os.environ['APP_LANG']
    
    def test_init_with_invalid_env_language(self):
        """测试环境变量设置无效语言"""
        os.environ['APP_LANG'] = 'invalid'
        
        mm = MessageManager()
        
        self.assertEqual(mm.get_language(), 'en')
        
        del os.environ['APP_LANG']
    
    # ==================== Get Message Tests ====================
    
    def test_get_simple_message(self):
        """测试获取简单消息"""
        mm = MessageManager()
        
        result = mm.get("success.insert")
        self.assertEqual(result, "Weather record added successfully")
    
    def test_get_nested_message(self):
        """测试获取嵌套消息"""
        mm = MessageManager()
        
        result = mm.get("error.database.duplicate")
        self.assertEqual(result, "Record already exists")
    
    def test_get_message_with_formatting(self):
        """测试带格式化的消息（注意：你的消息文件中可能没有格式化消息）"""
        mm = MessageManager()
        
        # 如果你的消息文件中有格式化消息，可以测试
        # 如果没有，这个测试可以跳过或修改
        result = mm.get("success.insert")
        self.assertIsInstance(result, str)
    
    def test_get_nonexistent_key(self):
        """测试获取不存在的key"""
        mm = MessageManager()
        
        result = mm.get("nonexistent.key")
        self.assertEqual(result, "Message key not found: nonexistent.key")
    
    def test_get_with_partial_key_match(self):
        """测试部分匹配的key"""
        mm = MessageManager()
        
        result = mm.get("error.database")
        # 应该返回整个字典的字符串表示
        self.assertIn("duplicate", result)
    
    # ==================== Language Switch Tests ====================
    
    def test_set_language_success(self):
        """测试成功切换语言"""
        mm = MessageManager()
        
        self.assertEqual(mm.get("success.insert"), "Weather record added successfully")
        
        result = mm.set_language('zh')
        
        self.assertTrue(result)
        self.assertEqual(mm.get_language(), 'zh')
        self.assertEqual(mm.get("success.insert"), "天气记录添加成功")
    
    def test_set_language_invalid(self):
        """测试切换无效语言"""
        mm = MessageManager()
        
        result = mm.set_language('invalid')
        
        self.assertFalse(result)
        self.assertEqual(mm.get_language(), 'en')
    
    def test_switch_language_multiple_times(self):
        """测试多次切换语言"""
        mm = MessageManager()
        
        mm.set_language('zh')
        self.assertEqual(mm.get("success.insert"), "天气记录添加成功")
        
        mm.set_language('en')
        self.assertEqual(mm.get("success.insert"), "Weather record added successfully")
    
    # ==================== Edge Cases Tests ====================
    
    def test_singleton_pattern(self):
        """测试单例模式"""
        mm1 = MessageManager()
        mm2 = MessageManager()
        
        self.assertIs(mm1, mm2)
    
    def test_get_available_languages_returns_copy(self):
        """测试返回可用语言的副本"""
        mm = MessageManager()
        
        languages = mm.get_available_languages()
        languages.append('test')
        
        # 原始列表不应被修改
        self.assertNotIn('test', mm.get_available_languages())
    
    def test_get_with_unicode_characters(self):
        """测试Unicode字符"""
        mm = MessageManager()
        mm.set_language('zh')
        
        result = mm.get("error.input.city_empty")
        self.assertEqual(result, "城市名不可为空")
    
    def test_reload(self):
        """测试重新加载"""
        mm = MessageManager()
        
        original = mm.get("success.insert")
        
        mm.reload()
        
        self.assertEqual(mm.get("success.insert"), original)


if __name__ == "__main__":
    unittest.main()