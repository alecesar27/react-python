from django.shortcuts import render,redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


import stripe
# This is your test secret API key.
stripe.api_key= settings.STRIPE_SECRET_KEY


class StripeCheckoutView(APIView):
        
    def post(self,request,amount):
   
        try:
            session = stripe.checkout.Session.create(
                line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                    'name': 'Payment of products',
                    },
                    'unit_amount': amount,
                },
                'quantity': 100,
                }],
                mode='payment',
                success_url=settings.SITE_URL + '?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '?canceled=true',
            )

            return redirect(session.url)
        except:
            return Response(
                {'error': 'Something went wrong when creating stripe checkout session'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )      
    
    # def post(self,request):

    #     try:
    #         checkout_session = stripe.checkout.Session.create(                
    #             line_items=[
    #                 {
    #                     'price': 'price_1PkR12RsM8v1MNAoTAtYKFLT', 
    #                     'quantity': 1,
    #                 },
    #             ],
    #             payment_method_types=['card',],
    #             mode='payment',
    #             success_url= settings.SITE_URL + '?success=true&session_id={CHECKOUT_SESSION_ID}',
    #             cancel_url = settings.SITE_URL + '?canceled=true',
    #         )
    #         return redirect(checkout_session.url)
    #     except:
    #         return Response(
    #             {'error': 'Something went wrong when creating stripe checkout session'},
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR
    #         )

