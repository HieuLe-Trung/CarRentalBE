from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User, Category, RentCar, SaleCar, ImageRent, ImageSale


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
        fields = ['id', 'category', 'name', 'model', 'fuel_type', 'transmission', 'seats', 'interior_color',
                  'condition', 'origin', 'color', 'year', 'description', 'price_per_day', 'mileage', 'status', 'images']
        # có cate để post

    def create(self, validated_data):
        images_data = self.context.get('request').FILES.getlist('images')
        rent = RentCar.objects.create(**validated_data)
        for image_data in images_data:
            ImageRent.objects.create(rent=rent, image=image_data)
        return rent


class SaleCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleCar
        fields = ['id', 'name', 'model', 'fuel_type', 'transmission', 'seats', 'interior_color',
                  'condition', 'origin', 'color', 'year', 'description', 'price', 'sold']
