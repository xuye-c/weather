import json
import os
from typing import Optional, Dict, Any, List

class MessageManager:
    """
    Multilanguage Supporter
    """
    _instance = None
    _messages: Dict[str, Any] = {}
    _available_languages: List[str] = []
    _current_lang: str = None
    _config_dir: str = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_manager()
        return cls._instance
    
    def _init_manager(self):
        self._config_dir = os.path.dirname(__file__)
        self._scan_available_languages()
        env_lang = os.getenv('APP_LANG', '')
        if env_lang in self._available_languages:
            self._current_lang = env_lang
        else:
            self._current_lang = self._available_languages[0] if self._available_languages else 'en'
        
        self._load_messages()
    
    def _scan_available_languages(self):
        self._available_languages = []
        
        if not os.path.exists(self._config_dir):
            return
        
        for filename in os.listdir(self._config_dir):
            if filename.startswith('messages_') and filename.endswith('.json'):
                # 提取语言代码: messages_zh.json -> zh
                lang_code = filename[9:-5] 
                self._available_languages.append(lang_code)
        
        self._available_languages.sort()
    
    def _load_messages(self):
        if not self._current_lang:
            return
        
        message_file = os.path.join(self._config_dir, f'messages_{self._current_lang}.json')
        
        try:
            with open(message_file, 'r', encoding='utf-8') as f:
                self._messages = json.load(f)
        except FileNotFoundError:
            # 如果找不到，尝试加载第一个可用语言
            if self._available_languages and self._current_lang != self._available_languages[0]:
                self._current_lang = self._available_languages[0]
                self._load_messages()
            else:
                self._messages = {}
    
    def get(self, key: str, **kwargs) -> str:
        """
        获取消息
        Args:
            key: message keys, e.g. 'error.database.integrity'
            **kwargs: idex
        Returns:
            structured message string
        """
        keys = key.split('.')
        value = self._messages
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return f"Message key not found: {key}"
            else:
                return f"Invalid message structure for key: {key}"
        
        if value is None:
            return f"Message key not found: {key}"
        
        if isinstance(value, str) and kwargs:
            try:
                return value.format(**kwargs)
            except KeyError as e:
                return f"Missing format parameter {e} for message: {key}"
        
        return value if isinstance(value, str) else str(value)
    
    def set_language(self, lang: str) -> bool:
        """
        language switch
        Args:
            lang: language index
        Returns:
            bool: True if switched successfully
        """
        if lang in self._available_languages:
            self._current_lang = lang
            self._load_messages()
            return True
        return False
    
    def get_language(self) -> str:
        """return current language"""
        return self._current_lang
    
    def get_available_languages(self) -> List[str]:
        """return all available langauges"""
        return self._available_languages.copy()
    
    def reload(self):
        """reload language resources"""
        self._scan_available_languages()
        if self._current_lang not in self._available_languages:
            self._current_lang = self._available_languages[0] if self._available_languages else 'zh'
        self._load_messages()
