django-admin startproject Nplus_problem
<br>
cd Nplus_problem
<br>
<br>
<br>
### Nplus_problem\settings.py

LANGUAGE_CODE, TIME_ZONE, USE_TZ 변경

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'reservations'
]
```

```python
# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = False
```

```python
# loggers django.db.backends
django_db_loggers = False

def query_log(choice: bool) -> None:
    """[summary]

    Args:
        choice (bool): [description]
    """
    
    if not choice:
        return
    
    global LOGGING
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            }
        },
        'loggers': {
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        }
    }

query_log(django_db_loggers)

```

<br>
python manage.py migrate
<br>
python manage.py createsuperuser
<br>
python manage.py startapp reservations
<br>
<br>
<br>

### Nplus_problem\urls.py

include('reservations.urls')

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('reservations/', include('reservations.urls')),
    path('admin/', admin.site.urls),
]

```

<br>
<br>
<br>

### reservations\models.py

<br>

| Reservation  |
|--------------|
| id: pk       |
| context      |
| owner(Owner): fk |

| Owner  |
|--------|
| id: pk |
| age    |
| name   |

<br>

```python
class Reservation(models.Model):
    context = models.TextField()
    owner = models.ForeignKey(
        'Owner',
        related_name="owners",
        related_query_name="owner",
        on_delete=models.CASCADE,
        db_column="owner"
    )

class Owner(models.Model):
    age = models.IntegerField()
    name = models.CharField(max_length=20)

# ModuleNotFoundError: No module named 'reservations.urls'
```

<br>
<br>
<br>

### reservations\views.py

```python
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

```

<br>
<br>
<br>

### reservations\urls.py

```python
from django.urls import path
from .views import OwnerListView, ReservationListView

app_name = 'reservations'
urlpatterns = [
    path(
        'reservation/',
        ReservationListView.as_view(),
        name='reservations-list'
    ),
    path(
        'owner/',
        OwnerListView.as_view(),
        name='owners-list'
    ),
]

```

<br>
python manage.py makemigrations
<br>
python manage.py migrate
<br>
<br>

reservations\templates\reservations\owner_list.html
<br>
reservations\templates\reservations\reservation_list.html
<br>
<br>

```css
"GET /reservations/reservation/ HTTP/1.1" 200 5
"GET /reservations/owner/ HTTP/1.1" 200 19
```

<br>
<br>
<br>

### reservations\admin.py

```python
from django.contrib import admin

from reservations.models import Owner, Reservation

# Register your models here.
admin.site.register(Reservation)
admin.site.register(Owner)

```

<br>
<br>
alter table reservations_reservation rename column owner_id to owner;
<br>
alter table reservations_reservation rename column content to context;
<br>

```
Reservation
1 - ctx1 - 1(Jake)
2 - ctx2 - 1(Jake)
3 - ctx3 - 2(Chan mini)
4 - ctx4 - 4(홍길동)
5 - ctx5 - 4(홍길동)
6 - ctx6 - 1(Jake)

Owner
1 - 26 - Jake
2 - 26 - Chan mini
3 - 25 - 언우
4 - 573 - 홍길동
```

<br>
<br>
<br>

# objects

http://127.0.0.1:8000/reservations/reservation/
<br>

<br>
objects.all()

```sql
(0.000)
SELECT "reservations_reservation"."id", "reservations_reservation"."context", "reservations_reservation"."owner"
FROM "reservations_reservation"; args=(); alias=default

(0.000)
SELECT "reservations_owner"."id", "reservations_owner"."age", "reservations_owner"."name"
FROM "reservations_owner"
WHERE "reservations_owner"."id" = 1
LIMIT 21; args=(1,); alias=default

(0.000)
SELECT "reservations_owner"."id", "reservations_owner"."age", "reservations_owner"."name"
FROM "reservations_owner"
WHERE "reservations_owner"."id" = 1
LIMIT 21; args=(1,); alias=default

(0.000)
SELECT "reservations_owner"."id", "reservations_owner"."age", "reservations_owner"."name"
FROM "reservations_owner"
WHERE "reservations_owner"."id" = 2
LIMIT 21; args=(2,); alias=default

(0.000)
SELECT "reservations_owner"."id", "reservations_owner"."age", "reservations_owner"."name"
FROM "reservations_owner"
WHERE "reservations_owner"."id" = 4
LIMIT 21; args=(4,); alias=default

(0.000)
SELECT "reservations_owner"."id", "reservations_owner"."age", "reservations_owner"."name"
FROM "reservations_owner"
WHERE "reservations_owner"."id" = 4
LIMIT 21; args=(4,); alias=default

(0.000)
SELECT "reservations_owner"."id", "reservations_owner"."age", "reservations_owner"."name"
FROM "reservations_owner"
WHERE "reservations_owner"."id" = 1
LIMIT 21; args=(1,); alias=default

"GET /reservations/reservation/ HTTP/1.1" 200 232
```

<br>
objects.prefetch_related('owner')

```sql
(0.000)
SELECT "reservations_reservation"."id", "reservations_reservation"."context", "reservations_reservation"."owner"
FROM "reservations_reservation"; args=(); alias=default

(0.000)
SELECT "reservations_owner"."id", "reservations_owner"."age", "reservations_owner"."name"
FROM "reservations_owner"
WHERE "reservations_owner"."id"
IN (1, 2, 4); args=(1, 2, 4); alias=default

"GET /reservations/reservation/?result=fetch HTTP/1.1" 200 232
```

<br>
objects.select_related('owner')

```sql
(0.000)
SELECT
"reservations_reservation"."id",
"reservations_reservation"."context",
"reservations_reservation"."owner",
"reservations_owner"."id",
"reservations_owner"."age",
"reservations_owner"."name"
FROM "reservations_reservation"
INNER JOIN "reservations_owner"
ON ("reservations_reservation"."owner" = "reservations_owner"."id"); args=(); alias=default

"GET /reservations/reservation/?result=select HTTP/1.1" 200 232
```

<br>
http://127.0.0.1:8000/reservations/owner/

```sql
(0.000)
SELECT "reservations_owner"."id", "reservations_owner"."age", "reservations_owner"."name"
FROM "reservations_owner"; args=(); alias=default

"GET /reservations/owner/ HTTP/1.1" 200 136
```

<br>
<br>
<br>

# Owner Detail View

### reservations\views.py

```python
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

```

<br>

### reservations\urls.py

```python
from .views import OwnerListView, OwnerView, ReservationListView

app_name = 'reservations'
urlpatterns = [
    path('reservation/', ReservationListView.as_view(), name='reservations-list'),
    path('owner/', OwnerListView.as_view(), name='owners-list'),
    path('owner/<int:id>/', OwnerView.as_view(), name='owners-detail'),
]

```

<br>

### reservations\templates\reservations\owner_detail.html

```django
{% block content %}

<h1>{{object.id}} - {{object.age}} - {{object.name}}</h1>
{% if owners %}

    <h2>Reservation</h2>
    {% for reservation in owners %}
        {{reservation.id}} - {{reservation.context}}<br>
    {% endfor %}

{% endif %}

{% endblock content %}
```

<br>
