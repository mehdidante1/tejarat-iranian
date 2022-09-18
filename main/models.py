from distutils.command.upload import upload
import email
from msilib.schema import Class
from pyexpat import model
from turtle import color
from django.urls import reverse
from django import forms
from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from extensions.utils import jalali_converter
from django.forms import ModelForm
from mptt.fields import TreeForeignKey
from django.core.validators import MinValueValidator , MaxValueValidator
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
# Create your models here. 

class Banner(models.Model):
    img=models.ImageField(upload_to="banner_imgs/")
    alt_text=models.CharField(max_length=300)

    class Meta:
        verbose_name_plural='بنر محصولات'

    def __str__(self):
        return self.alt_text
#category
class Category(models.Model):
    parent = models.ForeignKey('self' , default=None , null = True , blank = True , on_delete=models.CASCADE , related_name="children" , verbose_name="زیر دست")
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=True, unique=True)
    image = models.ImageField(upload_to = "cat_imgs/")
    position = models.IntegerField(_("پوزیشن")  , null=True , blank = True)
    status = models.BooleanField(_("آیا نمایش داده شود؟") , null=True, blank=True)

    def image_tag(self):
        return mark_safe('<img src="%s" width="60" height ="60" />' % (self.image.url))

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = "دسته بندی ها"
        ordering = ['parent__id']

#barnd
class Brand(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to = "brand_imgs/")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = "برند"



#color
class Color(models.Model):
    title = models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)


    def color_bg(self):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.color_code))

    def __str__(self):
       return self.title

    def color_tag(self):
        if self.color_code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.color_code))
        else:
            return ""
    class Meta:
        verbose_name = 'رنگ بندی'
        verbose_name_plural = "رنگ بندی "


# Product Model
class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),

    )
    title=models.CharField(max_length=200 , verbose_name="عنوان محصول")
    slug = models.SlugField(unique=True , verbose_name="آدرس محصول")
    keywords = models.CharField(max_length=255, verbose_name="کلمات کلیدی")
    detail=RichTextField(verbose_name="جزییات محصول")
    image=models.ImageField(upload_to='product_imgs/' , verbose_name="عکس")
    specs=RichTextField(verbose_name="مشخصات")
    price = models.IntegerField(default=0, verbose_name="قیمت")
    discount_price = models.IntegerField(default = 0, verbose_name="قیمت با تخفیف")
    amount=models.IntegerField(default=0 , verbose_name="موجودی محصول")
    minamount=models.IntegerField(default=3, verbose_name="حداقال موجودی")
    variant=models.CharField(max_length=10,choices=VARIANTS, default='None', verbose_name="ویژگی های محصول")
    category=models.ForeignKey(Category,on_delete=models.CASCADE, verbose_name="دسته بندی" , null = True , blank=True)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE, verbose_name="برند محصول")
    status=models.BooleanField(default=True, verbose_name="وضعیت انتشار")
    is_featured = models.BooleanField(default=False, verbose_name="تایید محصول")
    date_of_made = models.CharField(_("تاریخ ساخت") , max_length=100, null=True)
    name_of_country = models.CharField(_("کشور سازنده") , max_length=200 , null=True)
    model = models.CharField(_("مدل محصول") , max_length=100 , null=True)
    tags = TaggableManager(verbose_name="تگ محصول")

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.id , self.slug])

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""



# Product Attribute
class ProductAttribute(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    color=models.ForeignKey(Color,on_delete=models.CASCADE , blank=True , null=True)
    #size=models.ForeignKey(Size,on_delete=models.CASCADE , blank=True, null=True)
    price=models.PositiveIntegerField(default=0)
    image_id = models.IntegerField(blank=True,null=True,default=0)
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'ویژگی محصولات'
        verbose_name_plural = "ویژگی ها"

    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             varimage=img.image.url
        else:
            varimage=""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""


class Images(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(blank=True, upload_to='images/')
    class Meta:
        verbose_name = 'عکس محصول'
        verbose_name_plural = "عکس محصولات"
    def __str__(self):
        return self.title

# Order


RATING=(
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
)
RECOMMEND = (
    ('خرید این محصول را توصیه می‌کنم' , 'خرید این محصول را توصیه می‌کنم'),
    ('خرید این محصول را توصیه نمیکنم' , 'خرید این محصول را توصیه نمیکنم'),
)
class ProductReview(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    review_text = models.TextField(verbose_name="متن دیدگاه")
    review_rating = models.CharField(choices=RATING , max_length=150 , verbose_name="امتیاز") 
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes', verbose_name='نپسندیدن')
    likes = models.ManyToManyField(User, blank=True, related_name='likes', verbose_name='پسندیدن')
    #recommend = models.BooleanField(default=False ,verbose_name="خرید این محصول را توصیه می‌کنم")
    recommend = models.CharField(choices=RECOMMEND , max_length=150 , verbose_name="توصیه خرید محصول")
    status = models.BooleanField(default=False , verbose_name="وضعیت")
	
    def get_review_rating(self):
        return self.review_rating
    
    class Meta:
        verbose_name = 'دیدگاه کاربر'
        verbose_name_plural = "دیدگاه کاربران"


class Wishlist (models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'لیست علاقه مندی کاربران'
        verbose_name_plural = "علاقه مندی ها"
   


# AddressBook
class UserAddressBook(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(null=True,blank=True , max_length=50 , verbose_name="شماره همراه")
    address=models.TextField(null=True,blank=True , verbose_name="آدرس محل سکونت")
    city = models.CharField(null=True,blank=True, max_length=20)
    country = models.CharField(null=True,blank=True, max_length=50)
    postal_code = models.IntegerField(null=True,blank=True , max_length=150)
    tag = models.IntegerField(null=True,blank=True , max_length=100)
    vahed = models.IntegerField(null=True,blank=True , max_length =20)
    phone_2 = models.IntegerField(null=True,blank=True ,  max_length= 100)
    #image = models.ImageField(null=True,blank=True, upload_to='images/users/')
    status=models.BooleanField(null=True,blank=True , default=True , verbose_name="وضعیت")

    def get_photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/static/images/adata.png"

    class Meta:
        verbose_name_plural='AddressBook'
    
    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] '

    class Meta:
        verbose_name = 'دفترچه آدرس کاربران'
        verbose_name_plural = "دفترچه آدرس"




class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    variant = models.ForeignKey(ProductAttribute, on_delete=models.SET_NULL,blank=True, null=True) # relation with varinat
    quantity = models.IntegerField(verbose_name="تعداد سفارش")

    def __str__(self):
        return self.product.title

    @property
    def price(self):
        return (self.product.price)

    @property
    def amount(self):
        return (self.quantity * self.product.price)

    @property
    def varamount(self):
        return (self.quantity * self.variant.price)


    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = "سبد خرید محصولات"
class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preaparing', 'Preaparing'),
        ('OnShipping', 'OnShipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=5, editable=False )
    first_name = models.CharField(max_length=10 , null=True)
    last_name = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=150 , null = True)
    phone_2 = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    tag = models.IntegerField(null = True ,max_length=150)
    vahed = models.IntegerField(null = True , max_length=150)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    total = models.FloatField()
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(max_length=100)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name


    class Meta:
        verbose_name = 'سفارشات کاربر'
        verbose_name_plural = "سفارشات کاربران"

    def jpublish(self):
        return jalali_converter(self.create_at)
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name', 'phone' , 'postal_code' , 'city', 'country' , 'tag', 'vahed' , 'phone_2','address']

class OrderProduct(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductAttribute, on_delete=models.SET_NULL,blank=True, null=True) # relation with varinat
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'سفارشات محصول'
        verbose_name_plural = "سفارشات"

    def jpublish(self):
        return jalali_converter(self.create_at)



class Notify(models.Model):
    notify_detail = models.TextField()
    read_by_user = models.ForeignKey(User , on_delete=models.CASCADE , null=True)
 
    def __str__(self):
        return str(self.notify_detail)

    class Meta:
        verbose_name = 'اعلانات'
        verbose_name_plural = "اعلانات"

class NotifUserStatus(models.Model):
    notif = models.ForeignKey(Notify, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'وضعیت بازدید از اعلانات'
        verbose_name_plural = "وضعیت اعلانات"


class Coupon(models.Model):
    code = models.CharField(max_length=50 , unique=True  , verbose_name="کد تخفیف")
    valid_from = models.DateTimeField(verbose_name="اعتبار از ")
    valid_to = models.DateTimeField(verbose_name="اعتبار تا ")
    discount = models.IntegerField(validators =[MinValueValidator(0),MaxValueValidator(100)] ,verbose_name="درصد تخفیف")
    active = models.BooleanField(verbose_name="فعال")

    def __str__(self):
        return self.code
    

    class Meta:
        verbose_name = 'کوپن تخفیف'
        verbose_name_plural = "کوپن تخفیفات"

class Category_Blog (models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(null=True, unique=True)


    class Meta:
        verbose_name = 'دسته بندی مقاله'
        verbose_name_plural = "دسته بندی مقالات"

class Blog (models.Model):
    title = models.CharField(max_length=150)
    descriptions = RichTextField()
    image = models.ImageField(blank=True, upload_to='blog_images/')
    slug = models.SlugField(null=True, unique=True)
    date = models.DateTimeField()
    status = models.BooleanField()
    views = models.IntegerField()

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = "مقالات"

    def __str__(self):
        return self.title

class Comment(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE , verbose_name= "محصول")
    reply = models.ForeignKey("Comment" , null=True , on_delete=models.CASCADE , blank=True , related_name="replies" , verbose_name = "پاسخ به نظر")
    name = models.CharField(max_length=200 , verbose_name= "نام")
    family = models.CharField(max_length=200 , verbose_name= "نام خانوادگی")
    email = models.EmailField(verbose_name= "آدرس الکترونیکی")
    text_comment = models.TextField(verbose_name="متن پرسش")
    status = models.BooleanField(default=False , verbose_name= "وضعیت نمایش")
	
    def get_review_rating(self):
        return self.text_comment
    
    class Meta:
        verbose_name = 'پرسش و پاسخ کاربر'
        verbose_name_plural = "پرسش و پاسخ کاربران"


class CommentBlog (models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE , verbose_name= "مقاله")
    reply = models.ForeignKey("CommentBlog" , null=True , on_delete=models.CASCADE , related_name="replies" , verbose_name= "پاسخ به نظر")
    name = models.CharField(max_length=200 , verbose_name= "نام کاربر")
    title = models.CharField(max_length=200 , verbose_name= "عنوان نظر")
    text = models.TextField(max_length=10000 , verbose_name= "متن نظر")
    create_date = models.DateTimeField(auto_now_add=True , verbose_name= "تاریخ درج نظر")

    def __str__(self):
        return '{}'.format(self.title)
        
    class Meta:
        verbose_name = 'نظرات مقاله'
        verbose_name_plural = "نظرات مقالات"

class Contact_Us (models.Model):
    subject = models.CharField(max_length= 200)
    name = models.CharField(max_length = 200) 
    email = models.EmailField()
    phone = models.IntegerField(max_length="20")
    text_message = models.TextField()


    def __str__(self):
        return self.subject
        
    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = "تماس با ما"