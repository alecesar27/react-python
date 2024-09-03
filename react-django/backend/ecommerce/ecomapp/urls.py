from . import views
from django.urls import path
from rest_framework_simplejwt.views import ( # type: ignore
    TokenObtainPairView
)

urlpatterns = [
    path('', views.getRoutes,name="getRoutes"),
    path('products/',views.ProductView.getProducts,name="getProducts"),
    path('product/<str:pk>',views.ProductView.getProduct,name="getProduct"),
    path('product/update/<str:pk>',views.ProductView.updateProduct,name="updateProduct"),
    path('products/update/',views.ProductView.updateProduct,name="updateProducts"),
    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/profile/',views.getUserProfiles,name="getUserProfiles"),
    path('users/',views.getUsers,name="getUsers"),
    path('users/register/',views.registerUser,name="register"),
    path('orders/',views.OrderView.getOrders,name="getOrders"),
    path('orderProduct/<str:id>',views.OrderView.getOrderProduct,name="getOrderProduct"),
    path('orders/update/<str:pk>',views.OrderView.updateOrder,name="updateOrder"),
    path('order/create/',views.OrderView.createOrder,name="createOrder"),
    path('openedOrderClient/<str:id>',views.OrderView.openedOrderClient,name="openedOrderClient"),
    path('address/<str:id>',views.AddressView.createAddress,name="createAddress"),
    path('clientAddress/<str:id>',views.AddressView.clientAddress,name="clientAddress"),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),

]
