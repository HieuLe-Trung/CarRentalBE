from cloudinary.models import CloudinaryResource
from django.contrib import admin
from django.utils.html import mark_safe
from .models import User, Category, RentCar, SaleCar, ImageSale, ImageRent, Rental


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_staff']
    search_fields = ['username', 'email']

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('password'):
            # Kiểm tra xem mật khẩu có được băm chưa
            raw_password = form.cleaned_data['password']
            if not obj.password.startswith('pbkdf2'):
                obj.set_password(raw_password)
        super().save_model(request, obj, form, change)


class CateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'Hãng_Xe']
    readonly_fields = ['Hãng_Xe']
    search_fields = ['name']

    def Hãng_Xe(self, obj):
        if obj.image:
            if type(obj.image) is CloudinaryResource:
                return mark_safe(
                    f'<img src="{obj.image.url}" height="200"  width="300" alt="avatar" />'
                )
            return mark_safe(
                f'<img src="{obj.image.name}" height="200" width="300" alt="avatar" />'
            )


class ImageSaleCarInlineAdmin(admin.StackedInline):
    model = ImageSale
    extra = 0
    fk_name = 'sale_car'


class ImageRentCarInlineAdmin(admin.StackedInline):
    model = ImageRent
    extra = 0
    fk_name = 'rent_car'


class RentCarAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','category']
    search_fields = ['name']
    inlines = [ImageRentCarInlineAdmin, ]


class SaleCarAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','category']
    search_fields = ['name']
    inlines = [ImageSaleCarInlineAdmin, ]


admin.site.register(User,UserAdmin)
admin.site.register(Category, CateAdmin)
admin.site.register(RentCar, RentCarAdmin)  # Quản lý các xe đang cho thue
admin.site.register(SaleCar, SaleCarAdmin)  # Quản lý các xe đang bán
admin.site.register(Rental)
