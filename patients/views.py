from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import Patient
from .serializers import PatientSerializer


class PatientListCreateView(generics.ListCreateAPIView):
    """
    List all patients created by the authenticated user, or create a new patient.
    - GET /api/patients/ : Retrieve all patients created by the authenticated user
    - POST /api/patients/ : Add a new patient
    """
    serializer_class = PatientSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Only return patients created by the currently authenticated user
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @extend_schema(
        summary="List user's patients",
        description="Retrieve all patients created by the authenticated user.",
        responses={200: PatientSerializer(many=True)},
        tags=["Patients"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new patient",
        description="Add a new patient record assigned to the authenticated user.",
        request=PatientSerializer,
        responses={
            201: PatientSerializer,
            400: OpenApiResponse(description="Validation error"),
        },
        tags=["Patients"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific patient record.
    - GET /api/patients/<id>/ : Get details of a specific patient
    - PUT /api/patients/<id>/ : Update patient details
    - PATCH /api/patients/<id>/ : Partially update patient details
    - DELETE /api/patients/<id>/ : Delete a patient record
    """
    serializer_class = PatientSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Ensure user can only view/modify their own patient records
        return Patient.objects.filter(created_by=self.request.user)

    @extend_schema(
        summary="Get patient details",
        description="Retrieve details of a specific patient created by the authenticated user.",
        responses={
            200: PatientSerializer,
            404: OpenApiResponse(description="Patient not found"),
        },
        tags=["Patients"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update patient",
        description="Update details of a specific patient.",
        request=PatientSerializer,
        responses={
            200: PatientSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="Patient not found"),
        },
        tags=["Patients"]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update patient",
        description="Partially update fields of a specific patient.",
        request=PatientSerializer,
        responses={
            200: PatientSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="Patient not found"),
        },
        tags=["Patients"]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Delete patient",
        description="Delete a patient record belonging to the authenticated user.",
        responses={
            204: OpenApiResponse(description="Patient deleted successfully"),
            404: OpenApiResponse(description="Patient not found"),
        },
        tags=["Patients"]
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Patient record deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )
