from ckeditor.fields import RichTextField
from django.db import models

YES_OR_NO = (
    (True, 'Yes'),
    (False, 'No')
)


class Category(models.Model):
    # objects = models.CharField(max_length=200, unique=200)
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    category_image = models.ImageField(upload_to='static/categories/', blank=True)
    price = models.IntegerField()
    stock = models.IntegerField()
    status_choices = (
        ('New', 'New'),
        ('Old', 'Old'),

    )
    status = models.CharField(max_length=15, choices=status_choices, default=status_choices[0][0])

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Khi xóa category thì Product bị xóa
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name


class Infor(models.Model):
    title_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.CharField(max_length=200, unique=True)
    number_phone = models.CharField(max_length=20, unique=True)
    contact = models.CharField(max_length=50, unique=True)
    adress = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title_name


class Baotri(models.Model):
    title_name = models.CharField(max_length=200, unique=True)
    hoatdong_name = RichTextField(null=True, blank=True)
    status = models.TextField(max_length=500, null=True)

    def __str__(self):
        return self.title_name


# Create your models here.


class Order(models.Model):
    first_name = models.CharField(max_length=400)
    last_name = models.CharField(max_length=400)
    address = models.CharField(max_length=600)
    city = models.CharField(max_length=400)
    payment_methosd = models.CharField(max_length=400)
    payment_data = models.CharField(max_length=400)
    items = models.TextField()
    fulfilled = models.BooleanField()


class Imageslide(models.Model):
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, default=1)
    image_name = models.ImageField(upload_to='static/imageslide/', blank=True)
