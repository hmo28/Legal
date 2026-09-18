"""Flask entry point. No provider requests are made during startup."""
from pathlib import Path
import os
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / '.env', override=False)
from legal_advisor.main import LegalAdvisorPlatform
from config import DISCLAIMERS

app = Flask(__name__, template_folder=str(Path(__file__).resolve().parents[1] / 'templates'))
app.json.ensure_ascii = False
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024
platform = LegalAdvisorPlatform()

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/health')
def health():
    configured = bool(os.environ.get('GEMINI_API_KEY') and os.environ.get('GEMINI_MODEL'))
    return jsonify(status='ok', ai_configured=configured)

@app.get('/api/services')
def services():
    return jsonify(platform.get_service_info())

@app.post('/api/process')
def process():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error='يرجى إرسال بيانات صحيحة.'), 400
    service = data.get('service_type')
    details = data.get('details')
    if not isinstance(service, str) or service not in platform.services:
        return jsonify(error='نوع الخدمة غير معروف.'), 400
    if not isinstance(details, str) or not details.strip():
        return jsonify(error='يرجى إدخال التفاصيل.'), 400
    if len(details) > 12000:
        return jsonify(error='النص طويل جدًا. الحد الأقصى 12000 حرف.'), 400
    if not platform.services[service].is_ai_available:
        return jsonify(error='خدمة الذكاء الاصطناعي غير مفعلة حاليًا.'), 503
    try:
        result = platform.process_request(data)
        result.setdefault('disclaimer', DISCLAIMERS.get(service, 'للاسترشاد فقط.'))
        return jsonify(result)
    except Exception:
        return jsonify(error='تعذر الاتصال بخدمة الذكاء الاصطناعي. حاول لاحقًا.'), 502
