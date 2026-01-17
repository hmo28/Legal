"""
خدمة المحادثة القانونية الذكية
Smart Legal Chat Service
"""

from typing import Dict, Any
from .base_service import BaseService
from config import DISCLAIMERS
from prompts import get_chat_prompt

class ChatService(BaseService):
    """خدمة المحادثة القانونية الذكية"""
    
    def __init__(self):
        super().__init__("chat")
    
    def process(self, details: str) -> Dict[str, Any]:
        """
        معالجة رسالة المحادثة
        
        Args:
            details: رسالة المستخدم
            
        Returns:
            dict: رد الذكاء الاصطناعي
        """
        if not self.validate_input(details):
            return {
                "error": "يرجى كتابة رسالة"
            }
        
        if not self.is_ai_available:
            return {
                "service_type": self.service_type,
                "content": "⚠️ عذراً، مكتبة الذكاء الاصطناعي غير مثبتة.\n\nيرجى تثبيت المكتبة: pip install google-generativeai",
                "disclaimer": DISCLAIMERS[self.service_type]
            }

        # الحصول على التعليمات المناسبة
        prompt = get_chat_prompt(details)
        
        ai_response = self._call_ai_model(prompt)
        
        if ai_response:
            return {
                "service_type": self.service_type,
                "content": ai_response
            }

        return {
            "service_type": self.service_type,
            "content": "⚠️ تعذر الاتصال بخدمة الذكاء الاصطناعي.",
            "disclaimer": DISCLAIMERS[self.service_type]
        }
    
    def format_output(self, result: str) -> Dict[str, Any]:
        """تنسيق مخرجات المحادثة"""
        return {
            "service_type": "المساعد القانوني الذكي",
            "content": result,
            "disclaimer": DISCLAIMERS[self.service_type],
            "format": "chat"
        }