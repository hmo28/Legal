"""
حزمة قوالب التعليمات القانونية
"""

from .legal_prompts import (
    get_consultation_prompt,
    get_contract_prompt,
    get_memo_prompt,
    get_analysis_prompt,
    get_objection_prompt,
    get_chat_prompt,
    get_prompt_by_service_type
)

__all__ = [
    'get_consultation_prompt',
    'get_contract_prompt',
    'get_memo_prompt',
    'get_analysis_prompt',
    'get_objection_prompt',
    'get_chat_prompt',
    'get_prompt_by_service_type'
]
