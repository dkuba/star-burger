from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer, Serializer

from foodcartapp.models import Product, OrderProducts, Order


class OrderSerializer(ModelSerializer):
     class Meta:
         model = Order


class OrderProductsSerializer(ModelSerializer):
    product = IntegerField()

    def validate_product(self, value):
        if value not in [product.id for
                         product in Product.objects.all()]:
            raise ValidationError("Неверный id продукта")
        return value

    class Meta:
        model = OrderProducts
        fields = ['product', 'quantity']


class ProductSerializer(Serializer):
    quantity = IntegerField()
    product = IntegerField()

    def validate_product(self, value):
        if value not in [product.id for
                         product in Product.objects.all()]:
            raise ValidationError("Неверный id продукта")
        return value


class OrderSerializer(ModelSerializer):

    products = OrderProductsSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'firstname', 'status', 'lastname', 'phonenumber',
                  'address', 'products', 'payment_method']
        write_only_fields = ['products', ]
