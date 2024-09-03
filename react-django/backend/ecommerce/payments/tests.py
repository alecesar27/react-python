import pytest # type: ignore
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .views import StripeCheckoutView

@pytest.mark.django_db
class TestStripeCheckoutView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.amount = 1000

    def test_post(self):
        response = self.client.post(reverse('stripe_checkout', args=[self.amount]))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_post_with_invalid_amount(self):
        response = self.client.post(reverse('stripe_checkout', args=[0]))
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_post_with_stripe_error(self):
        # Mock stripe error
        import stripe
        stripe.api_key = 'invalid_key'
        response = self.client.post(reverse('stripe_checkout', args=[self.amount]))
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_post_with_success_url(self):
        response = self.client.post(reverse('stripe_checkout', args=[self.amount]))
        self.assertRedirects(response, 'https://example.com/success')

    def test_post_with_cancel_url(self):
        response = self.client.post(reverse('stripe_checkout', args=[self.amount]))
        self.assertRedirects(response, 'https://example.com/cancel')
