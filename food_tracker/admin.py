from django.contrib import admin

from .models import Favs, User, Product, Meal, Diary, DiaryEntry, Breakfast, Lunch, Dinner, Snacks, ProductInstance, Favs, Default, DefaultInstance

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Meal)
admin.site.register(Diary)
admin.site.register(DiaryEntry)
admin.site.register(Breakfast)
admin.site.register(Lunch)
admin.site.register(Dinner)
admin.site.register(Snacks)
admin.site.register(ProductInstance)
admin.site.register(Favs)
admin.site.register(DefaultInstance)
admin.site.register(Default)