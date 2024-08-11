
from django.contrib import admin
from django.urls import path, include

# from carRentalSales.carRentalSalesapp.admin import admin_site

urlpatterns = [
    # path('', include('carRentalSalesapp.urls')),
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
