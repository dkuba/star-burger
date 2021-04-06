from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from foodcartapp.models import Product


class ModelsTest(TestCase):

    def test_order_model(self):
        pass

class OrderTestCase(APITestCase):
    def setUp(self):
        Product.objects.create(name='Беконайзер', price='777')
        Product.objects.create(name='Лонг бургер', price='777')
        Product.objects.create(name='Бургер', price='777')
        self.url = '/api/order/'

    def test_proper_data(self):
        response = self.client.post(self.url, """
        {"products": [{"product": 1, "quantity": 1}],
         "firstname": "Dmitri",
         "lastname": "Kubarev",
         "phonenumber": "+79857791213",
         "address": "ул Маршала Катукова"}
         """, content_type='application/json')

        self.assertTrue(status.is_success(response.status_code))

    def test_products_is_string(self):
        response = self.client.post(self.url, """{"products": "HelloWorld",
        "firstname": "1",
        "lastname": "2",
        "phonenumber": "3",
        "address": "4"}""", content_type='application/json')

        self.assertTrue(status.is_client_error(response.status_code))

    def test_products_is_null(self):
        response = self.client.post(self.url, """{"products": null,
        "firstname": "1",
        "lastname": "2",
        "phonenumber": "3",
        "address": "4"}""", content_type='application/json')

        self.assertTrue(status.is_client_error(response.status_code))

    def test_products_is_empty_list(self):
        response = self.client.post(self.url, """{"products": [],
        "firstname": "1",
        "lastname": "2",
        "phonenumber": "3",
        "address": "4"}""", content_type='application/json')

        self.assertTrue(status.is_client_error(response.status_code))

    def test_products_is_missing(self):
        response = self.client.post(self.url, """{"firstname": "1",
        "lastname": "2",
        "phonenumber": "3",
        "address": "4"}""", content_type='application/json')

        self.assertTrue(status.is_client_error(response.status_code))

    def test_first_name_is_null(self):
        response = self.client.post(self.url, """{"products": [{"product": 1,
        "quantity": 1}], "firstname": null, "lastname": "2",
        "phonenumber": "3", "address": "4"}""",
                                    content_type='application/json')

        self.assertTrue(status.is_client_error(response.status_code))

    def test_no_order_keys(self):
        response = self.client.post(self.url, """{"products": [{"product": 1,
        "quantity": 1}]}""", content_type='application/json')

        self.assertTrue(status.is_client_error(response.status_code))

    def test_order_keys_null(self):
        response = self.client.post(self.url, """{"products": [{"product": 1,
        "quantity": 1}], "firstname": null, "lastname": null,
        "phonenumber": null, "address": null}""",
                                    content_type='application/json')

        self.assertTrue(status.is_client_error(response.status_code))

    def test_no_phone_number(self):
        response = self.client.post(self.url, """{"products": [{"product": 1,
        "quantity": 1}], "firstname": "Тимур", "lastname": "Иванов",
        "phonenumber": "", "address": "Москва, Новый Арбат 10"}""",
                                    content_type='application/json')

        self.assertTrue(status.is_client_error(response.status_code))

    def test_wrong_product_id(self):
        response = self.client.post(self.url, """{"products": [{"product":
        "jngrtgntg", "quantity": 1}], "firstname": "1", "lastname": "2",
        "phonenumber": "3", "address": "4"}""",
                                    content_type='application/json')

        self.assertTrue(status.is_client_error(response.status_code))

    def test_firstname_is_list(self):
        response = self.client.post(self.url, """{"products": [{"product": 1,
        "quantity": 1}], "firstname": [], "lastname": "2", "phonenumber": "3",
        "address": "4"}""",
                                    content_type='application/json')

        self.assertTrue(status.is_client_error(response.status_code))
