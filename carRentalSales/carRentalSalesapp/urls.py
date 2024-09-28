
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import CategoryListCreateView, CategoryView, FavoriteViewSet

router = DefaultRouter()
router.register('user', views.UserViewSet,basename='user')
router.register('rent-car', views.RentCarViewSet,basename='rent-car')
router.register('sale-car', views.SaleCarViewSet,basename='sale-car')

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryView.as_view(), name='category-update-delete'),
    path('favorites/<str:car_type>/<int:car_id>/', FavoriteViewSet.as_view({'post': 'add_to_favorites'}), name='add_to_favorites'),
    path('favorites/<str:car_type>/', FavoriteViewSet.as_view({'get': 'list_favorites'}), name='list_favorites'),

]