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
    license_number = models.CharField(max_length=20, blank=True)
    license_verified = models.BooleanField(default=False)  # true khi store duyệt gplx


class Category(BaseModel):
    name = models.CharField(max_length=30)
    image = CloudinaryField(folder="cateCar", null=False, blank=False, default='')


class Car(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    quantity = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50)  # vẫn còn, đã bán, đang cho thuê


class Image(models.Model):
    image = CloudinaryField(folder="ImgCar", null=True, blank=True)
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE, default=None)


class Rental(BaseModel):
    renter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    price_per_day = models.FloatField(null=True, blank=True)
    mileage = models.IntegerField()
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField()
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ('user', 'car', 'rental')


class Sale(BaseModel):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField(null=True, blank=True)
    sale_date = models.DateTimeField(auto_now=True)


class FavoriteCar(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'car')


class Maintenance(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    service_date = models.DateField()
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)


class RefundRequest(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE)
    reason = models.TextField()
    bank_account_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
