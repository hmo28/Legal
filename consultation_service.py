"""
خدمة الاستشارة القانونية العامة
General Legal Consultation Service
"""

from typing import Dict, Any
from .base_service import BaseService
from config import DISCLAIMERS
from prompts import get_consultation_prompt

class ConsultationService(BaseService):
    """خدمة الاستشارة القانونية العامة"""
    
    def __init__(self):
        super().__init__("consultation")
    
    def process(self, details: str) -> Dict[str, Any]:
        if not self.validate_input(details):
            return {"error": "يرجى تقديم تفاصيل القضية"}
        
        # 1. جلب الـ Prompt من ملف prompts.py
        prompt = get_consultation_prompt(details)
        
        # 2. استدعاء الذكاء الاصطناعي (استخدام الدالة التي أضفناها في BaseService)
        ai_result = self.get_ai_response(prompt)
        
        # 3. تنسيق النتيجة النهائية
        return self.format_output(ai_result)
    
    def format_output(self, result: str) -> Dict[str, Any]:
        """
        تنسيق مخرجات الاستشارة
        
        Args:
            result: نص الاستشارة من النموذج
            
        Returns:
            dict: استشارة منظمة
        """
        return {
            "service_type": "الاستشارة القانونية العامة",
            "content": result,
            "disclaimer": DISCLAIMERS[self.service_type],
            "format": "text"
        }
