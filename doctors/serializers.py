from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for Doctor model with validation and read-only metadata."""

    created_by_name = serializers.ReadOnlyField(source='created_by.name', default=None)

    class Meta:
        model = Doctor
        fields = (
            'id',
            'name',
            'specialization',
            'contact_number',
            'email',
            'years_of_experience',
            'hospital_affiliation',
            'created_by',
            'created_by_name',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')

    def validate_contact_number(self, value):
        val = value.strip()
        if len(val) < 5:
            raise serializers.ValidationError('Contact number must be at least 5 digits.')
        return val

    def validate_years_of_experience(self, value):
        if value < 0 or value > 80:
            raise serializers.ValidationError('Years of experience must be between 0 and 80.')
        return value
