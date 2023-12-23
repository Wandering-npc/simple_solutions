from django.shortcuts import render
from django.http import JsonResponse
import stripe
from django.conf import settings

from trades.models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY

def get_checkout_session(request, item_id):
    item = Item.objects.get(id=item_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
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
    return JsonResponse({'session_id': session.id})

def item_detail(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, 'trades/item_detail.html', {'item': item})

