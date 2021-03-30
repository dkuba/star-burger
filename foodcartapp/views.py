import json

from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Order, OrderProducts


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    data = request.data
    try:
        validate_api_order_request(data)
    except Exception as e:
        return Response({"error": str(e)},
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    order = Order.objects.create(first_name=data['firstname'],
                                 last_name=data['lastname'],
                                 phone_number=data['phonenumber'],
                                 address=data['address'])

    for product_data in data['products']:
        OrderProducts.objects.create(
            product=Product.objects.get(id=product_data['product']),
            order=order, amount=product_data['quantity'])

    return Response({}, status=status.HTTP_200_OK)


def validate_api_order_request(data):
    if any([isinstance(data['products'], str), not data['products'], ]):
        raise Exception('Список продуктов неверного формата или отсутствует')

