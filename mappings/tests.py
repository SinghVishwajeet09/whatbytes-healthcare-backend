from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from patients.models import Patient
from doctors.models import Doctor
from mappings.models import PatientDoctorMapping

User = get_user_model()


class MappingAPITests(APITestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(
            email='doctor_user1@example.com',
            name='Dr. User One',
            password='Password123!'
        )
        self.user2 = User.objects.create_user(
            email='doctor_user2@example.com',
            name='Dr. User Two',
            password='Password123!'
        )

        login_res = self.client.post(
            reverse('auth-login'),
            {'email': 'doctor_user1@example.com', 'password': 'Password123!'},
            format='json'
        )
        self.token_user1 = login_res.data['tokens']['access']

        login_res2 = self.client.post(
            reverse('auth-login'),
            {'email': 'doctor_user2@example.com', 'password': 'Password123!'},
            format='json'
        )
        self.token_user2 = login_res2.data['tokens']['access']

        # Create patient for user1
        self.patient1 = Patient.objects.create(
            name='Robert Baratheon',
            age=45,
            gender='Male',
            contact_number='1234567890',
            created_by=self.user1
        )

        # Create patient for user2
        self.patient2 = Patient.objects.create(
            name='Eddard Stark',
            age=44,
            gender='Male',
            contact_number='9876543210',
            created_by=self.user2
        )

        # Create doctors
        self.doctor1 = Doctor.objects.create(
            name='Meredith Grey',
            specialization='General Surgery',
            contact_number='5551112222',
            email='grey@seattlegrace.com',
            years_of_experience=10
        )
        self.doctor2 = Doctor.objects.create(
            name='Derek Shepherd',
            specialization='Neurosurgery',
            contact_number='5553334444',
            email='shepherd@seattlegrace.com',
            years_of_experience=15
        )

        self.mapping_list_create_url = reverse('mapping-list-create')

    def test_assign_doctor_to_patient_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user1}')
        payload = {
            'patient': self.patient1.id,
            'doctor': self.doctor1.id,
            'notes': 'Post-op observation'
        }
        response = self.client.post(self.mapping_list_create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('mapping', response.data)
        self.assertEqual(response.data['mapping']['patient_id'], self.patient1.id)
        self.assertEqual(response.data['mapping']['doctor_id'], self.doctor1.id)

    def test_assign_doctor_to_other_users_patient_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user1}')
        payload = {
            'patient': self.patient2.id,  # Owned by user2!
            'doctor': self.doctor1.id,
            'notes': 'Attempting unauthorized assignment'
        }
        response = self.client.post(self.mapping_list_create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('patient', response.data)

    def test_prevent_duplicate_mapping(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user1}')
        payload = {
            'patient': self.patient1.id,
            'doctor': self.doctor1.id,
        }
        # First assignment
        res1 = self.client.post(self.mapping_list_create_url, payload, format='json')
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)

        # Duplicate assignment
        res2 = self.client.post(self.mapping_list_create_url, payload, format='json')
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_mappings(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user1}')
        # Create 2 mappings for patient1
        self.client.post(self.mapping_list_create_url, {'patient': self.patient1.id, 'doctor': self.doctor1.id}, format='json')
        self.client.post(self.mapping_list_create_url, {'patient': self.patient1.id, 'doctor': self.doctor2.id}, format='json')

        response = self.client.get(self.mapping_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_doctors_assigned_to_specific_patient(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user1}')
        self.client.post(self.mapping_list_create_url, {'patient': self.patient1.id, 'doctor': self.doctor1.id}, format='json')
        self.client.post(self.mapping_list_create_url, {'patient': self.patient1.id, 'doctor': self.doctor2.id}, format='json')

        # GET /api/mappings/<patient_id>/
        patient_mappings_url = reverse('mapping-patient-or-detail', kwargs={'lookup_id': self.patient1.id})
        response = self.client.get(patient_mappings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['patient_id'], self.patient1.id)
        self.assertEqual(response.data['total_assigned'], 2)
        self.assertEqual(len(response.data['assigned_doctors']), 2)

    def test_remove_doctor_from_patient(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user1}')
        res = self.client.post(self.mapping_list_create_url, {'patient': self.patient1.id, 'doctor': self.doctor1.id}, format='json')
        mapping_id = res.data['mapping']['id']

        # DELETE /api/mappings/<id>/
        delete_url = reverse('mapping-patient-or-detail', kwargs={'lookup_id': mapping_id})
        del_resp = self.client.delete(delete_url)
        self.assertEqual(del_resp.status_code, status.HTTP_204_NO_CONTENT)

        # Verify mapping is deleted
        self.assertFalse(PatientDoctorMapping.objects.filter(id=mapping_id).exists())
