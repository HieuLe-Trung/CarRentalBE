from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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
    address = models.CharField(max_length=100, default='')
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
    rental_count = models.PositiveIntegerField(default=0)
    average_rating = models.FloatField(default=0)
    status = models.CharField(max_length=50)  # sẵn xe, đang cho thue, sold


class SaleCar(Car):
    price = models.FloatField(null=True, blank=True)
    mileage = models.IntegerField(default=0)
    sold = models.BooleanField(default=False)


class ImageRent(models.Model):
    image = CloudinaryField(folder="ImgRentCar", null=True, blank=True)
    rent_car = models.ForeignKey(RentCar, related_name='images', on_delete=models.CASCADE, default=None)


class ImageSale(models.Model):
    image = CloudinaryField(folder="ImgSaleCar", null=True, blank=True)
    sale_car = models.ForeignKey(SaleCar, related_name='images', on_delete=models.CASCADE, default=None)


class Rental(BaseModel):  # phiếu thuê
    renter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(RentCar, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_rental_price = models.DecimalField(max_digits=10, decimal_places=2, null=True,
                                             blank=True)  # dễ thống kê doanh thu
    actual_return_date = models.DateTimeField(null=True, blank=True)  # Ngày trả xe thực tế
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Phí phạt trả trễ
    confirmation_status = models.CharField(max_length=20, default='')  # xác nhận của cửa hàng khi nhận được tiền mặt


class Deposit(BaseModel):
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE, null=True,
                                  blank=True)  # 1 phiếu thuê tđ với 1 phiếu cọc
    sale = models.ForeignKey(SaleCar, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_payment_status = models.CharField(
        max_length=20)  # để kiểm tra xem những ngay đã cọc sẽ vô hiệu hóa cho thuê


class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)


class Payment(BaseModel):
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20)  # đã thanh toán, chưa thanh toán


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    car = models.ForeignKey(RentCar, on_delete=models.CASCADE, related_name='reviews')
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE,
                                  related_name='review')  # chỉ những xe đã được thue(có phiếu thuê) mới được đánh giá
    rating = models.IntegerField()
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ('user', 'car', 'rental')


class FavoriteRentCar(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rent_car = models.ForeignKey(RentCar, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'rent_car')


class FavoriteSaleCar(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sale_car = models.ForeignKey(SaleCar, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'sale_car')


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
