from django.urls import path
from .views import MappingListCreateView, MappingPatientOrDetailView, MappingDetailDirectView

urlpatterns = [
    # POST /api/mappings/ (Assign doctor to patient), GET /api/mappings/ (Retrieve all mappings)
    path('', MappingListCreateView.as_view(), name='mapping-list-create'),

    # GET /api/mappings/<patient_id>/ (Get doctors assigned to patient)
    # DELETE /api/mappings/<id>/ (Remove doctor from patient)
    path('<int:lookup_id>/', MappingPatientOrDetailView.as_view(), name='mapping-patient-or-detail'),

    # Dedicated alias endpoints for testing convenience
    path('patient/<int:lookup_id>/', MappingPatientOrDetailView.as_view(), name='mapping-patient-detail'),
    path('remove/<int:mapping_id>/', MappingDetailDirectView.as_view(), name='mapping-delete-direct'),
]
