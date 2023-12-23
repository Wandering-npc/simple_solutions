from django.urls import path
from .views import get_checkout_session, item_detail

app_name  = 'trades'

urlpatterns = [
    path('buy/<int:item_id>/', get_checkout_session, name='get_checkout_session'),
    path('item/<int:item_id>/', item_detail, name='item_detail'),
]