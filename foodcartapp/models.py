from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField('название', max_length=50)
    address = models.CharField('адрес', max_length=100, blank=True)
    contact_phone = models.CharField('контактный телефон', max_length=50,
                                     blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'


class ProductQuerySet(models.QuerySet):
    def available(self):
        return self.distinct().filter(menu_items__availability=True)


class ProductCategory(models.Model):
    name = models.CharField('название', max_length=50)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('название', max_length=50)
    category = models.ForeignKey(ProductCategory, null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name='категория',
                                 related_name='products')
    price = models.DecimalField('цена', max_digits=8, decimal_places=2,
                                validators=[MinValueValidator(0)])
    image = models.ImageField('картинка')
    special_status = models.BooleanField('спец.предложение', default=False,
                                         db_index=True)
    description = models.TextField('описание', max_length=256, blank=True)

    objects = ProductQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,
                                   related_name='menu_items',
                                   verbose_name="ресторан")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='menu_items',
                                verbose_name='продукт')
    availability = models.BooleanField('в продаже', default=True,
                                       db_index=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]


class Order(models.Model):
    firstname = models.CharField('Имя', max_length=50, db_index=True)
    lastname = models.CharField('Фамилия', max_length=50, db_index=True)
    phonenumber = PhoneNumberField(verbose_name='Тел.', db_index=True)
    address = models.TextField('Адрес')
    products = models.ManyToManyField(Product, related_name="order_product",
                                      verbose_name='Позиции заказа',
                                      through='OrderProducts')
    status = models.CharField('Сатус', max_length=20, choices=[
        ('Обработан', 'Обработан'), ('Не обработан', 'Не обработан')],
                              default='Не обработан')
    comment = models.TextField('Комментарий', null=True, blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.firstname} {self.lastname}, {self.address}'


class OrderProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name='продукт')
    product_price = models.DecimalField(verbose_name='Цена',
                                        max_digits=6, decimal_places=2,
                                        validators=[MinValueValidator(0)])
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Количество')

    class Meta:
        ordering = ['product', ]
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'
