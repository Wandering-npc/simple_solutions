from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Item(models.Model):
    """
    Модель товара.

    Атрибуты:
        - name (CharField): Название товара.
        - description (TextField): Описание товара.
        - price (DecimalField): Цена товара.
        - currency (CharField): Валюта товара ('USD' или 'EUR').

    Методы:
        - __str__: Возвращает строковое представление товара.
    """
    CUR = (
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    )
    name = models.CharField(
        unique=True,
        max_length=256,
        verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2
    )
    currency = models.CharField(
        max_length=10,
        default='USD',
        choices=CUR)

    def __str__(self):
        return self.name

class Discount(models.Model):
    """
    Модель скидки.

    Атрибуты:
        - percent_off (IntegerField): Процент скидки.

    Методы:
        - __str__: Возвращает строковое представление скидки.
    """
    percent_off = models.IntegerField(
        null=True,
        default=None,
        validators=[MinValueValidator(1), MaxValueValidator(99)])

    def __str__(self):
        return f'{self.percent_off}%'

class Tax(models.Model):
    """
    Модель налога.

    Атрибуты:
        - value (IntegerField): Процент налога.
        - name (CharField): Название налога.
        - stripe_id (CharField): Идентификатор налога в Stripe.

    Методы:
        - __str__: Возвращает строковое представление налога.
    """
    value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)])
    name = models.CharField(max_length=30, unique=True)
    stripe_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.name) + ' - ' + f'{self.value}%'

class Order(models.Model):
    """
    Модель заказа.

    Атрибуты:
        - customer (ForeignKey): Пользователь, оформивший заказ.
        - items (ManyToManyField): Товары в заказе через модель OrderItem.
        - is_paid (BooleanField): Статус оплаты заказа.
        - created (DateTimeField): Дата и время создания заказа.
        - updated (DateTimeField): Дата и время последнего обновления заказа.
        - tax (ForeignKey): Налог на заказ.
        - discount (ForeignKey): Скидка на заказ.

    Методы:
        - get_total_cost: Возвращает общую стоимость заказа.
        - __str__: Возвращает строковое представление заказа.
    """
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders')
    items = models.ManyToManyField('Item', through='OrderItem')
    is_paid = models.BooleanField(default=False, verbose_name='Статус')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    tax = models.ForeignKey(
        Tax,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    discount = models.ForeignKey(
        Discount,
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    def get_total_cost(self):
        return sum(item_order.get_cost() for item_order in self.items.all())

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    """
    Модель связи между товарами и заказами.

    Атрибуты:
        - order (ForeignKey): Заказ, к которому относится элемент.
        - item (ForeignKey): Товар, который связан с элементом заказа.
        - quantity (PositiveIntegerField): Количество товара в заказе.

    Методы:
        - __str__: Возвращает строковое представление элемента заказа.
        - get_cost: Возвращает стоимость элемента заказа.
    """
    order = models.ForeignKey(
        Order,
        related_name='order_items',
        on_delete=models.CASCADE)
    item = models.ForeignKey(
        Item,
        related_name='order_items',
        on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.item)

    def get_cost(self):
        return self.item.price * self.quantity