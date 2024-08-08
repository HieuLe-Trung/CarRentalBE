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

    def __str__(self):
        return self.name


class Car(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, default='')
    model = models.CharField(max_length=100)  # kiểu dáng, phiên bản
    fuel_type = models.CharField(max_length=50, default='')  # loại nhiên lieu
    transmission = models.CharField(max_length=50, default='')  # loại hộp số
    seats = models.IntegerField(default=0)
    interior_color = models.CharField(max_length=50, default='')  # màu noi thất
    condition = models.CharField(max_length=10, default='')  # tình trạng (new - used)
    origin = models.CharField(max_length=10, default='')  # xuất  xứ (domestic - imported)
    color = models.CharField(max_length=50, default='')
    year = models.IntegerField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class RentCar(Car):  # đăng xe cho thuê
    price_per_day = models.FloatField()
    mileage = models.IntegerField(default=0)
    status = models.CharField(max_length=50)


class SaleCar(Car):
    price = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)


class Image(models.Model):
    image = CloudinaryField(folder="ImgCar", null=True, blank=True)
    rent_car = models.ForeignKey(RentCar, on_delete=models.CASCADE, default=None)
    sale_car = models.ForeignKey(SaleCar, on_delete=models.CASCADE, default=None)


class Rental(BaseModel):  # phiếu thuê
    renter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(RentCar, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_rental_price = models.DecimalField(max_digits=10, decimal_places=2, null=True,
                                             blank=True)  # dễ thống kê doanh thu


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    car = models.ForeignKey(RentCar, on_delete=models.CASCADE, related_name='reviews')
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE, related_name='review')  # chỉ những xe đã được thue(có phiếu thuê) mới được đánh giá
    rating = models.IntegerField()
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ('user', 'car', 'rental')


class Sale(BaseModel):  # phiếu bán
    car = models.ForeignKey(SaleCar, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    sale_date = models.DateTimeField(auto_now=True)


class FavoriteCar(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rent_car = models.ForeignKey(RentCar, on_delete=models.CASCADE, null=True, blank=True)  # khi user tim xe thuê thi set sale_car là null
    sale_car = models.ForeignKey(SaleCar, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'rent_car', 'sale_car')


class Maintenance(models.Model):
    car = models.ForeignKey(SaleCar, on_delete=models.CASCADE)
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
