from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import Doctor
from .serializers import DoctorSerializer


class DoctorListCreateView(generics.ListCreateAPIView):
    """
    List all doctors or add a new doctor.
    - GET /api/doctors/ : Retrieve all doctors
    - POST /api/doctors/ : Add a new doctor (Authenticated users only)
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @extend_schema(
        summary="List all doctors",
        description="Retrieve all doctors registered in the system.",
        responses={200: DoctorSerializer(many=True)},
        tags=["Doctors"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Add a new doctor",
        description="Register a new doctor (Authenticated users only).",
        request=DoctorSerializer,
        responses={
            201: DoctorSerializer,
            400: OpenApiResponse(description="Validation error"),
        },
        tags=["Doctors"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific doctor record.
    - GET /api/doctors/<id>/ : Get details of a specific doctor
    - PUT /api/doctors/<id>/ : Update doctor details
    - PATCH /api/doctors/<id>/ : Partially update doctor details
    - DELETE /api/doctors/<id>/ : Delete a doctor record
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        summary="Get doctor details",
        description="Retrieve details of a specific doctor.",
        responses={
            200: DoctorSerializer,
            404: OpenApiResponse(description="Doctor not found"),
        },
        tags=["Doctors"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update doctor details",
        description="Update doctor details.",
        request=DoctorSerializer,
        responses={
            200: DoctorSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="Doctor not found"),
        },
        tags=["Doctors"]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update doctor details",
        description="Partially update specific doctor details.",
        request=DoctorSerializer,
        responses={
            200: DoctorSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="Doctor not found"),
        },
        tags=["Doctors"]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Delete doctor",
        description="Delete a doctor record.",
        responses={
            204: OpenApiResponse(description="Doctor deleted successfully"),
            404: OpenApiResponse(description="Doctor not found"),
        },
        tags=["Doctors"]
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Doctor record deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )
