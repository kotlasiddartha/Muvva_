from django.test import TestCase, Client
from django.urls import reverse
from .models import Receipe


class UpdateReceipeTest(TestCase):
	def setUp(self):
		self.client = Client()
		self.r = Receipe.objects.create(receipe_name='Alice', case_number='C001')

	def test_update_via_post(self):
		url = reverse('update_receipe', args=[self.r.id])
		resp = self.client.post(url, {
			'receipe_name': 'Alice Updated',
			'case_number': 'C001',
		})
		self.assertEqual(resp.status_code, 302)
		self.r.refresh_from_db()
		self.assertEqual(self.r.receipe_name, 'Alice Updated')

	def test_update_via_ajax(self):
		url = reverse('update_receipe', args=[self.r.id])
		resp = self.client.post(url, {
			'receipe_name': 'Alice Ajax',
			'case_number': 'C001',
		}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		self.assertEqual(data.get('status'), 'ok')
		self.r.refresh_from_db()
		self.assertEqual(self.r.receipe_name, 'Alice Ajax')
