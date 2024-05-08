from uuid import uuid4

from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from django.contrib import admin
from .validators import customer_phone_validate, customer_validate_birth_date


# Create your models here.


class Promotion(models.Model):
    """Класс для работы с акциями."""
    description = models.CharField(max_length=255, verbose_name='описание')
    discount = models.FloatField(verbose_name='Процент скидки')


class Collection(models.Model):
    """Класс для работы с категориями."""
    title = models.CharField(max_length=255, verbose_name='Название')
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='+', verbose_name='Рекомендуемый товар')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


# категория
# kategoriya
#


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование продукта')
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)],
                                     verbose_name='Цена')
    inventory = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Кол-во на складе')
    last_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, verbose_name='Категория')
    promotion = models.ManyToManyField(Promotion, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['pk']


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='store/images/')


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    # first_name = models.CharField(verbose_name='Имя покупателя', max_length=255)
    # last_name = models.CharField(verbose_name='Фамилия покупателя', max_length=255)
    # email = models.EmailField(unique=True, verbose_name='Почта')
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, default=None, unique=False)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=255, validators=[customer_phone_validate])
    birth_date = models.DateField(null=True, blank=True, verbose_name='дата рождения',
                                  validators=[customer_validate_birth_date])
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE,
                                  verbose_name='Статус')

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    def __str__(self):
        return f'{self.user.first_name} - {self.user.last_name}'

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
        ordering = ['user__first_name', 'user__last_name']


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETED = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETED, 'Completed'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]

    placed_at = models.DateTimeField(auto_now_add=True, verbose_name='Время оформления')
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING,
                                      verbose_name='Статус')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Покупатель')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Кол-во заказанного')
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')


class Address(models.Model):
    street = models.CharField(max_length=255, verbose_name='Улица')
    city = models.CharField(max_length=255, verbose_name='Город')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Покупатель')


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,
                             verbose_name='Корзина', related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Кол-во товаров')


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
