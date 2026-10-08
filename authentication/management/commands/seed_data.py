from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from patients.models import Patient
from doctors.models import Doctor
from mappings.models import PatientDoctorMapping

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds initial demo data for testing the Healthcare API'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Seeding demo healthcare data...'))

        # Create or update superuser
        admin_user, _ = User.objects.get_or_create(
            email='admin@healthcare.com',
            defaults={'name': 'Super Admin', 'is_staff': True, 'is_superuser': True}
        )
        admin_user.set_password('AdminPassword123!')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        self.stdout.write(self.style.SUCCESS(f'Admin user ready: {admin_user.email}'))

        # Create or update demo users
        user1, created = User.objects.get_or_create(
            email='dr.john@healthcare.com',
            defaults={'name': 'Dr. John Doe'}
        )
        if created:
            user1.set_password('Password123!')
            user1.save()
            self.stdout.write(self.style.SUCCESS(f'Created user: {user1.email}'))
        else:
            self.stdout.write(self.style.WARNING(f'User already exists: {user1.email}'))

        user2, created = User.objects.get_or_create(
            email='nurse.mary@healthcare.com',
            defaults={'name': 'Nurse Mary Smith'}
        )
        if created:
            user2.set_password('Password123!')
            user2.save()
            self.stdout.write(self.style.SUCCESS(f'Created user: {user2.email}'))

        # Create Doctors
        doctors_data = [
            {
                'name': 'Sarah Connor',
                'specialization': 'Cardiology',
                'contact_number': '+1-555-0101',
                'email': 'dr.sarah@cardio-center.com',
                'years_of_experience': 12,
                'hospital_affiliation': 'Metro General Hospital'
            },
            {
                'name': 'Robert Langdon',
                'specialization': 'Neurology',
                'contact_number': '+1-555-0102',
                'email': 'dr.robert@neuro-care.org',
                'years_of_experience': 16,
                'hospital_affiliation': 'Harvard Memorial Clinic'
            },
            {
                'name': 'Elena Rostova',
                'specialization': 'Pediatrics',
                'contact_number': '+1-555-0103',
                'email': 'dr.elena@children-first.org',
                'years_of_experience': 8,
                'hospital_affiliation': 'St. Jude Children Pavilion'
            }
        ]

        doctors = []
        for d in doctors_data:
            doc, _ = Doctor.objects.get_or_create(
                email=d['email'],
                defaults={**d, 'created_by': user1}
            )
            doctors.append(doc)
            self.stdout.write(self.style.SUCCESS(f'Doctor ready: Dr. {doc.name} ({doc.specialization})'))

        # Create Patients for user1
        patients_data = [
            {
                'name': 'Alice Wonder',
                'age': 29,
                'gender': 'Female',
                'contact_number': '+1-555-0201',
                'email': 'alice.wonder@example.com',
                'address': '42 Rabbit Hole Lane, Wonderland',
                'medical_history': 'Seasonal allergies, mild asthma'
            },
            {
                'name': 'Bruce Wayne',
                'age': 38,
                'gender': 'Male',
                'contact_number': '+1-555-0202',
                'email': 'bruce@wayne-enterprises.com',
                'address': '1007 Mountain Drive, Gotham City',
                'medical_history': 'Multiple contusions, previous collarbone fracture'
            }
        ]

        patients = []
        for p in patients_data:
            pat, _ = Patient.objects.get_or_create(
                name=p['name'],
                created_by=user1,
                defaults={**p}
            )
            patients.append(pat)
            self.stdout.write(self.style.SUCCESS(f'Patient ready: {pat.name}'))

        # Create Mappings
        if len(patients) >= 2 and len(doctors) >= 2:
            m1, _ = PatientDoctorMapping.objects.get_or_create(
                patient=patients[0],
                doctor=doctors[0],
                defaults={'notes': 'Cardiovascular evaluation and routine ECG'}
            )
            m2, _ = PatientDoctorMapping.objects.get_or_create(
                patient=patients[1],
                doctor=doctors[1],
                defaults={'notes': 'Neurological post-trauma assessment'}
            )
            self.stdout.write(self.style.SUCCESS(f'Mapping created: {m1}'))
            self.stdout.write(self.style.SUCCESS(f'Mapping created: {m2}'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded demo healthcare records!'))
