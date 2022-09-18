from unicodedata import name
from django.http import JsonResponse , HttpResponseRedirect
from django.shortcuts import redirect, render , get_object_or_404
from requests import session
from .models import *
from .models import NotifUserStatus
from .forms import SignupForm , ReviewAdd , AddressBookForm , ProfileForm , SearchForm , CouponsApplyForm  , AddComment , CommentBlogForm

def search(request):
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            catid = form.cleaned_data['catid']
            if catid==0:
                products=Product.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query,brand_id=catid)
            context = {'products': products, 'query':query,
                        }
            return render(request, 'search.html', context)

    return HttpResponseRedirect('/')