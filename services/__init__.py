"""
حزمة خدمات المستشار القانوني
"""

from .consultation_service import ConsultationService
from .contract_service import ContractService
from .memo_service import MemoService
from .analysis_service import AnalysisService
from .objection_service import ObjectionService
from .chat_service import ChatService
from .base_service import BaseService

__all__ = [
    'BaseService',
    'ConsultationService',
    'ContractService',
    'MemoService',
    'AnalysisService',
    'ObjectionService',
    'ChatService'
]
