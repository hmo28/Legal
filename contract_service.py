"""
خدمة صياغة العقود
Contract Drafting Service
"""

from typing import Dict, Any
from .base_service import BaseService
from config import DISCLAIMERS, CONTRACT_SECTIONS
from prompts import get_contract_prompt

class ContractService(BaseService):
    """خدمة صياغة العقود"""
    
    def __init__(self):
        super().__init__("contract")
    
    def process(self, details: str) -> Dict[str, Any]:
        """
        معالجة طلب صياغة العقد
        
        Args:
            details: تفاصيل العقد المطلوب
            
        Returns:
            dict: العقد المنظم
        """
        if not self.validate_input(details):
            return {
                "error": "يرجى تقديم تفاصيل العقد المطلوب"
            }
        
        if not self.is_ai_available:
            return {
                "service_type": self.service_type,
                "content": "⚠️ عذراً، مكتبة الذكاء الاصطناعي غير مثبتة.\n\nيرجى تثبيت المكتبة: pip install google-generativeai",
                "disclaimer": DISCLAIMERS[self.service_type]
            }

        # الحصول على التعليمات المناسبة
        prompt = get_contract_prompt(details)
        
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
        تنسيق مخرجات العقد
        
        Args:
            result: نص العقد من النموذج
            
        Returns:
            dict: عقد منظم
        """
        return {
            "service_type": "صياغة العقود",
            "content": result,
            "sections": CONTRACT_SECTIONS,
            "disclaimer": DISCLAIMERS[self.service_type],
            "format": "document"
        }
