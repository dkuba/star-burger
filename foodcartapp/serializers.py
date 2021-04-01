from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer, Serializer

from foodcartapp.models import Product, OrderProducts, Order


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

    products = OrderProductsSerializer(many=True)

    class Meta:
        model = Order
        fields = ['firstname', 'lastname', 'phonenumber', 'address', 'products']
