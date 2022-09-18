from attr import field
from django.contrib import admin
from .models import *
# Register your models here.
import admin_thumbnails
from mptt.admin import DraggableMPTTAdmin
import csv
import datetime
from django.http import HttpResponse





admin.site.register(Brand)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title' , 'image_tag')
#admin.site.register(Category , CategoryAdmin)


class CategoryAdmin2(admin.ModelAdmin):
    list_display = ('title' , 'slug' , 'parent' , 'position' , 'status'  , 'image_tag')
admin.site.register(Category , CategoryAdmin2)

class contact_us(admin.ModelAdmin):
    list_display = ('subject' , 'name' , 'email' , 'phone' , 'text_message')
admin.site.register(Contact_Us , contact_us)

class ProductReviewAdmin(admin.ModelAdmin):
    list_display=('user' , 'product' , 'review_text' , 'get_review_rating' )
admin.site.register(ProductReview , ProductReviewAdmin)



admin.site.register(Wishlist)




class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name','address', 'mobile','city','country', 'vahed' , 'tag' , 'phone_2' , 'postal_code']

admin.site.register(UserAddressBook,UserProfileAdmin)



class ShopCartAdmin(admin.ModelAdmin):
    list_display = ('product','user','quantity','price','amount' )
    
admin.site.register(ShopCart , ShopCartAdmin)




@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1

class ProductVariantsInline(admin.TabularInline):
    model = ProductAttribute
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True


@admin_thumbnails.thumbnail('image')
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image','title','image_thumbnail']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category', 'status','image_tag']
    list_filter = ['category']
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline,ProductVariantsInline]
    prepopulated_fields = {'slug': ('title',)}


class ColorAdmin(admin.ModelAdmin):
    list_display = ['title','color_code','color_tag']




class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title','product','color','price','quantity','image_tag']


admin.site.register(Product,ProductAdmin)
admin.site.register(Images,ImagesAdmin)
admin.site.register(Color,ColorAdmin)






def export_csv(modeladmin , request , queryset):
    opts = modeladmin.model._meta
    content = 'attchment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type = "text/csv")
    response['Content-disposition'] = content
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    writer.writerow([field for field in fields]) 
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj , field.name)
            if isinstance(value , datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_csv.short_description = "خروجی فایل csv"    



class OrderProductline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product','price','quantity','amount')
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name','phone','city','total','status']
    list_filter = ['status']
    readonly_fields = ['user' , 'total' , 'ip' , 'first_name','last_name', 'phone' , 'postal_code' , 'city', 'country' , 'tag', 'vahed' , 'phone_2','address']
    can_delete = False
    inlines = [OrderProductline]
    actions = [export_csv]




class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product','price','quantity','amount']
    list_filter = ['user']

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)

admin.site.register(Notify)
admin.site.register(NotifUserStatus)



@admin.register(Coupon)
class CouponsAdmin(admin.ModelAdmin):
    list_display = ['code' , 'valid_from' , 'valid_to' , 'discount' , 'active']
    list_filter = ['active' , 'valid_to' , 'valid_from']
    search_field = ['code']


class Blogadmin(admin.ModelAdmin):
    list_display = ['title' , 'slug' , 'date' , 'views' , 'status']
    list_filter = ['date' , 'views']
admin.site.register(Blog , Blogadmin)


admin.site.register(Category_Blog)

class CommentReviewAdmin(admin.ModelAdmin):
    list_display=('name' , 'family' , 'text_comment' , 'email' )
    list_filter =['status']
    search_field = ['name']
admin.site.register(Comment , CommentReviewAdmin)




class CommentBlogAdmin(admin.ModelAdmin):
    list_display=('name' , 'title' , 'text' , 'create_date' )
    list_filter =['name']
admin.site.register(CommentBlog , CommentBlogAdmin)