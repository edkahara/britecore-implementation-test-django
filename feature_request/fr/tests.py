from django.test import TestCase
from .models import Request
import json

class TestRequests(TestCase):
    fixtures = ['clients.json', 'products.json']

    def setUp(self):
        self.first_request = {
            'title': 'First Request',
            'description': 'First Description',
            'client': 1,
            'priority': 1,
            'product': 1,
            'targetDate': 'May 30, 2019'
        }
        self.second_request = {
            'title': 'Second Request',
            'description': 'Second Description',
            'client': 1,
            'priority': 1,
            'product': 1,
            'targetDate': 'May 30, 2019'
        }
        self.request_edit = {
            'title': 'First Request Edited',
            'description': 'First Description Edited',
            'client': 1,
            'priority': 1,
            'product': 1,
            'targetDate': 'May 30, 2019'
        }

    def createFirstRequestForTesting(self):
        self.client.post('/create/', self.first_request)

    def createSecondRequestForTesting(self):
        self.client.post('/create/', self.second_request)

    def test_create_request(self):
        res = self.client.post('/create/', self.first_request)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Request.objects.count(), 1)
        self.assertEqual(Request.objects.get(id=1).title, 'First Request')

    def test_get_all_requests(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "no feature requests")

    def test_get_specific_request(self):
        self.createFirstRequestForTesting()
        res = self.client.get('/1/')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertEqual(data[0]['fields']['title'], 'First Request')
        self.assertEqual(data[0]['fields']['client'], 1)
        self.assertEqual(data[0]['fields']['priority'], 1)

    def test_priority_reorder_on_create(self):
        self.createFirstRequestForTesting()
        res = self.client.post('/create/', data=self.second_request)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Request.objects.count(), 2)
        self.assertEqual(Request.objects.get(id=1).priority, 2)
        self.assertEqual(Request.objects.get(id=2).priority, 1)

    def test_update_request(self):
        self.createFirstRequestForTesting()
        res = self.client.post('/update/1/', data=self.request_edit)
        self.assertEqual(res.status_code, 302)
        data = Request.objects.get(id=1)
        self.assertEqual(data.title, 'First Request Edited')
        self.assertEqual(data.description, 'First Description Edited')

    def test_priority_reorder_on_update(self):
        self.createFirstRequestForTesting()
        self.createSecondRequestForTesting()
        res = self.client.post('/update/1/', data=self.request_edit)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Request.objects.get(id=1).priority, 1)
        self.assertEqual(Request.objects.get(id=2).priority, 2)

    def test_delete_request(self):
        self.createFirstRequestForTesting()
        self.createSecondRequestForTesting()
        res = self.client.get('/delete/1/')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Request.objects.count(), 1)
        self.assertEqual(Request.objects.first().title, 'Second Request')

    def test_request_not_found_on_get(self):
        res = self.client.get('/1/')
        self.assertEqual(res.status_code, 404)

    def test_request_not_found_on_update(self):
        res = self.client.post('/update/1/', data=self.request_edit)
        self.assertEqual(res.status_code, 404)

    def test_request_not_found_on_delete(self):
        res = self.client.get('/delete/1/')
        self.assertEqual(res.status_code, 404)
