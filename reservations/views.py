from django.shortcuts import render
from django.views import View

from reservations.models import Owner, Reservation

# Create your views here.
class ReservationListView(View):
    template_name = 'reservations/reservation_list.html'

    def get(self, request, *args, **kwargs):
        result = request.GET.get('result') or 'all'
        if 'all' in result:
            self.queryset = Reservation.objects.all()
        elif 'fetch' in result:
            self.queryset = Reservation.objects.prefetch_related('owner_id')
        elif 'select' in result:
            self.queryset = Reservation.objects.select_related('owner_id')
        else:
            self.queryset = None
            
        context = {'object_list': self.queryset}
        return render(request, self.template_name, context)

class OwnerListView(View):
    template_name = 'reservations/owner_list.html'

    def get(self, request, *args, **kwargs):
        self.queryset = Owner.objects.all()
        context = {'object_list': self.queryset}
        return render(request, self.template_name, context)
