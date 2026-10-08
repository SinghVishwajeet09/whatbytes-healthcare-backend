from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model with validation and read-only ownership."""

    created_by_name = serializers.ReadOnlyField(source='created_by.name')
    created_by_email = serializers.ReadOnlyField(source='created_by.email')

    class Meta:
        model = Patient
        fields = (
            'id',
            'name',
            'age',
            'gender',
            'contact_number',
            'email',
            'address',
            'medical_history',
            'created_by',
            'created_by_name',
            'created_by_email',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')

    def validate_age(self, value):
        if value < 0 or value > 130:
            raise serializers.ValidationError('Age must be between 0 and 130.')
        return value

    def validate_contact_number(self, value):
        val = value.strip()
        if len(val) < 5:
            raise serializers.ValidationError('Contact number must be at least 5 digits.')
        return val
