from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Client, HealthProgram, Enrollment

class HealthSystemTests(TestCase):
    def setUp(self):
        self.client_api = APIClient()
        self.program_data = {'name': 'Malaria'}
        self.client_data = {
            'full_name': 'Test User',
            'national_id': '99999999',
            'date_of_birth': '1990-01-01',
            'contact': '0700000000'
        }

    def test_create_program(self):
        response = self.client_api.post('/api/programs/', self.program_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HealthProgram.objects.count(), 1)

    def test_register_client(self):
        response = self.client_api.post('/api/clients/', self.client_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 1)

    def test_enroll_client_in_program(self):
        program = HealthProgram.objects.create(name="HIV")
        client = Client.objects.create(**self.client_data)
        data = {'client': client.id, 'program': program.id}
        response = self.client_api.post('/api/enroll/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enrollment.objects.count(), 1)

    def test_view_client_profile(self):
        program = HealthProgram.objects.create(name="TB")
        client = Client.objects.create(**self.client_data)
        Enrollment.objects.create(client=client, program=program)

        response = self.client_api.get(f'/api/clients/{client.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('programs', response.data)
        self.assertEqual(response.data['full_name'], self.client_data['full_name'])

    def test_list_clients(self):
        Client.objects.create(**self.client_data)
        response = self.client_api.get('/api/clients/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
