import datetime
from datetime import datetime
from decimal import Decimal

from django.utils import timezone
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from . import serializers
from .perms import IsEmployee
from .serializers import UserSerializer, CateSerializer, RentCarDetailSerializer, SaleCarDetailSerializer, \
    RentCarSerializer, SaleCarSerializer, FavoriteRentCarSerializer, FavoriteSaleCarSerializer, RentalSerializer
from .models import User, Category, RentCar, SaleCar, FavoriteRentCar, FavoriteSaleCar, Rental


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

    def get_serializer_class(self):
        if self.action == 'list':
            return RentCarSerializer
        return RentCarDetailSerializer

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

    @action(methods=['get'], detail=False, url_path='available')
    def available_cars(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response({"detail": "Vui lòng cung cấp ngày bắt đầu và ngày kết thúc."},
                            status=status.HTTP_400_BAD_REQUEST)
        # Truy vấn những xe đã đặt
        booked_cars = Rental.objects.filter(
            start_date__lt=end_date,
            end_date__gt=start_date
        ).values_list('car', flat=True)

        available_cars = self.queryset.exclude(id__in=booked_cars)  # Exclude: tìm những xe khong nằm trong ds

        serializer = self.get_serializer(available_cars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SaleCarViewSet(viewsets.ModelViewSet):
    queryset = SaleCar.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SaleCarSerializer
        return SaleCarDetailSerializer

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


class FavoriteViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def add_to_favorites(self, request, car_type, car_id):
        if car_type == 'rent':
            rent_car = RentCar.objects.filter(id=car_id).first()
            if not rent_car:
                return Response({"detail": "Xe cho thuê không được tìm thấy."}, status=status.HTTP_404_NOT_FOUND)

            favorite = FavoriteRentCar.objects.filter(user=request.user, rent_car=rent_car).first()
            if favorite:
                favorite.delete()
                return Response({"detail": "Đã xóa khỏi danh sách yêu thích."}, status=status.HTTP_200_OK)
            else:
                FavoriteRentCar.objects.create(user=request.user, rent_car=rent_car)
                return Response({"detail": "Đã thêm vào danh sách yêu thích."}, status=status.HTTP_201_CREATED)

        elif car_type == 'sale':
            sale_car = SaleCar.objects.filter(id=car_id).first()
            if not sale_car:
                return Response({"detail": "Xe bán không được tìm thấy."}, status=status.HTTP_404_NOT_FOUND)

            favorite = FavoriteSaleCar.objects.filter(user=request.user, sale_car=sale_car).first()
            if favorite:
                favorite.delete()
                return Response({"detail": "Đã xóa khỏi danh sách yêu thích."}, status=status.HTTP_200_OK)
            else:
                FavoriteSaleCar.objects.create(user=request.user, sale_car=sale_car)
                return Response({"detail": "Đã thêm vào danh sách yêu thích."}, status=status.HTTP_201_CREATED)

        return Response({"detail": "Loại xe không hợp lệ."}, status=status.HTTP_400_BAD_REQUEST)

    def list_favorites(self, request, car_type):
        if car_type == 'rent':
            favorites = FavoriteRentCar.objects.filter(user=request.user).select_related('rent_car')
            serializer = FavoriteRentCarSerializer(favorites, many=True)
            return Response(serializer.data)

        elif car_type == 'sale':
            favorites = FavoriteSaleCar.objects.filter(user=request.user).select_related('sale_car')
            serializer = FavoriteSaleCarSerializer(favorites, many=True)
            return Response(serializer.data)

        return Response({"detail": "Loại xe không hợp lệ."}, status=status.HTTP_400_BAD_REQUEST)


class RentalViewSet(viewsets.ViewSet,):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

    def get_permissions(self):
        if self.action == 'confirm_return':
            return [IsEmployee()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        rent_car_id = request.data.get('rent_car_id')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        rent_car = RentCar.objects.get(id=rent_car_id)

        # Tính toán số ngày thuê
        start_date_dt = timezone.datetime.fromisoformat(start_date)
        end_date_dt = timezone.datetime.fromisoformat(end_date)
        rental_days = (end_date_dt - start_date_dt).days

        # Tính tổng giá thuê
        total_rental_price = rental_days * rent_car.price_per_day

        # Tạo một phiếu thuê mới khi gửi yêu cau thue
        rental_data = {
            "renter": request.user.id,
            "car": rent_car_id,
            "start_date": start_date_dt,
            "end_date": end_date_dt,
            "total_rental_price": total_rental_price
        }

        rental_serializer = self.get_serializer(data=rental_data)
        if rental_serializer.is_valid():
            rental_serializer.save()
            return Response(rental_serializer.data, status=status.HTTP_201_CREATED)

        return Response(rental_serializer.errors, status=status.HTTP_400_BAD_REQUEST)