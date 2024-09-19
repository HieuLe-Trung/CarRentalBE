from rest_framework import viewsets, generics, permissions
from rest_framework.parsers import MultiPartParser

from .perms import IsEmployee
from .serializers import UserSerializer, CateSerializer, RentCarSerializer, SaleCarSerializer
from .models import User, Category, RentCar, SaleCar


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CateSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsEmployee()]
        return [permissions.AllowAny()]


class CategoryView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CateSerializer

    def get_permissions(self):
        return [IsEmployee()]


class RentCarViewSet(viewsets.ModelViewSet):
    queryset = RentCar.objects.all()
    serializer_class = RentCarSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [permissions.AllowAny()]
        return [IsEmployee()]


class SaleCarViewSet(viewsets.ModelViewSet):
    queryset = SaleCar.objects.all()
    serializer_class = SaleCarSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [permissions.AllowAny()]
        return [IsEmployee()]
