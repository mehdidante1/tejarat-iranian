from .models import *
from django.shortcuts import render
from .forms import CouponsApplyForm


def cart_list(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total=0
    form = CouponsApplyForm(request.POST)
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity
    #return HttpResponse(str(total))
    context={'shopcart': shopcart,
             'total': total,
             'form' : form,
             }
    return context
