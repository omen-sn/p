from django.conf import settings
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db import models
import random

# Create your models here.
UKRAINIAN_MAP = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g',
    'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
    'и': 'y', 'і': 'i', 'ї': 'yi', 'й': 'i', 'к': 'k',
    'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
    'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
    'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
    'ь': '', 'ю': 'iu', 'я': 'ia'
}

def custom_slugify(value):
    for ukr, lat in UKRAINIAN_MAP.items():
        value = value.replace(ukr, lat).replace(ukr.upper(), lat.capitalize())
    return slugify(value)

class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Product.Status.PUBLISHED)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Name")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Product(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Draft'
        PUBLISHED = 1, 'Published'

    title = models.CharField(max_length=255, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    in_stock = models.IntegerField(default=0, verbose_name='Quantity in stock')  # Замість Boolean використовуємо Integer для кількості
    category = models.ForeignKey('Category', on_delete=models.PROTECT, default=4, related_name='products', verbose_name='Category')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Date of addition')  # Дата додавання товару
    date_update = models.DateTimeField(auto_now=True, verbose_name='Date of the last change')  # Дата змінення товару
    supplier = models.CharField(max_length=255, blank=True, verbose_name='Supplier')  # Постачальник
    is_published = models.BooleanField(choices=Status.choices, default=Status.PUBLISHED, verbose_name='Published')
    tags = models.ManyToManyField('TagProduct', blank=True, related_name='tags', verbose_name='Tags')
    detail = models.OneToOneField('ProductDetail', on_delete=models.SET_NULL, null=True, blank=True, related_name='product', verbose_name='More information')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, verbose_name='Image')  # шлях 'product_images/' вказує на каталог, де будуть зберігатися зображення
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1, verbose_name='User who added the product')  # зв'язок з моделлю користувача

    objects = models.Manager()
    published = ProductManager()
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

        ordering = ['-date_added']
        indexes = [
            models.Index(fields=['-date_added'])
        ]
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.pk:  # Якщо це новий запис
            super(Product, self).save(*args, **kwargs)  # Зберегти об'єкт, щоб отримати ID

        if not self.slug:
            # Створити слаг з назви та рандомного числа, враховуючи українські символи
            self.slug = custom_slugify(f'{self.title}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}')

        super(Product, self).save(*args, **kwargs)


class TagProduct(models.Model):
    tag = models.CharField(max_length=100, db_index=True, verbose_name='Tag')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})



class ProductDetail(models.Model):
    detailed_description = models.TextField(verbose_name='Detailed description')
    warranty_information = models.TextField(blank=True, null=True, verbose_name='Warranty information')
    usage_instructions = models.TextField(blank=True, null=True, verbose_name='Usage instructions')

    def __str__(self):
        return f'Detail for {self.product.title if self.product else "No product"}'