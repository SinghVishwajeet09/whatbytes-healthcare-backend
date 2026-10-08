from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Patient

User = get_user_model()


class PatientAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='doctor1@example.com',
            name='Doctor One',
            password='Password123!'
        )
        self.user2 = User.objects.create_user(
            email='doctor2@example.com',
            name='Doctor Two',
            password='Password123!'
        )

        login_res = self.client.post(
            reverse('auth-login'),
            {'email': 'doctor1@example.com', 'password': 'Password123!'},
            format='json'
        )
        self.token_user1 = login_res.data['tokens']['access']

        login_res2 = self.client.post(
            reverse('auth-login'),
            {'email': 'doctor2@example.com', 'password': 'Password123!'},
            format='json'
        )
        self.token_user2 = login_res2.data['tokens']['access']

        self.list_create_url = reverse('patient-list-create')
        self.patient_payload = {
            'name': 'Johnathan Doe',
            'age': 35,
            'gender': 'Male',
            'contact_number': '9876543210',
            'email': 'johnathan@example.com',
            'address': '123 Health Ave, Metropolis',
            'medical_history': 'No known allergies. Mild hypertension.'
        }

    def test_create_patient_unauthenticated(self):
        response = self.client.post(self.list_create_url, self.patient_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_patient_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user1}')
        response = self.client.post(self.list_create_url, self.patient_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Johnathan Doe')
        self.assertEqual(response.data['created_by_email'], 'doctor1@example.com')

    def test_list_patients_user_isolation(self):
        # User 1 creates patient
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user1}')
        self.client.post(self.list_create_url, self.patient_payload, format='json')

        # User 2 creates patient
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user2}')
        payload2 = dict(self.patient_payload, name='Jane Smith', contact_number='1122334455')
        self.client.post(self.list_create_url, payload2, format='json')

        # User 1 lists patients - should only see their own
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user1}')
        response1 = self.client.get(self.list_create_url)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 1)
        self.assertEqual(response1.data[0]['name'], 'Johnathan Doe')

        # User 2 lists patients - should only see their own
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user2}')
        response2 = self.client.get(self.list_create_url)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 1)
        self.assertEqual(response2.data[0]['name'], 'Jane Smith')

    def test_get_patient_details(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user1}')
        res = self.client.post(self.list_create_url, self.patient_payload, format='json')
        patient_id = res.data['id']

        detail_url = reverse('patient-detail', kwargs={'pk': patient_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], patient_id)

    def test_get_patient_details_other_user_forbidden_or_not_found(self):
        # User 1 creates patient
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user1}')
        res = self.client.post(self.list_create_url, self.patient_payload, format='json')
        patient_id = res.data['id']

        # User 2 tries to access user 1's patient
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user2}')
        detail_url = reverse('patient-detail', kwargs={'pk': patient_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_patient(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user1}')
        res = self.client.post(self.list_create_url, self.patient_payload, format='json')
        patient_id = res.data['id']

        detail_url = reverse('patient-detail', kwargs={'pk': patient_id})
        update_payload = dict(self.patient_payload, name='John Doe Updated', age=36)
        response = self.client.put(detail_url, update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Doe Updated')
        self.assertEqual(response.data['age'], 36)

    def test_delete_patient(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user1}')
        res = self.client.post(self.list_create_url, self.patient_payload, format='json')
        patient_id = res.data['id']

        detail_url = reverse('patient-detail', kwargs={'pk': patient_id})
        del_resp = self.client.delete(detail_url)
        self.assertEqual(del_resp.status_code, status.HTTP_204_NO_CONTENT)

        get_resp = self.client.get(detail_url)
        self.assertEqual(get_resp.status_code, status.HTTP_404_NOT_FOUND)
