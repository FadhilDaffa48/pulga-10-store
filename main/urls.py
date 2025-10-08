from django.urls import path
from main import views

app_name = "main"

urlpatterns = [
    path('', views.display, name='display'),
    path('product/<uuid:id>/', views.product_detail, name='product_detail'),
    path('product/buy/<uuid:id>/', views.buy_product, name='buy'),
    path('edit/<uuid:id>/', views.edit_product, name='edit_product'),
    path('add-ajax/', views.add_news_entry_ajax, name='add_product_ajax'),
    path('delete/<uuid:id>/', views.delete_product, name='delete_product'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('add/', views.add_product, name='add_product'),
    path('show_xml/', views.show_xml, name='show_xml'),
    path('show_json/', views.show_json, name='show_json'),
    path('xml/<uuid:id>/', views.xml_by_id, name='xml_by_id'),
    path('json/<uuid:id>/', views.json_by_id, name='json_by_id'),
    ]