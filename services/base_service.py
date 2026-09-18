"""Shared service interface; credentials stay in server-side settings."""
from abc import ABC, abstractmethod
import json
import os
import urllib.request
from urllib.parse import quote

class BaseService(ABC):
    def __init__(self, service_type):
        self.service_type = service_type

    @property
    def is_ai_available(self):
        return bool(os.environ.get('GEMINI_API_KEY') and os.environ.get('GEMINI_MODEL'))

    def get_ai_response(self, prompt):
        if not self.is_ai_available:
            raise RuntimeError('AI configuration is missing')
        model = os.environ['GEMINI_MODEL'].removeprefix('models/')
        url = 'https://generativelanguage.googleapis.com/v1beta/models/' + quote(model, safe='') + ':generateContent'
        payload = json.dumps({'contents': [{'parts': [{'text': prompt}]}]}).encode()
        req = urllib.request.Request(url, data=payload, headers={
            'Content-Type': 'application/json',
            'x-goog-api-key': os.environ['GEMINI_API_KEY'],
        })
        with urllib.request.urlopen(req, timeout=45) as response:
            result = json.load(response)
        candidates = result.get('candidates', [])
        parts = candidates[0].get('content', {}).get('parts', []) if candidates else []
        text = '\n'.join(p['text'] for p in parts if p.get('text'))
        if not text:
            raise RuntimeError('Provider returned no text')
        return text

    def _call_ai_model(self, prompt):
        return self.get_ai_response(prompt)

    def validate_input(self, details):
        return isinstance(details, str) and bool(details.strip())

    @abstractmethod
    def process(self, details):
        pass

    @abstractmethod
    def format_output(self, result):
        pass
