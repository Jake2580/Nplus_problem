from django.urls import path
from .views import OwnerListView, OwnerView, ReservationListView

app_name = 'reservations'
urlpatterns = [
    path('reservation/', ReservationListView.as_view(), name='reservations-list'),
    path('owner/', OwnerListView.as_view(), name='owners-list'),
    path('owner/<int:id>/', OwnerView.as_view(), name='owners-detail'),
]
