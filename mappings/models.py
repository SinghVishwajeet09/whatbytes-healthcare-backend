from django.db import models
from patients.models import Patient
from doctors.models import Doctor


class PatientDoctorMapping(models.Model):
    """
    Mapping model linking a patient with an assigned doctor.
    """
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='doctor_mappings'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='patient_mappings'
    )
    notes = models.TextField(blank=True, default='')
    assigned_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-assigned_date']
        constraints = [
            models.UniqueConstraint(
                fields=['patient', 'doctor'],
                name='unique_patient_doctor_mapping'
            )
        ]

    def __str__(self):
        return f"{self.patient.name} -> Dr. {self.doctor.name}"
