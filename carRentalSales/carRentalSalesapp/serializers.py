from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from .models import User, Category, RentCar, SaleCar, ImageRent, ImageSale, FavoriteRentCar, FavoriteSaleCar


class UserSerializer(ModelSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Kiểm tra và lấy URL của hình ảnh từ CloudinaryField
        if instance.avatar:
            rep['avatar'] = instance.avatar.url
        else:
            rep['avatar'] = None
        return rep

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'phone', 'email', 'password', 'avatar']

    read_only_fields = ['id']
    extra_kwargs = {
        'password': {
            'write_only': True
        }
    }

    def create(self, validated_data):
        data = validated_data.copy()

        user = User(**data)
        user.set_password((data['password']))
        user.save()
        return user

    def patch(self, instance, validated_data):
        email = validated_data.get('email', instance.email)
        phone = validated_data.get('phone', instance.phone)

        # Kiểm tra xem email hoặc phone đã tồn tại trong cơ sở dữ liệu hay không
        if User.objects.exclude(id=instance.id).filter(email=email).exists():
            raise ValidationError("Email đã tồn tại trong hệ thống.")
        if User.objects.exclude(id=instance.id).filter(phone=phone).exists():
            raise ValidationError("Số điện thoại đã tồn tại trong hệ thống.")
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class CateSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']


class ImageRentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageRent
        fields = ['id', 'image']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['image'] = instance.image.url
        return rep


class ImageSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageSale
        fields = ['id', 'image']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['image'] = instance.image.url
        return rep


class RentCarSerializer(serializers.ModelSerializer):
    images = ImageRentSerializer(many=True, required=False)

    class Meta:
        model = RentCar
        fields = ['id', 'name', 'category', 'price_per_day', 'images']

    def create(self, validated_data):
        images_data = self.context.get('request').FILES.getlist('images')
        rent = RentCar.objects.create(**validated_data)
        for image_data in images_data:
            ImageRent.objects.create(rent=rent, image=image_data)
        return rent


class RentCarDetailSerializer(RentCarSerializer):
    class Meta:
        model = RentCarSerializer.Meta.model
        fields = RentCarSerializer.Meta.fields + ['model', 'fuel_type', 'transmission', 'seats', 'interior_color',
                                                  'condition', 'origin', 'color', 'year', 'description', 'status']


class SaleCarSerializer(serializers.ModelSerializer):
    images = ImageSaleSerializer(many=True, required=False)

    class Meta:
        model = SaleCar
        fields = ['id', 'name', 'category', 'price', 'images']

    def create(self, validated_data):
        images_data = self.context.get('request').FILES.getlist('images')
        sale_car = SaleCar.objects.create(**validated_data)
        for image_data in images_data:
            ImageSale.objects.create(sale_car=sale_car, image=image_data)
        return sale_car


class SaleCarDetailSerializer(SaleCarSerializer):
    class Meta:
        model = SaleCarSerializer.Meta.model
        fields = SaleCarSerializer.Meta.fields + [
            'model', 'fuel_type', 'transmission', 'seats',
            'interior_color', 'condition', 'origin',
            'color', 'year', 'description', 'mileage', 'sold'
        ]


class FavoriteRentCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRentCar
        fields = ['user', 'rent_car']


class FavoriteSaleCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteSaleCar
        fields = ['user', 'sale_car']