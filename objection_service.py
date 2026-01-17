"""
خدمة تحليل الحكم / إعداد مذكرة اعتراض
Judgment Analysis / Objection Memo Service
"""

from typing import Dict, Any
from .base_service import BaseService
from config import DISCLAIMERS, OBJECTION_SECTIONS
from prompts import get_objection_prompt

class ObjectionService(BaseService):
    """خدمة تحليل الحكم وإعداد مذكرة الاعتراض"""
    
    def __init__(self):
        super().__init__("objection")
    
    def process(self, details: str) -> Dict[str, Any]:
        """
        معالجة طلب تحليل الحكم وإعداد مذكرة الاعتراض
        
        Args:
            details: تفاصيل الحكم المراد الاعتراض عليه
            
        Returns:
            dict: مذكرة الاعتراض المنظمة
        """
        if not self.validate_input(details):
            return {
                "error": "يرجى تقديم تفاصيل الحكم المراد الاعتراض عليه"
            }
        
        if not self.is_ai_available:
            return {
                "service_type": self.service_type,
                "content": "⚠️ عذراً، مكتبة الذكاء الاصطناعي غير مثبتة.\n\nيرجى تثبيت المكتبة: pip install google-generativeai",
                "disclaimer": DISCLAIMERS[self.service_type]
            }

        # الحصول على التعليمات المناسبة
        prompt = get_objection_prompt(details)
        
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
        تنسيق مخرجات مذكرة الاعتراض
        
        Args:
            result: نص مذكرة الاعتراض من النموذج
            
        Returns:
            dict: مذكرة اعتراض منظمة
        """
        return {
            "service_type": "تحليل الحكم / إعداد مذكرة اعتراض",
            "content": result,
            "sections": OBJECTION_SECTIONS,
            "disclaimer": DISCLAIMERS[self.service_type],
            "format": "document"
        }
