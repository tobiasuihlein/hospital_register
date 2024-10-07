from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'hospital_locations', views.HospitalLocationsView, 'hospital_location')
router.register(r'hospital_details', views.HospitalDetailsView, 'hospital_detail')

urlpatterns = router.urls