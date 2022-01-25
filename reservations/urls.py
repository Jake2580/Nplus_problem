from django.urls import path
from .views import OwnerListView, ReservationListView

app_name = 'reservations'
urlpatterns = [
    path('reservation/', ReservationListView.as_view(), name='reservations-list'),
    path('owner/', OwnerListView.as_view(), name='owners-list'),
]
