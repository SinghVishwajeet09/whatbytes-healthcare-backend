from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.models import Patient
from doctors.models import Doctor


class NestedPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('id', 'name', 'age', 'gender', 'contact_number')


class NestedDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('id', 'name', 'specialization', 'contact_number', 'email', 'hospital_affiliation')


class PatientDoctorMappingReadSerializer(serializers.ModelSerializer):
    """Detailed read serializer for patient-doctor mapping."""
    patient = NestedPatientSerializer(read_only=True)
    doctor = NestedDoctorSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(read_only=True, source='patient.id')
    doctor_id = serializers.PrimaryKeyRelatedField(read_only=True, source='doctor.id')

    class Meta:
        model = PatientDoctorMapping
        fields = (
            'id',
            'patient_id',
            'patient',
            'doctor_id',
            'doctor',
            'notes',
            'assigned_date'
        )
        read_only_fields = fields


class PatientDoctorMappingCreateSerializer(serializers.ModelSerializer):
    """Serializer to assign a doctor to a patient with validation."""

    class Meta:
        model = PatientDoctorMapping
        fields = ('id', 'patient', 'doctor', 'notes', 'assigned_date')
        read_only_fields = ('id', 'assigned_date')

    def validate(self, attrs):
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')
        request = self.context.get('request')

        # Verify that patient belongs to requesting user
        if request and request.user and not request.user.is_staff:
            if patient.created_by != request.user:
                raise serializers.ValidationError({
                    'patient': 'You can only assign doctors to patients you created.'
                })

        # Check for duplicate assignment
        if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
            raise serializers.ValidationError(
                'This doctor is already assigned to the selected patient.'
            )

        return attrs

    def to_representation(self, instance):
        # Return enriched representation upon creation
        return PatientDoctorMappingReadSerializer(instance, context=self.context).data
