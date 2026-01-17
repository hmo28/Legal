# -*- coding: utf-8 -*-
"""تشغيل منصة الويب"""
import sys
import os

# تحديد المسار الصحيح للمشروع
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
os.chdir(project_root)
sys.path.insert(0, project_root)

from flask import Flask, render_template, request, jsonify
import json

# استخدام المسار الكامل لمجلد templates
templates_path = os.path.join(project_root, 'templates')
app = Flask(__name__, template_folder=templates_path)
app.config['JSON_AS_ASCII'] = False

try:
    from legal_advisor.main import LegalAdvisorPlatform
    platform = LegalAdvisorPlatform()
except ImportError:
    from services import ConsultationService, ContractService, MemoService, AnalysisService, ObjectionService, ChatService
    from config import SERVICE_TYPES
    
    class LegalAdvisorPlatform:
        def __init__(self):
            self.services = {
                "consultation": ConsultationService(),
                "contract": ContractService(),
                "memo": MemoService(),
                "analysis": AnalysisService(),
                "objection": ObjectionService(),
                "chat": ChatService()
            }
        
        def process_request(self, request_data):
            service_type = request_data.get("service_type")
            if not service_type or service_type not in self.services:
                return {"error": f"نوع الخدمة غير معروف: {service_type}"}
            details = request_data.get("details", "")
            return self.services[service_type].process(details)
        
        def get_service_info(self, service_type=None):
            return {"available_services": SERVICE_TYPES}
    
    platform = LegalAdvisorPlatform()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/services', methods=['GET'])
def get_services():
    services_info = platform.get_service_info()
    return jsonify(services_info)

@app.route('/api/process', methods=['POST'])
def process_request_api():
    try:
        data = request.get_json()
        result = platform.process_request({
            "service_type": data.get("service_type"),
            "details": data.get("details", "")
        })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("=" * 70)
    print(" " * 10 + "⚖️  منصة المستشار القانوني الافتراضي")
    print(" " * 15 + "متخصصة في الأنظمة السعودية")
    print("=" * 70)
    
    # فحص مكتبات الذكاء الاصطناعي
    try:
        import google.generativeai as genai
        # إعداد المفتاح للفحص
        api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyAkuhR5glb5NSUC2ySrpUVy-tASEDyuyag")
        genai.configure(api_key=api_key)
        
        print("✅ مكتبة Google AI (Gemini) مثبتة.")
        print("⏳ جاري فحص الموديلات المتاحة للمفتاح...")
        try:
            models = list(genai.list_models())
            chat_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
            if chat_models:
                print(f"✅ الاتصال ناجح! الموديلات المتاحة: {', '.join(chat_models)}")
            else:
                print("⚠️ الاتصال ناجح ولكن لم يتم العثور على موديلات تدعم المحادثة.")
        except Exception as e:
            print(f"❌ خطأ في مفتاح API أو الاتصال: {e}")
    except ImportError:
        print("❌ تنبيه: مكتبة google-generativeai غير مثبتة!")
        print("   لإصلاح المشكلة، اكتب في التيرمينال: pip install google-generativeai")

    print(f"\n📁 المجلد: {os.getcwd()}")
    print(f"📁 templates: {os.path.exists('templates')}")
    print(f"📁 index.html موجود: {os.path.exists(os.path.join(templates_path, 'index.html'))}")
    print("\n" + "=" * 70)
    print("🚀 جاري التشغيل على: http://127.0.0.1:5000")
    print("🌐 افتح المتصفح للوصول إلى المنصة")
    print("⏹️  اضغط Ctrl+C لإيقاف الخادم")
    print("=" * 70 + "\n")
    try:
        port = int(os.environ.get("PORT", 5000))
        app.run(debug=False, host='0.0.0.0', port=port, use_reloader=False)
    except Exception as e:
        print(f"❌ خطأ: {e}")
        import traceback
        traceback.print_exc()
