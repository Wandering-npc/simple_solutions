from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
import stripe
from django.conf import settings

from trades.models import Item, Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY

def get_checkout_session(request, item_id):
    """
    Получение сеанса оформления заказа для товара.

    :param request: объект запроса Django
    :param item_id: идентификатор товара
    :return: JsonResponse с идентификатором сеанса и настройками Stripe
    """
    item = Item.objects.get(id=item_id)

    # Определение настроек Stripe в зависимости от валюты товара
    if request.method == 'GET':
        if item.currency == 'EUR':
            stripe_config = {'publicKey': settings.STRIPE_PUBLIC_KEY_EURO}
        elif item.currency == 'USD':
            stripe_config = {'publicKey': settings.STRIPE_PUBLIC_KEY_USD}

    # Создание сеанса оформления заказа с использованием Stripe API
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(f'/success?session_id={{CHECKOUT_SESSION_ID}}'),
        cancel_url=request.build_absolute_uri(f'/cancel'),
    )

    return JsonResponse({'session_id': session.id,
                         'stripe_config': stripe_config})

def item_detail(request, item_id):
    """
    Отображение подробной информации о товаре.

    :param request: объект запроса Django
    :param item_id: идентификатор товара
    :return: объект ответа Django с информацией о товаре
    """
    item = Item.objects.get(id=item_id)
    return render(request, 'trades/item_detail.html', {'item': item})

def item_list(request):
    """
    Отображение списка товаров.

    :param request: объект запроса Django
    :return: объект ответа Django с списком товаров
    """
    items = Item.objects.all()
    return render(request, 'trades/item_list.html', {'items': items})

def add_to_order(request, item_id):
    """
    Добавление товара в корзину заказа пользователя.

    :param request: объект запроса Django
    :param item_id: идентификатор товара
    :return: перенаправление на страницу списка товаров
    """
    item = get_object_or_404(Item, id=item_id)    
    # Получение или создание заказа пользователя
    order, created = Order.objects.get_or_create(customer=request.user, is_paid=False) 
    # Получение или создание элемента заказа для выбранного товара
    order_item, created = OrderItem.objects.get_or_create(order=order, item=item)
    order_item.quantity += 1
    order_item.save()
    return redirect('trades:item_list')

