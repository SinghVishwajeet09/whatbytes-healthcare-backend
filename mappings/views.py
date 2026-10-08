from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import PatientDoctorMapping
from .serializers import (
    PatientDoctorMappingReadSerializer,
    PatientDoctorMappingCreateSerializer
)
from patients.models import Patient


class MappingListCreateView(APIView):
    """
    Handle patient-doctor mappings:
    - POST /api/mappings/ : Assign a doctor to a patient
    - GET /api/mappings/ : Retrieve all patient-doctor mappings
    """
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        summary="List all patient-doctor mappings",
        description="Retrieve all patient-doctor mappings for patients created by the authenticated user.",
        responses={200: PatientDoctorMappingReadSerializer(many=True)},
        tags=["Mappings"]
    )
    def get(self, request):
        patient_id = request.query_params.get('patient_id')
        user = request.user

        queryset = PatientDoctorMapping.objects.select_related('patient', 'doctor')
        if not user.is_staff:
            queryset = queryset.filter(patient__created_by=user)

        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)

        serializer = PatientDoctorMappingReadSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Assign doctor to patient",
        description="Assign a doctor to a patient.",
        request=PatientDoctorMappingCreateSerializer,
        responses={
            201: PatientDoctorMappingReadSerializer,
            400: OpenApiResponse(description="Validation error or duplicate assignment"),
        },
        tags=["Mappings"]
    )
    def post(self, request):
        serializer = PatientDoctorMappingCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            mapping = serializer.save()
            return Response(
                {
                    'message': 'Doctor assigned to patient successfully.',
                    'mapping': PatientDoctorMappingReadSerializer(mapping).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MappingPatientOrDetailView(APIView):
    """
    Dual-purpose view to satisfy assignment specifications:
    - GET /api/mappings/<patient_id>/ : Get all doctors assigned to a specific patient.
    - DELETE /api/mappings/<id>/ : Remove a doctor from a patient (delete mapping by mapping ID).
    """
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        summary="Get all doctors assigned to a specific patient",
        description="Retrieve all doctors assigned to the specified patient ID.",
        responses={
            200: PatientDoctorMappingReadSerializer(many=True),
            404: OpenApiResponse(description="Patient not found"),
        },
        tags=["Mappings"]
    )
    def get(self, request, lookup_id):
        # Treat lookup_id as patient_id
        user = request.user
        if user.is_staff:
            patient = get_object_or_404(Patient, pk=lookup_id)
        else:
            patient = get_object_or_404(Patient, pk=lookup_id, created_by=user)

        mappings = PatientDoctorMapping.objects.filter(
            patient=patient
        ).select_related('doctor', 'patient')

        serializer = PatientDoctorMappingReadSerializer(mappings, many=True)
        return Response(
            {
                'patient_id': patient.id,
                'patient_name': patient.name,
                'total_assigned': mappings.count(),
                'assigned_doctors': serializer.data
            },
            status=status.HTTP_200_OK
        )

    @extend_schema(
        summary="Remove doctor from patient",
        description="Remove a doctor assignment from a patient by mapping ID.",
        responses={
            204: OpenApiResponse(description="Mapping removed successfully"),
            404: OpenApiResponse(description="Mapping not found"),
        },
        tags=["Mappings"]
    )
    def delete(self, request, lookup_id):
        # Treat lookup_id as mapping_id
        user = request.user
        if user.is_staff:
            mapping = get_object_or_404(PatientDoctorMapping, pk=lookup_id)
        else:
            mapping = get_object_or_404(
                PatientDoctorMapping,
                pk=lookup_id,
                patient__created_by=user
            )

        mapping.delete()
        return Response(
            {'message': 'Doctor removed from patient successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )


class MappingDetailDirectView(APIView):
    """
    Explicit endpoints for clarity:
    - DELETE /api/mappings/remove/<int:mapping_id>/
    - GET /api/mappings/patient/<int:patient_id>/
    """
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, mapping_id):
        user = request.user
        if user.is_staff:
            mapping = get_object_or_404(PatientDoctorMapping, pk=mapping_id)
        else:
            mapping = get_object_or_404(
                PatientDoctorMapping,
                pk=mapping_id,
                patient__created_by=user
            )
        mapping.delete()
        return Response(
            {'message': 'Doctor removed from patient successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )
