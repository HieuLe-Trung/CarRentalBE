from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    is_active = models.BooleanField(default=True)
    avatar = CloudinaryField(folder="avatarUserCar", null=False, blank=False, default='')
    phone = models.CharField(max_length=10, unique=True, null=True)
    email = models.EmailField(max_length=50, unique=True)
    rate = models.FloatField(null=True, blank=True, default=0.0)


class Category(BaseModel):
    name = models.CharField(max_length=30)


class Car(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    mileage = models.IntegerField()
    price = models.FloatField(null=True, blank=True)  # giá có thể trông nếu đăng bài cho thue
    price_per_day = models.FloatField(null=True, blank=True)  # trông nếu chỉ bán
    status = models.CharField(max_length=50)  # vẫn còn, đã bán, đang cho thuê





