from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from stripe_api.models import Item, Order
from stripe_api.serializers import ItemSerializer
from django.http import Http404
from rest_framework.views import APIView

import stripe


@api_view(['GET'])
def order_list(request) -> Response:
    order = Order.objects.filter(user=request.user).exclude(is_done=True).prefetch_related('item')[:1]
    if len(order):
        order_sum = 0
        items = Item.objects.filter(order=order)
        for order_item in items:
            order_sum += order_item.price
        return Response(order_sum)
    else:
        return Response(0)

@api_view(['GET'])
def add_to_order(request) -> Response:
    order = Order.objects.filter(user=request.user).exclude(is_done=True).prefetch_related('item')[:1]
    item_id = request.GET.get('id')
    if not len(order):
        order = Order(user=request.user)
        order.save()
    else:
        order = order[0]
    order.item.add(Item.objects.get(pk=item_id))
    order.save()
    order_sum = 0
    items = Item.objects.filter(order=order)
    for order_item in items:
        order_sum += order_item.price
    return Response(order_sum)


@api_view(['GET'])
def order_buy(request) -> Response:
    order = Order.objects.filter(user=request.user).exclude(is_done=True).prefetch_related('item')[:1]
    if not len(order):
        return Response(False)
    cost = 0
    desc = ""
    items = Item.objects.filter(order=order)
    for order_item in items:
        cost += order_item.price
        desc += order_item.description + " "
    domain = settings.SITE_URL
    stripe.api_key = settings.STRIPE_API_KEY
    order = order[0]
    response = stripe.checkout.Session.create(
        success_url="{}".format(domain),
        cancel_url="{}".format(domain),
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "order: " + str(order.id),
                        "description": desc,
                    },
                    "unit_amount": cost
                },
                "quantity": 1,
            },
        ],
        mode="payment",
    )

    order.is_done = True
    order.save()
    return Response(response['id'])


@api_view(['GET'])
def buy(request, pk: int) -> Response:
    item = Item.objects.get(pk=pk)
    domain = settings.SITE_URL
    stripe.api_key = settings.STRIPE_API_KEY
    response = stripe.checkout.Session.create(
        success_url="{}".format(domain),
        cancel_url="{}".format(domain),
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": item.name,
                        "description": item.description,
                    },
                    "unit_amount": item.price
                },
                "quantity": 1,
            },
        ],
        mode="payment",
    )

    return Response(response['id'])


class ItemDetail(APIView):
    def get_object(self, pk) -> Item:
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)




