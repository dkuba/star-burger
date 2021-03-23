import json

from django.http import JsonResponse
from django.templatetags.static import static


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


def register_order(request):
    try:
        data = json.loads(request.body.decode())
    except ValueError:
        return JsonResponse({
            'error': 'bla bla bla',
        })

    # {'products': [{'product': 3, 'quantity': 1}, {'product': 2, 'quantity': 1},
    #               {'product': 1, 'quantity': 1}], 'firstname': 'Дмитрий',
    #  'lastname': 'Кубарев', 'phonenumber': '+79857791713',
    #  'address': 'ул Маршала Катукова д 3, к 1 479'}
    product_objects = []
    order = Order.objects.create(first_name=data['firstname'],
                                 last_name=data['lastname'],
                                 phone_number=data['phonenumber'],
                                 address=data['address'])

    for product_data in data['products']:
        OrderProducts.objects.create(
            product=Product.objects.get(id=product_data['product']),
            order=order, amount=product_data['quantity'])

    return JsonResponse({})
