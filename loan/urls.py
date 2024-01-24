from django.contrib import admin
from django.urls import path, include
from .views import ingest_data

from rest_framework import routers

from .viewsets import CustomerViewSet, CheckEligibilityView, CreateLoanView, LoanViewSet

router = routers.DefaultRouter()
router.register('customer', CustomerViewSet)
router.register('loan', LoanViewSet)



urlpatterns = [
    path('ingest/', ingest_data),
    path('check-eligibility/', CheckEligibilityView.as_view()),
    path('create-loan/', CreateLoanView.as_view()),
]

urlpatterns += router.urls