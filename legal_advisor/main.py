"""
الملف الرئيسي لمنصة المستشار القانوني الافتراضي
Main file for Virtual Legal Advisor Platform
"""

import json
from typing import Dict, Any, Optional
from services import (
    ConsultationService,
    ContractService,
    MemoService,
    AnalysisService,
    ObjectionService,
    ChatService
)
from config import SERVICE_TYPES

class LegalAdvisorPlatform:
    """منصة المستشار القانوني الافتراضي"""
    
    def __init__(self):
        """تهيئة الخدمات"""
        self.services = {
            "consultation": ConsultationService(),
            "contract": ContractService(),
            "memo": MemoService(),
            "analysis": AnalysisService(),
            "objection": ObjectionService(),
            "chat": ChatService()
        }
    
    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        معالجة الطلب الوارد
        
        Args:
            request: الطلب بصيغة JSON يحتوي على:
                - service_type: نوع الخدمة
                - details: تفاصيل الطلب
                
        Returns:
            dict: النتيجة المنظمة
        """
        # التحقق من وجود نوع الخدمة
        service_type = request.get("service_type")
        if not service_type:
            return {
                "error": "يرجى تحديد نوع الخدمة (service_type)",
                "available_services": list(SERVICE_TYPES.keys())
            }
        
        # التحقق من صحة نوع الخدمة
        if service_type not in self.services:
            return {
                "error": f"نوع الخدمة غير معروف: {service_type}",
                "available_services": list(SERVICE_TYPES.keys())
            }
        
        # الحصول على تفاصيل الطلب
        details = request.get("details", "")
        
        # معالجة الطلب
        service = self.services[service_type]
        result = service.process(details)
        
        return result
    
    def get_service_info(self, service_type: Optional[str] = None) -> Dict[str, Any]:
        """
        الحصول على معلومات عن الخدمات المتاحة
        
        Args:
            service_type: نوع الخدمة (اختياري)
            
        Returns:
            dict: معلومات الخدمة/الخدمات
        """
        if service_type:
            if service_type in SERVICE_TYPES:
                return {
                    "service_type": service_type,
                    "name": SERVICE_TYPES[service_type],
                    "available": True
                }
            else:
                return {
                    "error": f"نوع الخدمة غير معروف: {service_type}",
                    "available_services": list(SERVICE_TYPES.keys())
                }
        else:
            return {
                "available_services": SERVICE_TYPES
            }


def main():
    """الدالة الرئيسية للتشغيل"""
    print("=" * 60)
    print("منصة المستشار القانوني الافتراضي - الأنظمة السعودية")
    print("=" * 60)
    print()
    
    platform = LegalAdvisorPlatform()
    
    # مثال على الاستخدام
    example_request = {
        "service_type": "contract",
        "details": "عقد شراكة بين أحمد وسلمان لمدة سنة، بمقابل مالي 10000 ريال، يشمل بند ملكية فكرية."
    }
    
    print("مثال على الطلب:")
    print(json.dumps(example_request, ensure_ascii=False, indent=2))
    print()
    print("-" * 60)
    print()
    
    # معالجة الطلب
    result = platform.process_request(example_request)
    
    print("النتيجة:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()
    print("-" * 60)
    print()
    
    print("للحصول على معلومات الخدمات المتاحة:")
    services_info = platform.get_service_info()
    print(json.dumps(services_info, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
