"""
خدمة تحليل مذكرة الخصم
Adversary Memo Analysis Service
"""

from typing import Dict, Any
from .base_service import BaseService
from config import DISCLAIMERS
from prompts import get_analysis_prompt

class AnalysisService(BaseService):
    """خدمة تحليل مذكرة الخصم"""
    
    def __init__(self):
        super().__init__("analysis")
    
    def process(self, details: str) -> Dict[str, Any]:
        """
        معالجة طلب تحليل مذكرة الخصم
        
        Args:
            details: نص مذكرة الخصم المراد تحليلها
            
        Returns:
            dict: التحليل المنظم
        """
        if not self.validate_input(details):
            return {
                "error": "يرجى تقديم نص مذكرة الخصم المراد تحليلها"
            }
            
        # التحقق من توفر المكتبات قبل البدء
        if not self.is_ai_available:
            return {
                "service_type": self.service_type,
                "content": "⚠️ عذراً، مكتبة الذكاء الاصطناعي غير مثبتة.\n\nيرجى فتح موجه الأوامر (Terminal) وتشغيل الأمر التالي:\npip install google-generativeai\n\nثم أعد تشغيل البرنامج.",
                "disclaimer": DISCLAIMERS[self.service_type]
            }
        
        # الحصول على التعليمات المناسبة
        prompt = get_analysis_prompt(details)
        
        # محاولة الاتصال بالذكاء الاصطناعي للحصول على رد فعلي
        ai_response = self._call_ai_model(prompt)
        
        if ai_response:
            return {
                "service_type": self.service_type,
                "content": ai_response
            }
            
        # في حال فشل الاتصال تماماً
        return {
            "service_type": self.service_type,
            "content": "⚠️ تعذر الاتصال بخدمة الذكاء الاصطناعي. يرجى التحقق من الاتصال بالإنترنت.",
            "disclaimer": DISCLAIMERS[self.service_type]
        }
    
    def format_output(self, result: str) -> Dict[str, Any]:
        """
        تنسيق مخرجات التحليل
        
        Args:
            result: نص التحليل من النموذج
            
        Returns:
            dict: تحليل منظم
        """
        return {
            "service_type": "تحليل مذكرة الخصم",
            "content": result,
            "disclaimer": DISCLAIMERS[self.service_type],
            "format": "analysis"
        }
