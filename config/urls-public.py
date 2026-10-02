from django.urls import path, include
from apps.frontend import views

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("", views.landing, name="landing"),
    path("pricing/", views.pricing, name="pricing"),
    path("login/", views.login, name="login"),
    path("demo/", views.menu, name="menu"),
    path("demo/cart/", views.cart, name="cart"),
    path("demo/checkout/", views.checkout, name="checkout"),
    path("demo/invoice/", views.invoice, name="invoice"),
    path("preview/vendor/", views.dashboard, name="dashboard"),
    path("preview/vendor/menu/", views.manage, name="menu_manage"),
    path("preview/vendor/qr/", views.qr, name="qr_codes"),
]