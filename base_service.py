"""
الخدمة الأساسية - واجهة مشتركة لجميع الخدمات القانونية
Base Service - Common interface for all legal services
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import os
import time
import google.generativeai as genai

# مفتاح API الخاص بك
GENAI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAkuhR5glb5NSUC2ySrpUVy-tASEDyuyag")
genai.configure(api_key=GENAI_API_KEY)

class BaseService(ABC):
    
    def __init__(self, service_type: str):
        self.service_type = service_type
        # إعداد الموديل
        # استخدام النسخة Lite لتجنب تجاوز حدود الاستخدام (Quota)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def get_ai_response(self, prompt: str) -> str:
        """هذه هي الدالة التي ستجلب الإجابة من الذكاء الاصطناعي"""
        # إعدادات الأمان للسماح بالنصوص القانونية
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        # محاولة الاتصال مع إعادة المحاولة في حال وجود ضغط
        for attempt in range(3):
            try:
                response = self.model.generate_content(prompt, safety_settings=safety_settings)
                return response.text
            except Exception as e:
                error_str = str(e)
                # إذا كان الخطأ بسبب الضغط (429)، ننتظر قليلاً ثم نعيد المحاولة
                if "429" in error_str and attempt < 2:
                    time.sleep(6)
                    continue
                
                # ترجمة الأخطاء للمستخدم النهائي بدلاً من عرض الكود
                if "429" in error_str:
                    return "⚠️ عذراً، الخدمة مشغولة جداً حالياً (تجاوز حد الاستخدام المجاني). يرجى الانتظار دقيقة ثم المحاولة."
                elif "404" in error_str or "not found" in error_str.lower():
                    return "⚠️ عذراً، الموديل الذكي غير متاح حالياً. يرجى التواصل مع الدعم الفني."
                elif "403" in error_str or "API key" in error_str:
                    return "⚠️ عذراً، هناك مشكلة في مفتاح التفعيل (API Key). يرجى التأكد من صلاحيته."
                else:
                    return f"⚠️ حدث خطأ غير متوقع:\n{error_str}"

    # --- توافق مع الخدمات الأخرى ---
    @property
    def is_ai_available(self) -> bool:
        return True

    def _call_ai_model(self, prompt: str) -> str:
        return self.get_ai_response(prompt)
    # -----------------------------

    @abstractmethod
    def process(self, details: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def format_output(self, result: str) -> Dict[str, Any]:
        pass

    def validate_input(self, details: str) -> bool:
        return bool(details and details.strip())
