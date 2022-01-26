from django.shortcuts import get_object_or_404, render
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
            self.queryset = Reservation.objects.prefetch_related('owner')
        elif 'select' in result:
            self.queryset = Reservation.objects.select_related('owner')
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

class OwnerView(View):
    template_name = 'reservations/owner_detail.html'  # DetailView

    model = Owner

    def get_object(self):
        id = self.kwargs.get('id')

        if id is None:
            return None

        obj = get_object_or_404(self.model, id=id)
        return obj
    
    # GET Method
    def get(self, request, id=None, *args, **kwargs):
        obj = self.get_object()
        context = dict(object=obj, owners=obj.owners.all())
        return render(request, self.template_name, context)
