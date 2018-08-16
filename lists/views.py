from django.shortcuts import render, redirect
from django.http import HttpResponse

from lists.models import Item, List


# Create your views here.
def home_page(request):
    return render(request, 'lists/home.html')

def view_list(request):
    return render(request, 'lists/list.html', {'items': Item.objects.all()})

# Should only ever get called for a POST request to make a new list item
def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text = request.POST['item_text'], list = list_)
    return redirect('/lists/the-only-list-in-the-world/')
