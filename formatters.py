"""
أدوات تنسيق المخرجات
Output Formatting Utilities
"""

from typing import Dict, Any
from config import DISCLAIMERS

def format_legal_document(content: str, service_type: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    تنسيق المستند القانوني
    
    Args:
        content: محتوى المستند
        service_type: نوع الخدمة
        metadata: بيانات إضافية
        
    Returns:
        dict: مستند منسق
    """
    result = {
        "content": content,
        "disclaimer": DISCLAIMERS.get(service_type, ""),
        "service_type": service_type
    }
    
    if metadata:
        result.update(metadata)
    
    return result

def format_for_pdf(content: str) -> str:
    """
    تنسيق المحتوى للتحويل إلى PDF
    
    Args:
        content: المحتوى النصي
        
    Returns:
        str: محتوى منسق لـ PDF
    """
    # يمكن إضافة تنسيق خاص لـ PDF هنا
    return content

def format_for_word(content: str) -> str:
    """
    تنسيق المحتوى للتحويل إلى Word
    
    Args:
        content: المحتوى النصي
        
    Returns:
        str: محتوى منسق لـ Word
    """
    # يمكن إضافة تنسيق خاص لـ Word هنا
    return content
