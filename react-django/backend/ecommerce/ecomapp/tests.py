import pytest # type: ignore
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .views import getRoutes, ProductView, OrderView, AddressView, MyTokenObtainPairView, getUserProfiles, getUsers, registerUser, ActivateAccountView
from .models import Products, Orders, Address, User
from .serializer import ProductsSerializer, OrdersSerializer, AddressSerializer, UserSerializer

@pytest.mark.django_db
class TestViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', 'testuser@example.com', 'password123')
        self.product = Products.objects.create(name='Test Product', price=10.99)
        self.order = Orders.objects.create(id_prod=self.product, quantity=2)
        self.address = Address.objects.create(user=self.user, street='123 Main St', city='Anytown', state='CA', zip_code='12345')

    def test_get_routes(self):
        response = self.client.get(reverse('get_routes'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_products(self):
        response = self.client.get(reverse('get_products'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product(self):
        response = self.client.get(reverse('get_product', args=[self.product._id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product(self):
        data = {'name': 'Updated Product', 'price': 9.99}
        response = self.client.put(reverse('update_product', args=[self.product._id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        data = {'id_prod': self.product._id, 'quantity': 2}
        response = self.client.post(reverse('create_order'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_orders(self):
        response = self.client.get(reverse('get_orders'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_order_product(self):
        response = self.client.get(reverse('get_order_product', args=[self.product._id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_address(self):
        data = {'user': self.user._id, 'street': '123 Main St', 'city': 'Anytown', 'state': 'CA', 'zip_code': '12345'}
        response = self.client.post(reverse('create_address', args=[self.user._id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_address(self):
        response = self.client.get(reverse('get_address', args=[self.user._id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_my_token_obtain_pair_view(self):
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(reverse('my_token_obtain_pair'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_profiles(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('get_user_profiles'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('get_users'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_user(self):
        data = {'fname': 'Test', 'lname': 'User', 'email': 'testuser@example.com', 'password': 'password123'}
        response = self.client.post(reverse('register_user'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activate_account_view(self):
        response = self.client.get(reverse('activate_account', args=['uidb64', 'token']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)