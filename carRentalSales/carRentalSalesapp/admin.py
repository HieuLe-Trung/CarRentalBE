from cloudinary.models import CloudinaryResource
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import mark_safe
from .models import User, Category, RentCar, SaleCar, Image


# class HCarAppAdminSite(AdminSite):
#     site_title = 'Trang quản trị HCAR'
#     site_header = 'Hệ thống Quản lý cửa hàng XE Ô TÔ HCAR'
#     index_title = 'Trang chủ quản trị'


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
    model = Image
    extra = 0
    fk_name = 'sale_car'


class ImageRentCarInlineAdmin(admin.StackedInline):
    model = Image
    extra = 0
    fk_name = 'rent_car'


class RentCarAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    inlines = [ImageRentCarInlineAdmin, ]


class SaleCarAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    inlines = [ImageSaleCarInlineAdmin, ]


# admin_site = HCarAppAdminSite(name='myHCar')

admin.site.register(Category, CateAdmin)
admin.site.register(RentCar, RentCarAdmin)  # Quản lý các xe đang cho thue
admin.site.register(SaleCar, SaleCarAdmin)  # Quản lý các xe đang bán
