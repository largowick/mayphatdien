from django.contrib import admin
from mayphat.models import Category, Product, Infor, Baotri, Imageslide


class ImagelistAdmin(admin.StackedInline):
    model = Imageslide


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}  # Gợi ý trường slug theo category_name
    inlines = [ImagelistAdmin]


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'created_date', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}


admin.site.register(Product, ProductAdmin)


# Register your models here.
class InforAdmin(admin.ModelAdmin):
    list_display = ('title_name', 'description', 'number_phone', 'contact', 'adress', 'email')
    prepopulated_fields = {'slug': ('title_name',)}


admin.site.register(Infor, InforAdmin)


class BaotriAdmin(admin.ModelAdmin):
    pass


#  def get_queryset(self,request):
#     qs = super(BaotriAdmin, self).get_queryset(request)
#     return qs.filter(title_name='baotri')
admin.site.register(Baotri, BaotriAdmin)

# admin.site.register(Imageslide)
# admin.site.register(Category, LessonAdmin)
