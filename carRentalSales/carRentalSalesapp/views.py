from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from . import serializers
from .perms import IsEmployee
from .serializers import UserSerializer, CateSerializer, RentCarSerializer, SaleCarSerializer
from .models import User, Category, RentCar, SaleCar


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    # lấy thông tin user đang đăng nhập để hiển thị profile
    @action(methods=['get', 'patch', 'delete'], url_name='current_user', detail=False)
    def current_user(self, request):
        if request.method == 'PATCH':
            user = request.user
            serializer = self.get_serializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            user = request.user
            user.is_active = False
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(UserSerializer(request.user).data)


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
