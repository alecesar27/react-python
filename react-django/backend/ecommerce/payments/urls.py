from django.urls import path
from .views import StripeCheckoutView


urlpatterns=[

   # path('create-checkout-session', StripeCheckoutView.as_view()),
    path('create_payment_intent<amount>',   StripeCheckoutView.as_view())
]