from unicodedata import category, name
from urllib import request
from django.http import JsonResponse , HttpResponseRedirect
from django.shortcuts import redirect, render , get_object_or_404
from requests import session
from .models import *
from .models import NotifUserStatus
from django.db.models import Max,Min,Count,Avg
from django.template.loader import render_to_string
from .forms import SignupForm , ReviewAdd , AddressBookForm , ProfileForm , SearchForm , CouponsApplyForm  , AddComment , CommentBlogForm
from django.contrib.auth import authenticate , login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models.functions import ExtractMonth
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage
from django.utils import timezone 
#paypal
from django.http import HttpResponse
import json
from django.contrib import messages
from taggit.models import Tag
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required

#from zeep import Client
# Create your views here.


def home(request ):
    t= "buty"
    product = Product.objects.filter(is_featured = True , category__slug = t).order_by('-id')
    category = Category.objects.all()
    brand = Brand.objects.all().order_by('-id')
    blog = Blog.objects.all().order_by('-id')
    return render(request , 'home-1.html' , {"cat": category , "product" : product , "brand" : brand  , 'blog' : blog})
  


def product_list_tags(request , tag_slug= None):
    product = Product.objects.filter(is_featured = True).order_by('-id')
    if tag_slug:
        tag = get_object_or_404(Tag , slug = tag_slug)
        product = product.filter(tags__in = [tag])
    return render(request , 'product_list_tag.html' , {'product_tag' : product})

def product_list_category(request , category_slug= None):
    product = Product.objects.all().order_by('-id')
    if category_slug:
        category = get_object_or_404(Category , slug = category_slug)
        product = product.filter(category__in = [category])
    return render(request , 'product_list_category.html' , {'product_category' : product})


def product_list(request):
    total_data = Product.objects.count()
    data = Product.objects.all().order_by('-id')
    category_product = Category.objects.all()
    min_price=ProductAttribute.objects.aggregate(Min('price'))
    max_price = ProductAttribute.objects.aggregate(Max('price'))
    return render(request , 'product_list.html', {"data" : data , "min_price" : min_price , "max_price" : max_price , "total_data" : total_data , 'cat' : category_product})
  
def category_products(request , id , slug):
    products = Product.objects.filter(category_id = id)
    category = Category.objects.all()
    context ={
        'products' : products,
        'category' : category

    }
    return render(request , 'product_category.html' , context)

def brand_product_list(request , brand_id):
    brand = Category.objects.get(id = brand_id)
    data = Product.objects.filter(category = brand).order_by('-id')
    return render(request , 'brand_product_list.html' , {"data" : data})


def product_detail(request , slug , id):
    query = request.GET.get('q')
    brand = Brand.objects.all().order_by('-id')
    category = Category.objects.all()
    product = Product.objects.get(id = id)
    images= Images.objects.filter(product_id = id)
    comment = Comment.objects.filter(product = product).order_by('-id')
    reviewForm =  ReviewAdd()
    commentForm = AddComment()
    
    # Product similar محصولات مشابه
    product_tags_ids = product.tags.values_list('id' , flat=True)
    similar_products = Product.objects.filter(tags__in = product_tags_ids).exclude(id = product.id)
    similar_products = similar_products.annotate(same_tags = Count('tags')).order_by('-same_tags')
    # محصولات مشابه

    if product.variant !="None": # Product have variants
        if request.method == 'POST': #if we select color
            variant_id = request.POST.get('variantid')
            variant = ProductAttribute.objects.get(id=variant_id) #selected product by click color radio
            colors = ProductAttribute.objects.filter(product_id=id )
            #sizes = ProductAttribute.objects.raw('SELECT * FROM  main_productattribute  WHERE product_id=%s GROUP BY size_id',[id])
            query += variant.title+' Color:' +str(variant.color)
        else:
            variants = ProductAttribute.objects.filter(product_id=id)
            colors = ProductAttribute.objects.filter(product_id=id )
            
            variant =ProductAttribute.objects.get(id=variants[0].id)
        
    #Check
    canAdd = True
    if request.user.is_authenticated:
        reviewCheck = ProductReview.objects.filter(user = request.user , product = product).count()
    if request.user.is_authenticated:
        if reviewCheck > 0:
            canAdd = False
    # fetch
    reviews = ProductReview.objects.filter(product = product)

    #fetch average product 
    avg_reviews = ProductReview.objects.filter(product = product).aggregate(avg_rating=Avg('review_rating'))

    #Check Comment
    canAdd2 = True
    commentCheck = Comment.objects.filter(product = product).count()
    if commentCheck > 0:
        canAdd2 = False


    context ={'data' : product , 'images' : images , 'colors': colors,  
                        'variant': variant,'query': query , 'form' : reviewForm , 'comment_form' : commentForm , 'canAdd' : canAdd , 'canAdd2'  : canAdd2 ,'reviews' : reviews , 'avg_reviews' : avg_reviews,
                        'similar_products' : similar_products , 'comment' : comment ,  "brand" : brand , 'cat' : category,
                        }

    return render(request , 'product_detail.html' , context)

def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'POST':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = ProductAttribute.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('ajax/color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


def search(request):
    brand = Brand.objects.all().order_by('-id')
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            catid = form.cleaned_data['catid']
            if catid==0:
                products=Product.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query,brand_id=catid)
            context = {'products': products, 'query':query, 'brand' : brand
                        }
            return render(request, 'search.html', context)

    return HttpResponseRedirect('/')

def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title +" > " + rs.category.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def filter_data(request):
    colors = request.GET.getlist('color[]')
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    sizes = request.GET.getlist('size[]')
    minPrice=request.GET['minPrice']
    maxPrice=request.GET['maxPrice']
    allProducts = Product.objects.all().distinct()
    allProducts=allProducts.filter(productattribute__price__gte=minPrice)
    allProducts=allProducts.filter(productattribute__price__lte=maxPrice)
    if len (colors)>0:
        allProducts = allProducts.filter(productattribute__color__id__in = colors)
    if len (categories)>0:
        allProducts = allProducts.filter(category__id__in = categories)
    if len (brands)>0:
        allProducts = allProducts.filter(brand__id__in = brands)

    if len (sizes)>0:
        allProducts = allProducts.filter(productattribute__size__id__in = sizes)
    t= render_to_string('ajax/product-list.html' , {'data' : allProducts})
    return JsonResponse({'data' : t})


def load_more_data(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    data = Product.objects.all().order_by('-id')[offset:offset+limit]
    t= render_to_string('ajax/product-list.html' , {'data' : data})
    return JsonResponse({'data' : t})


# add to cart


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
             'cat':category,
             'total': total,
             'form' : form,
             }
    return render(request,'cart.html',context)



def update_cart_item(request):
    shopcart = ShopCart.objects.filter(user_id=request.user)
    total=0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(ShopCart.objects.filter(user = request.user , product_id = prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cart = ShopCart.objects.get(product_id = prod_id , user = request.user)
            cart.quantity = prod_qty
            cart.save()
            return redirect('/')        
    t=render_to_string('ajax/cart-list.html' , {'shopcart' : shopcart ,'total' : total})
    return JsonResponse({ 'data' : t , 'status' : "محصول بروز شد"})       
    
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            user = authenticate(username = username , password = pwd)
            reg = UserAddressBook(user=user )
            reg.save()
            login(request , user)
            return redirect('home')
        else:
            print(form)
            print("Invalid Form")
            print(form.errors)
            return render(request, 'signup.html',{'form':form})
    form = SignupForm
    return render(request , 'signup.html' , {'form' : form})




@login_required
def order_product(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity


    form_coupon = CouponsApplyForm(request.POST)
    if shopcart.exists():
        if form_coupon.is_valid():
            now = timezone.now() 
            code = form_coupon.cleaned_data['code']
            try:
                coupon_obj = Coupon.objects.get(code__iexact = code , valid_from__lte = now , valid_to__gte = now , active=True)
                if coupon_obj.valid_to >= now:
                    get_discount = (coupon_obj.discount / int(100)) * int(total)
                    total_price_after_discount = int(total) - int(get_discount)
                    request.session['discount_total'] = total_price_after_discount
                    request.session['coupon_code'] = code
                    messages.success(request, 'کد تخفیف اعمال شد.')
                    return redirect('order_product')
                else:
                    coupon_obj.active = False
                    coupon_obj.save()
            except:
                messages.error(request, 'کد تخفیف وارد شده اعتبار ندارد')
                return redirect('order_product')
        
            
        total_price_after_discount = request.session.get('discount_total')
        coupon_code = request.session.get('coupon_code')
    


    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        #return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............

            data = Order()
            data.first_name = form.cleaned_data['first_name'] #get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.postal_code = form.cleaned_data['postal_code']
            data.city = form.cleaned_data['city']
            data.country = form.cleaned_data['country']
            data.tag = form.cleaned_data['tag']
            data.vahed = form.cleaned_data['vahed']
            data.phone_2 = form.cleaned_data['phone_2']
            data.address = form.cleaned_data['address']
            data.user_id = current_user.id
            if total_price_after_discount:
                data.total = total_price_after_discount
            else:
                data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode= get_random_string(5).upper() # random cod
            data.code =  ordercode
            data.save() #
            request.session['discount_total'] = 0   

            shopcart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id     = data.id # Order Id
                detail.product_id   = rs.product_id
                detail.user_id      = current_user.id
                detail.quantity     = rs.quantity
                if rs.product.variant == 'None':
                    detail.price    = rs.product.price
                else:
                    detail.price = rs.variant.price
                detail.variant_id   = rs.variant_id
                detail.amount        = rs.amount
                detail.save()
                #order_product.delay(data.id)
                request.session['order_id'] = data.id
                return redirect(reverse('zarinpal:request'))
                
                #************ <> *****************

            ShopCart.objects.filter(user_id=current_user.id).delete() # Clear & Delete shopcart
            request.session['cart_items']=0
            messages.success(request, "سفارش شما با موفقیت انجام شد. با تشکر از خرید شما")
            return render(request, 'order-complete.html',{'ordercode':ordercode,'category': category , 'total' : total })
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/")
    

    form= OrderForm()
    profile = UserAddressBook.objects.get(user_id=current_user , status=True)
    
    try:
        context = {'shopcart': shopcart,
               'cat': category,
               'total': total,
               'form': form,
               'profile' : profile,
               'total_price_after_discount' : total_price_after_discount,
               'coupon_code': coupon_code
               }
    
    except:
        return redirect('/')
    
    
    return render(request, 'checkout.html', context )
 

def save_review(request , pid):
    product = Product.objects.get(pk=pid)
    user = request.user
    review = ProductReview.objects.create(
        user = user,
        product = product , 
        review_text = request.POST['review_text'],
        review_rating = request.POST['review_rating'],
        recommend = request.POST['recommend'],
    )
    data ={
        'user' : user.username,
        'review_text':request.POST['review_text'],
        'review_rating' : request.POST['review_rating'],
        'recommend' : request.POST['recommend'],
    }

        #fetch average product 
    avg_reviews = ProductReview.objects.filter(product = product).aggregate(avg_rating=Avg('review_rating'))
    return JsonResponse({'bool': True , 'data' : data , 'avg_reviews' : avg_reviews})

import calendar
@login_required
def my_dashboard (request):
    category = Category.objects.all()
    data = User.objects.get(id = request.user.id)
    orders = OrderProduct.objects.annotate(month = ExtractMonth('create_at')).values('month').annotate(count = Count('id')).values('month' , 'count')
    monthNumber =[]
    totalOrders = []
    for d in orders :
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])
    return render(request , 'dashboard.html' , {'monthNumber' : monthNumber , 'data' : data , 'totalOrders' : totalOrders , 'cat' : category})


@login_required
def my_orders (request):
    data = User.objects.get(id = request.user.id)
    category = Category.objects.all()
    orders = Order.objects.filter(user = request.user).order_by('-id')
    return render(request , 'my_orders.html' , {'orders' : orders , 'cat' : category , 'data' : data})



def my_order_items(request,id):
	order=Order.objects.get(pk=id)
	orderitems=OrderProduct.objects.filter(order=order).order_by('-id')
	return render(request, 'order-items.html',{'orderitems':orderitems})


def add_wishlist(request):
    pid = request.GET['product']
    product = Product.objects.get(pk = pid)
    data = {}
    checkw = Wishlist.objects.filter(product = product , user = request.user).count()
    if checkw > 0:
        data = {
            'bool' : False
        }
    else:
        wishlist = Wishlist.objects.create(
        product = product,
        user = request.user,
        )
        data = {
            'bool' : True
        }
    return JsonResponse(data)


def wishlist(request):
    category = Category.objects.all()
    wlist = Wishlist.objects.filter(user = request.user).order_by('-id')
    return render(request , 'wishlist.html' , {'wlist' : wlist , 'cat' : category})


def my_review(request):
    category = Category.objects.all()
    reviews = ProductReview.objects.filter(user = request.user).order_by('-id')
    return render(request , 'reviews.html' , {'reviews' : reviews , 'cat' : category})


def my_address(request):
    category = Category.objects.all()
    addbook = UserAddressBook.objects.filter(user = request.user).order_by('-id')
    return render(request , 'my-address.html' , {'addbook' : addbook , 'cat' : category})

def save_address (request):

    category = Category.objects.all()
    msg =None
    if request.method == 'POST':
        form = AddressBookForm(request.POST)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            if 'status' in request.POST:
                UserAddressBook.objects.update(status=False)
            saveForm.save()
            msg='آدرس مورد نظر با موفقیت ایجاد شد'
    form = AddressBookForm
    return render(request , 'add-address.html' , {'form' : form , 'msg' : msg , 'cat' : category}) 


# add address
def activate_address(request):
	a_id=str(request.GET['id'])
	UserAddressBook.objects.update(status=False)
	UserAddressBook.objects.filter(id=a_id).update(status=True)
	return JsonResponse({'bool':True})

def Edit_Profile (request):
    data = User.objects.get(id = request.user.id)
    categoey = Category.objects.all()
    msg =None
    if request.method == 'POST':
        form = ProfileForm(request.POST , instance = request.user)
        if form.is_valid():
            form.save()
            msg='تغیرات با موفقیت ثبت شد.'
        else:
            print(form)
            print("Invalid Form")
            print(form.errors)
            return render(request, 'edit-profile.html',{'form':form})
    form = ProfileForm(instance = request.user)
    return render(request , 'edit-profile.html' , {'form' : form , 'msg' : msg , 'cat' : categoey , 'data' : data}) 



def update_address (request , id):
    category = Category.objects.all()
    address = UserAddressBook.objects.get(pk = id)
    msg =None
    addbook = UserAddressBook.objects.get(id = id)
    if request.method == 'POST':
        form = AddressBookForm(request.POST , instance = address)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            if 'status' in request.POST:
                UserAddressBook.objects.update(status=False)
            saveForm.save()
            msg='آدرس مورد نظر با موفقیت ایجاد شد'
    form = AddressBookForm(instance = address)
    return render(request , 'update-address.html' , {'form' : form , ' cat' : category , 'msg' : msg , 'addbook' : addbook}) 



def addtoshopcart(request , id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    checkproduct = ShopCart.objects.filter(product_id = id)
    product= Product.objects.get(pk=id)

    if checkproduct:
        control = 1 # The product is in the cart   
    else:
        control = 0 # The product is not in the cart"""

    if product.variant != 'None':
        variantid = request.POST.get('variantid')  # from variant add to cart
        checkinvariant = ShopCart.objects.filter(variant_id=variantid, user_id=current_user.id)  # Check product in shopcart
        if checkinvariant:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""
    else:
        checkinproduct = ShopCart.objects.filter(product_id=id, user_id=current_user.id) # Check product in shopcart
        if checkinproduct:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""


    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control==1: # Update  shopcart
                if product.variant == 'None':
                    data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
                else:
                    data = ShopCart.objects.get(product_id=id, variant_id=variantid, user_id=current_user.id)
                data.quantity = form.cleaned_data['quantity']
                data.save()  # save data
            else : # Inser to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id =id
                data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "محصول با موفقیت به سبد خرید اضافه شد.")
        return HttpResponseRedirect(url)

    else: # if there is no post
        if control == 1:  # Update  shopcart
            data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()  #
        else:  #  Inser to Shopcart
            data = ShopCart()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.variant_id =None
            data.save()  #
        messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect(url)




def notifs(request):
    category = Category.objects.all()
    data = Notify.objects.all().order_by('-id')
    return render(request , 'notfications.html' , {'data' : data , 'cat' : category})



def get_notifs(request):
	data=Notify.objects.all().order_by('-id')
	notifStatus=False
	jsonData=[]
	totalUnread=0
	for d in data:
		try:
			notifStatusData=NotifUserStatus.objects.get(user=request.user,notif=d)
			if notifStatusData:
				notifStatus=True
		except NotifUserStatus.DoesNotExist:
			notifStatus=False
		if not notifStatus:
			totalUnread=totalUnread+1
		jsonData.append({
				'pk':d.id,
				'notify_detail':d.notify_detail,
				'notifStatus':notifStatus
			})
	# jsonData=serializers.serialize('json', data)
	return JsonResponse({'data':jsonData,'totalUnread':totalUnread})


def mark_read_notif(request):
    notif = request.GET['notif']
    notif = Notify.objects.get(pk = notif)
    user = request.user
    NotifUserStatus.objects.create(notif= notif , user = user , status=True)
    return JsonResponse({'bool' : True })




def link(request , id):
    user = request.user
    link = get_object_or_404(ProductReview , id = id)
    return JsonResponse({
        'likes' : link.likes.count(),
        'dislikes' : link.dislikes.count(),
        'status' : user.is_authenticated,
    })

def like (request , id ):
    url = request.META.get('HTTP_REFERER')
    user = request.user
    link = ProductReview.objects.get( id = id)
    #product = get_object_or_404(Product, id=id)
    if user in link.dislikes.all():
        link.dislikes.remove(user)
        link.likes.add(user)
    elif user in link.likes.all():
        link.likes.remove(user)
    else:
        link.likes.add(user)
    return HttpResponseRedirect(url)

def dislike (request , id):
    url = request.META.get('HTTP_REFERER')
    user = request.user
    link = get_object_or_404(ProductReview , id = id)
    if user in link.likes.all():
        link.likes.remove(user)
        link.dislikes.add(user)
    elif user in link .dislikes.all():
        link.dislikes.remove(user)
    else:
        link.dislikes.add(user)
    return HttpResponseRedirect(url)


def update_cart (request , id):
    form = ShopCartForm(request.POST)
    current_user = request.user
    if request.method == 'POST':
        if form.is_valid():
            data = ShopCart.objects.get(id=id, user_id=current_user.id)
            data.quantity = form.cleaned_data['quantity']
            data.save() 
    return HttpResponseRedirect('/cart')



def deletereview(request,id):
    ProductReview.objects.filter(id=id).delete()	
    return HttpResponseRedirect('/my-review')




def forgotpass(request):
    context = {}
    if request.method=="POST":
        un = request.POST["username"]
        pwd = request.POST["npass"]

        user = get_object_or_404(User,username=un)
        user.set_password(pwd)
        user.save()

        login(request,user)
        if user.is_superuser:
            return HttpResponseRedirect("/")
        else:
          context["status"] = "کلمه عبور با موفقیت تغیر کرد.!!!"

    return render(request,'forget_password.html',context)



import random
def reset_password(request):
    un = request.GET["username"]
    try:
        user = get_object_or_404(User,username=un)
        otp = random.randint(1000,9999)
        msz = "عزیز {} \n{} از طرق این کد کلمه عبور خود را تغیر دهید \nلطفا این کد چهار رقمی را برای کسی به اشتراک نگذارید. \nبا تکر \nکالا مارکت".format(user.username, otp)
        try:
            email = EmailMessage("Account Verification",msz,to=[user.email])
            email.send()
            return JsonResponse({"status":"sent","email":user.email,"rotp":otp})
        except:
            return JsonResponse({"status":"error","email":user.email})
    except:
        return JsonResponse({"status":"failed"})



# update $ delete in Shop cart
def save_all(request,form , template_name):
    shopcart = ShopCart.objects.filter(user_id=request.user.id)
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity
    data= dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = ShopCart.objects.filter(user_id = request.user.id)
            data['book_list'] = render_to_string('cart_list_2.html',{'shopcart':books , 'total' : total})
        else:
            data['form_is_valid'] = False
    context = {
        'form' : form,
        'total' : total,
        'item' : shopcart,
        'status' : "سبد خرید پاک شد"
    }
    data['html_form'] = render_to_string(template_name,context,request=request)
    return JsonResponse(data)
          






def book_update(request , id):
    shopcart = ShopCart.objects.filter(user_id=request.user.id)
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity
    book = get_object_or_404(ShopCart , id =id , user_id = request.user.id)
    if request.method == 'POST':
        form = ShopCartForm(request.POST , instance = book)
    else:
        form = ShopCartForm(instance = book)
    return save_all(request,form,'book_update.html' )


def notfound (request ):
    return render(request , '404.html')



def book_delete(request,id):
    shopcart = ShopCart.objects.filter(user_id=request.user.id)
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity
    data = dict()
    book = get_object_or_404(ShopCart,id=id)
    if request.method =='POST':
        book.delete()
        data['form_is_valid'] = True
        books = ShopCart.objects.filter(user_id = request.user.id)
        data['book_list'] = render_to_string('cart_list_2.html' , {'shopcart' : books , 'total' : total})
    else:
        context = {'item' : book , 'total' : total , 'status' : "سبد خرید پاک شد"}
        data['html_form'] = render_to_string('book_delete.html' , context , request=request)
    return JsonResponse(data)


def wishlist_delete(request,id):
    data = dict()
    book = get_object_or_404(Wishlist,id=id)
    if request.method =='POST':
        book.delete()
        data['form_is_valid'] = True
        books = Wishlist.objects.filter(user_id = request.user.id)
        data['book_list'] = render_to_string('wish_list_2.html' , {'wlist' : books})
    else:
        context = {'item' : book}
        data['html_form'] = render_to_string('wishlist_delete.html' , context , request=request)
    return JsonResponse(data)


def book2_delete(request,id):
    shopcart = ShopCart.objects.filter(user_id=request.user.id)
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity
    data = dict()
    book = get_object_or_404(ShopCart,id=id)
    if request.method =='POST':
        book.delete()
        data['form_is_valid'] = True
        books = ShopCart.objects.filter(user_id = request.user.id)
        data['book_list'] = render_to_string('cart_list_home.html' , {'shopcart' : books , 'total' : total})
    else:
        context = {'item' : book , 'total' : total}
        data['html_form'] = render_to_string('delete_cart_home.html' , context , request=request)
    return JsonResponse(data)


def blog_list (request):
    category = Category.objects.all()
    blog_list = Blog.objects.all().order_by('-id')
    return render(request , 'blog_list.html' , {'blog_list' : blog_list , 'cat' : category})



def blog_details (request , id):
    category = Category.objects.all()
    url = request.META.get('HTTP_REFERER')
    blog = get_object_or_404(Blog, id=id)
    blog_item = Blog.objects.all().order_by('-id')
    comments = CommentBlog.objects.filter(blog = blog , reply = None).order_by('-id')
    if request.method == 'POST':
        Comment_blog_form = CommentBlogForm(request.POST or None)
        if Comment_blog_form.is_valid():
            name = request.POST.get('name')
            title = request.POST.get('title')
            text = request.POST.get('text')
            reply_id = request.POST.get('comment_blog_id')
            comment_qs = None
            if reply_id:
                comment_qs = CommentBlog.objects.get(id = reply_id)
            comment_blog = CommentBlog.objects.create(blog = blog , name = name , title = title , text = text , reply = comment_qs)
            comment_blog.save()
            return HttpResponseRedirect(url)
    else:
        Comment_blog_form = CommentBlogForm()

    
    return render(request , 'blog_details.html' , {'blog' : blog , 'blog_item' : blog_item , 'comments' : comments , 'form' : Comment_blog_form , 'cat' : category})


def save_comment(request , pid):
    product = Product.objects.get(pk=pid)
    comment = Comment.objects.create(
        product = product ,
        name = request.POST['name'],
        family = request.POST['family'],
        email = request.POST['email'],
        text_comment = request.POST['text_comment'],
    )
    data ={
        'name':request.POST['name'],
        'family':request.POST['family'],
        'email':request.POST['email'],
        'text_comment':request.POST['text_comment'],
    }
    return JsonResponse({'bool': True , 'data' : data })


def contact_us (request):

    if request.method == 'POST' :
        subject = request.POST['subject']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        text_message = request.POST['text_message']

        Contact_Us.objects.create(
            subject = subject , 
            name = name , 
            email = email ,
            phone = phone ,
            text_message = text_message ,

        )
        messages.success(request, "درخواست شما با موفقیت ارسال شد.")
        return redirect('tamas')
        
   
    return render(request , 'contact-us.html')

  