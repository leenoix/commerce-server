from django.urls import path

from commerce.views import v1


urlpatterns = [
    path('v1/users/sign-up', v1.UserSignUpView.as_view()),
    path('v1/users/sign-in', v1.UserSignInView.as_view()),
    path('v1/users/sign-out', v1.UserSignOutView.as_view()),

    path('v1/products', v1.ProductView.as_view()),
    path('v1/cart', v1.ShoppingCartView.as_view()),
]
