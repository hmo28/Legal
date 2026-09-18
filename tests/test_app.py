import os
import unittest
from unittest.mock import patch
from services.run_web import app
from services.base_service import BaseService

class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_pages(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertEqual(self.client.get('/health').json['status'], 'ok')
        services = self.client.get('/api/services').json['available_services']
        self.assertIn('chat', services)
        self.assertEqual(len(services), 6)

    def test_bad_requests(self):
        for data in [None, [], {}, {'service_type': []},
                     {'service_type':'chat','details':123},
                     {'service_type':'chat','details':' '},
                     {'service_type':'chat','details':'x'*12001}]:
            self.assertEqual(self.client.post('/api/process',json=data).status_code,400)

    def test_missing_key(self):
        with patch.dict(os.environ, {'GEMINI_API_KEY':''}):
            self.assertEqual(self.client.post('/api/process',json={'service_type':'chat','details':'test'}).status_code,503)

    def test_all_services_with_simulated_provider(self):
        with patch.dict(os.environ,{'GEMINI_API_KEY':'test','GEMINI_MODEL':'test'}), patch.object(BaseService,'get_ai_response',return_value='SIMULATED TEST RESPONSE'):
            for service in ['chat','consultation','contract','memo','analysis','objection']:
                response=self.client.post('/api/process',json={'service_type':service,'details':'test details'})
                self.assertEqual(response.status_code,200,service)
                self.assertIn('SIMULATED TEST RESPONSE',response.json['content'])
                self.assertIn('disclaimer',response.json)

    def test_provider_errors_are_not_exposed(self):
        with patch.dict(os.environ,{'GEMINI_API_KEY':'test','GEMINI_MODEL':'test'}), patch.object(BaseService,'get_ai_response',side_effect=RuntimeError('secret-internal-value')):
            response=self.client.post('/api/process',json={'service_type':'chat','details':'test'})
            self.assertEqual(response.status_code,502)
            self.assertNotIn('secret-internal-value',response.get_data(as_text=True))

if __name__=='__main__':
    unittest.main()
