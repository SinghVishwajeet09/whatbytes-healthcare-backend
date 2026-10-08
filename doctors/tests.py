from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Doctor

User = get_user_model()


class DoctorAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@hospital.com',
            name='Hospital Admin',
            password='AdminPassword123!'
        )
        login_res = self.client.post(
            reverse('auth-login'),
            {'email': 'admin@hospital.com', 'password': 'AdminPassword123!'},
            format='json'
        )
        self.token = login_res.data['tokens']['access']
        self.list_create_url = reverse('doctor-list-create')
        self.doctor_payload = {
            'name': 'Gregory House',
            'specialization': 'Diagnostic Medicine',
            'contact_number': '5551234567',
            'email': 'house@princetonplainsboro.com',
            'years_of_experience': 20,
            'hospital_affiliation': 'Princeton-Plainsboro Teaching Hospital'
        }

    def test_create_doctor_unauthenticated(self):
        response = self.client.post(self.list_create_url, self.doctor_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_doctor_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(self.list_create_url, self.doctor_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Gregory House')
        self.assertEqual(response.data['specialization'], 'Diagnostic Medicine')

    def test_list_doctors(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.client.post(self.list_create_url, self.doctor_payload, format='json')
        second_doc = dict(
            self.doctor_payload,
            name='James Wilson',
            email='wilson@princetonplainsboro.com',
            specialization='Oncology'
        )
        self.client.post(self.list_create_url, second_doc, format='json')

        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_doctor_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        res = self.client.post(self.list_create_url, self.doctor_payload, format='json')
        doc_id = res.data['id']

        detail_url = reverse('doctor-detail', kwargs={'pk': doc_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'house@princetonplainsboro.com')

    def test_update_doctor(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        res = self.client.post(self.list_create_url, self.doctor_payload, format='json')
        doc_id = res.data['id']

        detail_url = reverse('doctor-detail', kwargs={'pk': doc_id})
        update_data = dict(self.doctor_payload, years_of_experience=21)
        response = self.client.put(detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['years_of_experience'], 21)

    def test_delete_doctor(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        res = self.client.post(self.list_create_url, self.doctor_payload, format='json')
        doc_id = res.data['id']

        detail_url = reverse('doctor-detail', kwargs={'pk': doc_id})
        del_resp = self.client.delete(detail_url)
        self.assertEqual(del_resp.status_code, status.HTTP_204_NO_CONTENT)

        get_resp = self.client.get(detail_url)
        self.assertEqual(get_resp.status_code, status.HTTP_404_NOT_FOUND)
