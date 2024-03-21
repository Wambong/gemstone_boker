from django.urls import path
from . import views
from .views import update_order_status

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_variation/', views.add_variation, name='add_variation'),
    path('add_product_gallery/', views.add_product_gallery, name='add_product_gallery'),
    path('inventory/', views.inventory, name ="inventory"),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('update_status_to_pending/', views.update_status_to_pending, name='update_status_to_pending'),
    path('all_payment_request/', views.all_payment_request, name='all_payment_request'),
    path("make_payment/", views.make_payment, name = "make_payment"),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('update_order_status/<int:order_id>/', update_order_status, name='update_order_status'),


]
