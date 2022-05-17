from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.fields import CharField, IntegerField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
import datetime
from django.core.exceptions import ObjectDoesNotExist

from .models import Breakfast, DefaultInstance, Lunch, ProductInstance, User, Product, Meal, Diary, DiaryEntry, Dinner, Snacks, Favs, Default, Faulty

from . import helperfunctie
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        today = datetime.datetime.today()

        # Converts datetime object into string (YYYY-MM-DD)
        date=helperfunctie.date_converter(today)
        return HttpResponseRedirect(reverse("alt", args=(date,)))
    else: 
        return HttpResponseRedirect(reverse("login"))


def index_alt(request, date):
    if request.user.is_authenticated:
        diary = request.user.diary
        try:
            entry = diary.entries.get(date=date)

            breakfast = entry.breakfast
            lunch = entry.lunch
            dinner = entry.dinner
            snacks = entry.snacks
            
            # Calculates daily totals for the different nutrient classes
            totals = helperfunctie.daily_totals(breakfast.nutrition(), lunch.nutrition(), dinner.nutrition(), snacks.nutrition())

            # Converts date (YYYY-MM-DD) into datetime object
            date_object = helperfunctie.datetime_converter(date)

            yesterday_object = date_object - datetime.timedelta(1)
            yesterday = helperfunctie.date_converter(yesterday_object)

            tomorrow_object = date_object + datetime.timedelta(1)
            tomorrow = helperfunctie.date_converter(tomorrow_object)
            return render(request, "food_tracker/index.html", {
                "date_object": date_object, 
                "date": date,
                "previous": yesterday,
                "next": tomorrow,
                "periods": [breakfast, lunch, dinner, snacks],
                "totals": totals,
            })
        except ObjectDoesNotExist:
            entry = DiaryEntry(date=date, diary=diary)
            entry.save()

            instant_periods(entry)
            return HttpResponseRedirect(reverse("alt", args=(date,)))                     
    else: 
        return HttpResponseRedirect(reverse("index"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "food_tracker/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "food_tracker/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "food_tracker/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, password)
            user.save()

            diary = Diary(user=user)
            diary.save()
        except IntegrityError:
            return render(request, "food_tracker/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "food_tracker/register.html")


def search(request, date):
    return render(request, "food_tracker/search.html", {
        "date": date
    })


def results(request, date):
    query = request.POST["q"]

    products = Product.objects.filter(name__icontains=query)
    meals = Meal.objects.filter(name__icontains=query)
    favs = Favs.objects.filter(user=request.user).all()

    favorites = helperfunctie.favorites(favs)

    return render(request, "food_tracker/results.html", {
        "date": date,
        "products": products,
        "meals": meals,
        "favorites": favorites,
    })


def add_product(request, date, product_id):
    if request.method == "POST":
        diary = request.user.diary

        entry = diary.entries.get(date=date)
        product = Product.objects.get(id=product_id)
        amount = request.POST["amount"]

        if request.POST["period"] == "breakfast":
            new = ProductInstance(breakfast_item=entry.breakfast, product=product, amount=amount)
            new.save()
        elif request.POST["period"] == "lunch":
            new = ProductInstance(lunch_item=entry.lunch, product=product, amount=amount)
            new.save()
        elif request.POST["period"] == "dinner":
            new = ProductInstance(dinner_item=entry.dinner, product=product, amount=amount)
            new.save()
        else:
            new = ProductInstance(snack_item=entry.snacks, product=product, amount=amount)
            new.save()
        return HttpResponseRedirect(reverse("alt", args=(date,)))
    else:
        return render(request, "food_tracker/add_product.html", {
            "product": Product.objects.get(id=product_id),
        })


def calender(request):
    date = request.POST["date"]

    if date == '':
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("alt", args=(date,)))


def new_product(request):
    if request.method == "POST":
        name = request.POST["name"]
        unit = request.POST["unit"]
        calories = request.POST["calories"]
        carbs = request.POST["carbs"]
        protein = request.POST["protein"]
        fat = request.POST["fat"]

        new_product = Product(name=name, unit=unit, calories=calories, carbs=carbs, protein=protein, fat=fat, creator=request.user)
        new_product.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "food_tracker/new_product.html")


def add_meal(request, meal_id, date):
    if request.method == "POST":
        diary = request.user.diary
        try:
            entry = diary.entries.get(date=date)
        except ObjectDoesNotExist:
            entry = DiaryEntry(date=date, diary=diary)
            entry.save()

            instant_periods(entry)

        meal = Meal.objects.get(id=meal_id)

        for product in meal.product.all():
            amount = request.POST[f"{product.id}"]

            if request.POST["period"] == "breakfast":
                new = ProductInstance(breakfast_item=entry.breakfast, product=product, amount=amount)
                new.save()
            elif request.POST["period"] == "lunch":
                new = ProductInstance(lunch_item=entry.lunch, product=product, amount=amount)
                new.save()
            elif request.POST["period"] == "dinner":
                new = ProductInstance(dinner_item=entry.dinner, product=product, amount=amount)
                new.save()
            else:
                new = ProductInstance(snack_item=entry.snacks, product=product, amount=amount)
                new.save()
        return HttpResponseRedirect(reverse("alt", args=(date,)))
    else:
        return render(request, "food_tracker/add_meal.html", {
            "meal": Meal.objects.get(id=meal_id),
            "date": date,
        })


def new_meal(request):
    if request.method == "POST":
        name = request.POST["name"]

        meal = Meal(name=name, creator=request.user)
        meal.save()
        return HttpResponseRedirect(reverse("meal", args=(meal.id,)))
    else:
        return render(request, "food_tracker/new_meal.html")


def meal(request, meal_id):
    meal = Meal.objects.get(id=meal_id)
    return render(request, "food_tracker/meal.html", {
        "meal": meal
    })


def meal_search(request, meal_id):
    meal = Meal.objects.get(id=meal_id)
    return render(request, "food_tracker/search.html", {
        "meal": meal
    })


def meal_results(request, meal_id):
    meal = Meal.objects.get(id=meal_id)

    query = request.POST["q"]

    products = Product.objects.filter(name__icontains=query)

    return render(request, "food_tracker/meal_results.html", {
        "products": products,
        "meal": meal,
        "query": query,
    })


def meal_add_product(request, meal_id, product_id):
    meal = Meal.objects.get(id=meal_id)

    product = Product.objects.get(id=product_id)

    meal.product.add(product)
    meal.save()

    return HttpResponseRedirect(reverse("meal", args=(meal_id,)))


def meal_delete_product(request, meal_id, product_id):
    meal = Meal.objects.get(id=meal_id)

    product = Product.objects.get(id=product_id)

    meal.product.remove(product)
    meal.save()

    return HttpResponseRedirect(reverse("meal", args=(meal_id,)))


def my_meals(request):
    meals = request.user.created_meals.all()

    fav_objects = Favs.objects.filter(user=request.user).all()

    favorites = helperfunctie.favorites(fav_objects)

    return render(request, "food_tracker/my_meals.html", {
        "meals": meals,
        "favorites": favorites,
    })


def favorites(request):
    favs = Favs.objects.filter(user=request.user).all()

    products = []
    meals = []

    for fav in favs:
        if fav.product != None:
            products.append(fav.product)
        else:
            meals.append(fav.meal)

    return render(request, "food_tracker/favorites_results.html", { 
        "products": products,
        "meals": meals, 
        "favorites": products + meals,
    })


def delete_product_favorite(request, product_id):
    product = Product.objects.get(id=product_id)

    fav = Favs.objects.get(user=request.user, product=product)
    fav.delete()

    return HttpResponseRedirect(reverse("favorites"))



def add_product_favorite(request, product_id): 
    product = Product.objects.get(id=product_id)

    fav = Favs(user=request.user, product=product, meal=None)
    fav.save()

    return HttpResponseRedirect(reverse("favorites"))


def delete_meal_favorite(request, meal_id):
    meal = Meal.objects.get(id=meal_id)

    fav = Favs.objects.get(user=request.user, meal=meal)
    fav.delete()

    return HttpResponseRedirect(reverse("favorites"))



def add_meal_favorite(request, meal_id): 
    meal = Meal.objects.get(id=meal_id)

    fav = Favs(user=request.user, product=None, meal=meal)
    fav.save()

    return HttpResponseRedirect(reverse("favorites"))


def meal_specify_date(request, meal_id):
    return render(request, "food_tracker/meal_specify_date.html", {
        "meal": Meal.objects.get(id=meal_id),
    })


def meal_send_date(request, meal_id):
    date = request.POST["date"]
    if date == '':
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("add_meal", args=(meal_id, date,)))


def product_specify_date(request, product_id):
    return render(request, "food_tracker/product_specify_date.html", {
        "product": Product.objects.get(id=product_id),
    })


def product_send_date(request, product_id):
    date = request.POST["date"]

    return HttpResponseRedirect(reverse("add_product", args=(product_id, date,)))


def default(request, meal_id, date):
    meal = Meal.objects.get(id=meal_id)

    try:
        default = Default.objects.get(user=request.user, meal=meal)

        instances = default.instances.all()

        products = []

        for instance in instances:
            products.append(instance.product)

        return render(request, "food_tracker/default.html", {
        "meal": meal, 
        "date": date,
        "defaults": instances,
        "products": products,
        })

    except ObjectDoesNotExist:
        return render(request, "food_tracker/default.html", {
        "meal": meal, 
        "date": date,
        })


def set_default(request, meal_id, date):
    meal = Meal.objects.get(id=meal_id)

    try:
        default = Default.objects.get(user=request.user, meal=meal)

        for product in meal.product.all():
            try:
                instance = DefaultInstance.objects.get(default=default, product=product)

                amount = request.POST[f"{product.id}"]

                instance.amount = amount
                instance.save()
            except ObjectDoesNotExist:
                amount = request.POST[f"{product.id}"]

                instance = DefaultInstance(default=default, product=product, amount=amount)
                instance.save()

        return HttpResponseRedirect(reverse("add_meal", args=(meal_id, date,)))

    except ObjectDoesNotExist:
        default = Default(user=request.user, meal=meal)
        default.save()

        for product in meal.product.all():
            amount = request.POST[f"{product.id}"]

            instance = DefaultInstance(default=default, product=product, amount=amount)
            instance.save()

        return HttpResponseRedirect(reverse("add_meal", args=(meal_id, date,)))


def get_default(request, meal_id, date):
    meal = Meal.objects.get(id=meal_id)

    try:
        default = Default.objects.get(user=request.user, meal=meal)

        instances = default.instances.all()

        products = []

        for instance in instances:
            products.append(instance.product)

        return render(request, "food_tracker/add_meal.html", {
                "meal": Meal.objects.get(id=meal_id),
                "date": date,
                "defaults": instances,
                "products": products, 
                })
    except ObjectDoesNotExist:
        return render(request, "food_tracker/add_meal.html", {
            "meal": Meal.objects.get(id=meal_id),
            "date": date,
            "message": "Er Zijn Nog Geen Voorkeuren Ingesteld Voor Dit Product",
        })


def faulty_product(request, product_id):
    product = Product.objects.get(id=product_id)

    faulty_product = Faulty(user=request.user, product=product)
    faulty_product.save()

    return HttpResponseRedirect(reverse("index"))


def instant_periods(entry):
    breakfast = Breakfast(entry=entry)
    breakfast.save()

    lunch = Lunch(entry=entry)
    lunch.save()

    dinner = Dinner(entry=entry)
    dinner.save()

    snacks = Snacks(entry=entry)
    snacks.save()














