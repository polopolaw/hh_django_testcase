from django.shortcuts import render
from stripe_api.models import Item
from stripe_api.serializers import ItemSerializer
import json


def index(request):
    items = Item.objects.all()
    context = {"items": json.dumps(ItemSerializer(items, many=True).data)}
    return render(
        request=request,
        template_name="index.html",
        context=context
    )
