"""
خدمة المذكرات القانونية
Legal Memo Service
"""

from typing import Dict, Any
from .base_service import BaseService
from config import DISCLAIMERS, MEMO_SECTIONS
from prompts import get_memo_prompt

class MemoService(BaseService):
    """خدمة المذكرات القانونية"""
    
    def __init__(self):
        super().__init__("memo")
    
    def process(self, details: str) -> Dict[str, Any]:
        """
        معالجة طلب إعداد المذكرة القانونية
        
        Args:
            details: تفاصيل المذكرة المطلوبة
            
        Returns:
            dict: المذكرة المنظمة
        """
        if not self.validate_input(details):
            return {
                "error": "يرجى تقديم تفاصيل المذكرة القانونية المطلوبة"
            }
        
        if not self.is_ai_available:
            return {
                "service_type": self.service_type,
                "content": "⚠️ عذراً، مكتبة الذكاء الاصطناعي غير مثبتة.\n\nيرجى تثبيت المكتبة: pip install google-generativeai",
                "disclaimer": DISCLAIMERS[self.service_type]
            }

        # الحصول على التعليمات المناسبة
        prompt = get_memo_prompt(details)
        
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
        """
        تنسيق مخرجات المذكرة
        
        Args:
            result: نص المذكرة من النموذج
            
        Returns:
            dict: مذكرة منظمة
        """
        return {
            "service_type": "المذكرات القانونية",
            "content": result,
            "sections": MEMO_SECTIONS,
            "disclaimer": DISCLAIMERS[self.service_type],
            "format": "document"
        }
