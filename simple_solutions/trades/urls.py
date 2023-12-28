from django.urls import path
from .views import get_checkout_session, item_detail, item_list, add_to_order

app_name  = 'trades'

urlpatterns = [
    path('buy/<int:item_id>/', get_checkout_session, name='get_checkout_session'),
    path('item/<int:item_id>/', item_detail, name='item_detail'),
    path('items/', item_list, name='item_list'),
    path('add_to_order/<int:item_id>/', add_to_order, name='add_to_order'),
]