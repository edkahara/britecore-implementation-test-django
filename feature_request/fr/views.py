from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from django.http import HttpResponse
from django.core import serializers
from datetime import datetime
from .models import Request, Product, Client


def home(request):
    nested_requests = {}

    for client in Client.objects.all():
        client_requests = client.request_set.order_by('priority')
        if client_requests:
            nested_requests[client] = client_requests

    context = {
        'requests': Request.objects.all(),
        'products': Product.objects.all(),
        'clients': Client.objects.all(),
        'nested_requests': nested_requests
    }

    return render(request, 'fr/index.html', context)


def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        client = request.POST["client"]
        priority = request.POST["priority"]
        product = request.POST["product"]
        targetDate = request.POST["targetDate"]

        if priority_taken_for_client_on_create(client, priority):
            reorder_priorities_for_client(client, priority)

        Request.objects.create(
            title=title,
            description=description,
            client=Client.objects.get(id=client),
            priority=priority,
            product=Product.objects.get(id=product),
            targetDate=datetime.strptime(targetDate, "%b %d, %Y").date()
        )

        return redirect('/')


def get(request, id=None):
    feature_request = serializers.serialize(
        'json', [get_object_or_404(Request, id=id)]
    )

    return HttpResponse(
        feature_request, content_type='application/json; charset=utf-8'
    )


def update(request, id=None):
    get_object_or_404(Request, id=id)
    feature_request = Request.objects.filter(id=id)

    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        client = request.POST["client"]
        priority = request.POST["priority"]
        product = request.POST["product"]
        targetDate = request.POST["targetDate"]

        if priority_taken_for_client_on_update(id, client, priority):
            reorder_priorities_for_client(client, priority)

        update_data = {
            'title': title,
            'description': description,
            'client': Client.objects.get(id=client),
            'priority': priority,
            'product': Product.objects.get(id=product),
            'targetDate': datetime.strptime(targetDate, "%b %d, %Y").date()
        }

        feature_request.update(**update_data)

        return redirect('/')


def delete(request, id=None):
    get_object_or_404(Request, id=id)

    Request.objects.filter(id=id).delete()

    return redirect('/')


def priority_taken_for_client_on_create(client, new_priority):
    similar_priority_request = Request.objects.filter(
        client=client, priority=new_priority
    ).count()
    return True if similar_priority_request else False


def priority_taken_for_client_on_update(id, client, new_priority):
    similar_priority_request = Request.objects.filter(
        client=client, priority=new_priority
    ).exclude(id=id).count()
    return True if similar_priority_request else False


def reorder_priorities_for_client(client, new_priority):
    Request.objects.filter(
        client=client, priority__gte=new_priority
    ).update(priority=F('priority')+1)
